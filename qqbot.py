import time

import pycqBot.cqHttpApi
import pycqBot.data
import pycqBot
import logging
import qqbotAPI as api
from queue import Queue
from typing import Any, Union
from config import config
import threading as thread

pycqBot.cqLog(logging.INFO)


class _commandAPI:
    antiSpam: bool
    antiSpamDelay: float
    antiSpamMode: Any

    def __init__(self):
        self.antiSpam = True
        self.antiSpamDelay = 1.0
        self.antiSpamMode = api.random.normal

    @staticmethod
    def echoModule(command_data: list[str], message: pycqBot.data.Message):
        message.reply(" ".join(command_data))

    def antiSpamModule(self, command_data: list[str], message: pycqBot.data.Message):
        if self.antiSpam:
            self.antiSpam = False
            log = "反刷屏已禁用"
            logging.info(log)
            message.reply(log)
        else:
            try:
                self.antiSpamDelay = float(command_data[0])
            except ValueError as err:
                log = f"反刷屏延迟时间错误：ValueError: {err}"
                logging.error(log)
                message.reply(log)
            except IndexError as err:
                log = f"反刷屏参数不足：IndexError: {err}"
                logging.error(log)
                message.reply(log)
            try:
                self.antiSpamMode = getattr(api.random, command_data[1])
            except AttributeError as err:
                log = f"反刷屏随机化错误：AttributeError: {err}"
                logging.error(log)
                message.reply(log)
            except IndexError as err:
                log = f"反刷屏参数不足：IndexError: {err}"
                logging.error(log)
                message.reply(log)
            self.antiSpam = True
            log = f"反刷屏已启用，延迟时间：{self.antiSpamDelay}，随机化：{self.antiSpamMode.__name__}"
            logging.info(log)
            message.reply(log)


class qqbot:
    api: pycqBot.cqHttpApi
    bot: pycqBot.cqBot
    _invalidGroups: Union[list[int], list[None]]
    _invalidUsers: Union[list[int], list[None]]
    _commands: _commandAPI
    _qqbotThread: thread.Thread
    _messageThread: thread.Thread
    _messageQueue: Queue

    def __init__(self, groups: Union[list[int], list[None]], users: Union[list[int], list[None]]):
        """
        初始化qqbot。
        :param groups: 需要处理消息的群聊。
        :param users: 需要处理消息的单聊。
        """
        self._invalidGroups = groups
        self._invalidUsers = users
        self._commands = _commandAPI()
        self._commands.antiSpam = config.AntiSpam
        self._commands.antiSpamDelay = config.AntiSpamInterval
        self._commands.antiSpamMode = eval(f"api.random.{config.AntiSpamMode}")
        self._messageThread = thread.Thread(target=self._sendMessage)
        self._messageQueue = Queue(maxsize=5)
        self._messageThread.start()
        self.api = pycqBot.cqHttpApi()
        self.bot = self.api.create_bot(group_id_list=self._invalidGroups, user_id_list=self._invalidUsers)
        self._qqbotThread = thread.Thread(target=self.bot.start, name="QQBotThread", args=(
            config.cqhttpPath, True, config.autoStartCqhttp))

    def _commandInit(self):
        """
        初始化命令。
        :return: none
        """
        self.bot.command(self._commands.echoModule, "echo", {
            "help": [
                "#echo [内容] - 输出文本"
            ],
            "type": "all"
        })
        self.bot.command(self._commands.antiSpamModule, "antispam", {
            "help": [
                "#antispam [延迟时间] [随机化] - 反刷屏功能，延迟时间单位为秒，随机化可选值为：none,normal,extra。",
            ],
            "type": "all"
        })

    def sendMessage(self, target: int, target_type: str, message: str):
        """
        发送消息。
        :param target: 目标ID
        :param target_type: 目标类型 (group,private)
        :param message: 信息内容
        :return: none
        """
        if self._commands.antiSpam:
            delay = self._commands.antiSpamDelay + self._commands.antiSpamMode(self._commands.antiSpamDelay)
        else:
            delay = 0

        if self._messageQueue.full():
            self._messageQueue.get()
        self._messageQueue.put((target, target_type, message, delay))

    def _sendMessage(self):
        while True:
            target, target_type, message, delay = self._messageQueue.get()
            if target_type == "group":
                self.api.send_group_msg(group_id=target, message=message)
            elif target_type == "private":
                self.api.send_private_msg(user_id=target, message=message)
            else:
                log = f"发送信息目标类型错误：ValueError: {target_type} 应为 group 或 private。"
                logging.error(log)
                return
            logging.info(f"向 {target_type} {target} 发送信息：{message}")
            time.sleep(delay)

    def silentStart(self):
        self._qqbotThread.start()

    def stop(self):
        self.bot.stop()
        self._qqbotThread.join()
        self._messageThread.join()
