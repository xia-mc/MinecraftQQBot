import random as ran
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
