import asyncio
import threading
import time
import logging

import minecraft
import qqbotAPI as api
from queue import Queue
from typing import Union, Any
from config import config
from commands import commands
from nakuru import (
    CQHTTP,
    GroupMessage,
    FriendMessage,
    Notify,
)
from nakuru.entities.components import Plain, Image


class baseTarget: ...


class group(baseTarget): ...


class private(baseTarget): ...


targetTypes = {
    "group": group,
    "private": private
}

targetTypesLang = {
    group: "群聊",
    private: "私聊"
}

bot = CQHTTP()


class qqbot:
    bot: CQHTTP
    qqMsgQueue: Queue[str]
    minecraftMsgQueue: Queue[str]
    _targetType: Union[group, private]
    _targetId: int
    _minecraftObject: minecraft.minecraft

    def __init__(self, target_id: int, target_type: Union[group, private],
                 minecraft_object: minecraft.minecraft,
                 host: str = "127.0.0.1", port: int = 6700, http_port: int = 5700, token: Union[str, None] = None):
        logging.info("初始化QQBot...")
        self.bot = CQHTTP(host, port, http_port, token)
        self.qqMsgQueue = Queue(maxsize=5)
        self._minecraftMsgQueue = Queue(maxsize=5)
        self._targetId = target_id
        self._targetType = target_type
        self._minecraftObject = minecraft_object

    @bot.receiver("GroupMessage")
    @bot.receiver("FriendMessage")
    async def _(self, bot: CQHTTP, source: Union[GroupMessage, FriendMessage]):
        logging.info(f"收到 QQ消息: {source.raw_message}")
        # 处理指令
        if source.message[0] == "!" and len(source.message) > 1:
            cmd = source.message[1::]
            if cmd in commands.keys():
                # 是有效命令
                self._minecraftObject.sendMessage(f"/{cmd}")
        # 处理消息
        self._minecraftObject.sendMessage(
            f"§b[§l{targetTypesLang[type(self._targetType)]}§r(§{config.targetQid}§b)]§a<{source.user_id}>§f "
            f"{source.message}")  # 目前不支持CQ TODO

        """
        代码参考
        # 通过纯 CQ 码处理
        if source.raw_message == "戳我":
            await bot.sendGroupMessage(source.group_id, f"[CQ:poke,qq={source.user_id}]")
        # 通过消息链处理
        chain = source.message
        if isinstance(chain[0], Plain):
            if chain[0].text == "看":
                await bot.sendGroupMessage(source.group_id, [
                    Plain(text="给你看"),
                    Image.fromFileSystem("D:/好康的.jpg")
                ])
        """

    @bot.receiver("Notify")
    async def _(self, bot: CQHTTP, source: Notify):
        if source.sub_type == "poke" and source.target_id == self._targetId:
            logging.info("收到 戳一戳 ，返回群服互通信息。")
            await bot.sendGroupMessage(source.group_id, "唔..群服互通工作正常！")

    def sendMessage(self, message: str):
        logging.debug("put message")
        self.qqMsgQueue.put(message)

    async def _syncMessage(self):
        message = self.qqMsgQueue.get()
        logging.info(f"向 QQ 发送消息: {message}")
        if self._targetType is group:
            await self.bot.sendGroupMessage(self._targetId, message)
        elif self._targetType is private:
            await self.bot.sendFriendMessage(self._targetId, message)
        else:
            raise TypeError(f"不支持的 QQ 目标类型: {self._targetType}")

    async def run(self):
        logging.info("启动 QQ 消息同步")
        self.sendMessage("▌ 群服互联已连接 ┈━═☆")
        threading.Thread(target=await self.bot._run(), name="QQBotThread").start()  # 危险
        while True:
            if not self.qqMsgQueue.empty():
                await self._syncMessage()
            if not self._minecraftObject.getChatStream().empty():
                self.sendMessage(f"[MC]{self._minecraftObject.getChatStream().get().message}")


# class qqbot:
#     api: pycqBot.cqHttpApi
#     bot: pycqBot.cqBot
#     _invalidGroups: Union[list[int], list[None]]
#     _invalidUsers: Union[list[int], list[None]]
#     _commands: _commandAPI
#     _qqbotThread: thread.Thread
#     _messageThread: thread.Thread
#     _messageQueue: Queue
#
#     def __init__(self, groups: Union[list[int], list[None]], users: Union[list[int], list[None]]):
#         """
#         初始化qqbot。
#         :param groups: 需要处理消息的群聊。
#         :param users: 需要处理消息的单聊。
#         """
#         self._invalidGroups = groups
#         self._invalidUsers = users
#         self._commands = _commandAPI()
#         self._commands.antiSpam = config.AntiSpam
#         self._commands.antiSpamDelay = config.AntiSpamInterval
#         self._commands.antiSpamMode = eval(f"api.random.{config.AntiSpamMode}")  # 危险的使用方式
#         self._messageThread = thread.Thread(target=self._sendMessage)
#         self._messageQueue = Queue(maxsize=5)
#         self._messageThread.start()
#         self.api = pycqBot.cqHttpApi()
#         self.bot = self.api.create_bot(group_id_list=self._invalidGroups, user_id_list=self._invalidUsers)
#         self._qqbotThread = thread.Thread(target=self.bot.start, name="QQBotThread", args=(
#             config.cqhttpPath, True, config.autoStartCqhttp))
#
#     def _commandInit(self):
#         """
#         初始化命令。
#         :return: none
#         """
#         self.bot.command(self._commands.echoModule, "echo", {
#             "help": [
#                 "#echo [内容] - 输出文本"
#             ],
#             "type": "all"
#         })
#         self.bot.command(self._commands.antiSpamModule, "antispam", {
#             "help": [
#                 "#antispam [延迟时间] [随机化] - 反刷屏功能，延迟时间单位为秒，随机化可选值为：none,normal,extra。",
#             ],
#             "type": "all"
#         })
#
#     def sendMessage(self, target: int, target_type: str, message: str):
#         """
#         发送消息。
#         :param target: 目标ID
#         :param target_type: 目标类型 (group,private)
#         :param message: 信息内容
#         :return: none
#         """
#         if self._commands.antiSpam:
#             delay = self._commands.antiSpamDelay + self._commands.antiSpamMode(self._commands.antiSpamDelay)
#         else:
#             delay = 0
#
#         if self._messageQueue.full():
#             self._messageQueue.get()
#         self._messageQueue.put((target, target_type, message, delay))
#
#     def _sendMessage(self):
#         while True:
#             target, target_type, message, delay = self._messageQueue.get()
#             if target_type == "group":
#                 self.api.send_group_msg(group_id=target, message=message)
#             elif target_type == "private":
#                 self.api.send_private_msg(user_id=target, message=message)
#             else:
#                 log = f"发送信息目标类型错误：ValueError: {target_type} 应为 group 或 private。"
#                 logging.error(log)
#                 return
#             logging.info(f"向 {target_type} {target} 发送信息：{message}")
#             time.sleep(delay)
#
#     def silentStart(self):
#         self._qqbotThread.start()
#
#     def stop(self):
#         self.bot.stop()
#         self._qqbotThread.join()
#         self._messageThread.join()
