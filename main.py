import logging
from config import config
import minecraft
import threading as thread
import asyncio
import qqbot


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

    targetType = qqbot.targetTypes[config.targetType]
    mc = minecraft.minecraft(config.minecraftLogPath)
    bot = qqbot.qqbot(config.targetQid, targetType,
                      mc,
                      config.botHost, config.botPort, config.botHttpPort, config.botToken)
    chatStream = mc.getChatStream()
    mc.silentSyncChat()

    asyncio.run(bot.run())

