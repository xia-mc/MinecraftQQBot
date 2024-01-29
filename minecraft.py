from typing import IO
from dataclasses import dataclass
from threading import Thread
from queue import Queue
from config import config
import logging
import time
import re


@dataclass
class message:
    """
    time: HH:MM:SS
    message: 消息内容
    """
    time: str
    message: str


class minecraft:
    file: IO
    stream: Queue[message]
    _silentSyncThread: Thread
    _silentSync: list[bool]
    _blockUpdate: list[bool]

    def __init__(self, file: str, encoding: str = 'UTF-8', max_delay: int = 2):
        """
        配置消息同步器。
        :param file: 日志文件的绝对路径
        :param encoding: 日志文件的解码方式
        :param max_delay: 最多缓存的消息数量
        """
        logging.info("初始化消息同步器...")
        self.file = open(file, 'r', encoding=encoding)
        self.stream = Queue(maxsize=max_delay)
        self._silentSyncThread = Thread()
        self._silentSync = [True]
        self._blockUpdate = [True]
        logging.info("开始同步消息。")
        self._syncChat()

    def getChatStream(self) -> Queue[message]:
        return self.stream

    def _syncChat(self):
        for line in self.file.readlines():
            if re.match(config.minecraftLogMatch, line) is not None:
                if self.stream.qsize() == self.stream.maxsize:
                    self.stream.get()
                self.stream.put(message(line[1:9], line[config.minecraftLogStartIndex:].replace('\n', '')))

    def syncChat(self, interval: float = 0.1):
        """
        (blocking)
        mainloop.
        :param interval:
        :return:
        """
        while self._blockUpdate[0]:
            self._syncChat()
            time.sleep(interval)

    def silentSyncChat(self, interval: float = 0.1):
        """
        (non-blocking)
        mainloop.
        :param interval:
        :return:
        """
        def _update():
            while self._silentSync[0]:
                self._syncChat()
                time.sleep(interval)

        self._silentSyncThread = Thread(target=_update, name="SilentSyncThread")
        self._silentSyncThread.start()

    def stop(self):
        self._silentSync[0] = False
        self._blockUpdate[0] = False
        self._silentSyncThread.join()

    def close(self):
        self.stop()
        self.file.close()

    def __del__(self):
        self.close()

    def __exit__(self):
        self.close()