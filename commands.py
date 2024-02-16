from dataclasses import dataclass
from config import config
import logging
import json

COMMANDS_INDEX_FILE = "commands/__index__.json"


@dataclass
class _commandData:
    match: str = ""
    startIndex: int = 48


class _commandsManager:
    validCommands: list
    mcVersion: str
    language: str
    _data: dict[str, _commandData]

    def __init__(self, minecraft_version: str, language: str) -> None:
        logging.info("初始化自定义命令...")
        self.validCommands = []
        self.mcVersion = minecraft_version
        self.language = language
        self._data = {}
        self.syncFromFile()
        logging.info(f"找到 {len(self.validCommands)} 个自定义命令.")

    def getData(self):
        return self._data

    def syncFromFile(self):
        with open(COMMANDS_INDEX_FILE) as indexFile:
            self.validCommands = json.load(indexFile)["commands"]
            for command in self.validCommands:
                with open(f"./commands/{command}.json", encoding="UTF-8") as langFile:
                    self._data.update({command: _commandData(**json.load(langFile)[self.mcVersion][self.language])})


# 初始化命令管理器
commandsManager = _commandsManager(config.minecraftVersion, config.minecraftLanguage)
commands = commandsManager.getData()
