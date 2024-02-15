import logging
import random as ran
import pycqBot
from typing import Any, Union
from pycqBot.data import Notice_Event
import numpy


class random:
    @staticmethod
    def none(delay: float):
        return delay

    @staticmethod
    def normal(delay: float):
        """
        适用于AntiSpam的基本随机化。
        :param delay: AntiSpam的延迟
        :return:
        """
        return ran.random() * ran.uniform(-1, 1) * delay * 0.8

    @staticmethod
    def extra(delay: float):
        """
        适用于AntiSpam的正态分布随机化。
        :param delay: AntiSpam的延迟
        :return:
        """
        return numpy.random.normal(0, delay * 0.8)


class _commandAPI:
    antiSpam: bool
    antiSpamDelay: float
    antiSpamMode: Any
    antiSpamModeList: list

    def __init__(self):
        self.antiSpam = True
        self.antiSpamDelay = 1.0
        self.antiSpamMode = random.normal
        self.antiSpamModeList = [random.none, random.normal, random.extra]

    def antiSpamModule(self, mode: Any = Union[random.none, random.normal, random.extra], delay: float = 0.0):
        assert mode in self.antiSpamModeList, "不支持的随机化模式。"
        assert delay > 0, "延迟时间必须大于0。"
        if mode is random.none:
            self.antiSpamDelay = delay
            self.antiSpam = False
            logging.info("反刷屏已禁用。")
            return
        self.antiSpam = True
        self.antiSpamDelay = delay
        self.antiSpamMode = mode
        logging.info(f"反刷屏已启用，延迟时间：{self.antiSpamDelay}，随机化：{self.antiSpamMode.__name__}")
