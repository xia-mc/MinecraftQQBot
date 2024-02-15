import configparser
import logging
import os
from dataclasses import dataclass
from typing import Union

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
CONFIG_FILENAME = 'config.ini'


@dataclass
class _Config:
    """
    来自文件的配置
    """
    minecraftLogPath: str = ""  # MC日志文件路径
    minecraftLogMatch: str = ""  # 正则表达式
    minecraftLogStartIndex: int = 0  # MC日志聊天信息开始的字符下标
    targetType: str = ""  # 目标类型，group或private
    targetQid: int = 0  # 目标QQ号
    AntiSpam: bool = False  # 反刷屏
    AntiSpamInterval: float = 0.0  # 反刷屏延迟
    AntiSpamMode: str = ""  # 反刷屏模式
    botHost: str = "127.0.0.1"  # 支持onebot协议的机器人ip
    botPort: int = 6700  # 支持onebot协议的机器人端口
    botHttpPort: int = 5700  # 支持onebot协议的机器人HTTP端口
    botToken: Union[str, None] = None  # （可选）机器人的Access-Token


class _configManager:
    configParser: configparser.ConfigParser
    filename: str
    data: _Config

    def __init__(self, filename: str):
        logging.info("初始化配置文件...")
        self.data = _Config()
        self.filename = filename
        self.configParser = configparser.ConfigParser()
        if not self._isExist(self.filename):
            logging.error("配置文件不存在。")
            self.create()
            logging.critical("配置文件已生成，程序即将退出。请完成配置后重启程序。")
            os.system("pause")
            exit()
        self._reload()
        self.sync()

    @staticmethod
    def _isExist(filename: str):
        return os.path.isfile(filename)

    def create(self):
        logging.info("创建新的配置文件...")
        self.configParser["Minecraft"] = {
            "logPath": r".\.minecraft\logs\latest.log",
            "chatMatch": r"\[\d\d:\d\d:\d\d] \[Render thread/INFO]: \[System] \[CHAT] <",
            "chatStartIndex": 48
        }
        self.configParser["QQBot"] = {
            "targetType": "group",
            "targetQid": 123456789,
            "AntiSpam": True,
            "AntiSpamInterval": 1.0,
            "AntiSpamMode": "normal"
        }
        self.configParser["onebot"] = {
            "host": "127.0.0.1",
            "port": 6700,
            "httpPort": 5700,
            "token": None
        }
        with open(self.filename, "w", encoding="utf-8") as configfile:
            self.configParser.write(configfile)

    def _reload(self):
        logging.info("读取配置文件...")
        self.configParser.read(self.filename, encoding="utf-8")

    def reload(self):
        global config
        self.reload()
        self.sync()
        config = self.data

    def sync(self):
        logging.info("同步配置文件...")
        self.data.minecraftLogPath = self.configParser["Minecraft"]["logPath"]
        self.data.minecraftLogMatch = self.configParser["Minecraft"]["chatMatch"]
        self.data.minecraftLogStartIndex = int(self.configParser["Minecraft"]["chatStartIndex"])
        self.data.targetType = self.configParser["QQBot"]["targetType"]
        self.data.targetQid = int(self.configParser["QQBot"]["targetQid"])
        self.data.AntiSpam = bool(self.configParser["QQBot"]["AntiSpam"])
        self.data.AntiSpamInterval = float(self.configParser["QQBot"]["AntiSpamInterval"])
        self.data.AntiSpamMode = self.configParser["QQBot"]["AntiSpamMode"]
        self.data.botHost = self.configParser["onebot"]["host"]
        self.data.botPort = int(self.configParser["onebot"]["port"])
        self.data.botHttpPort = int(self.configParser["onebot"]["httpPort"])
        self.data.botToken = None \
            if self.configParser["onebot"]["token"] == "None" else self.configParser["onebot"]["token"]


configManager = _configManager(CONFIG_FILENAME)
config: _Config = configManager.data
