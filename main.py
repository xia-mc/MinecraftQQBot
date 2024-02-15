import logging
from config import config
import minecraft
import asyncio
import qqbot

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

    targetType = qqbot.targetTypes[config.targetType]
    bot = qqbot.qqbot(config.targetQid, targetType,
                      config.botHost, config.botPort, config.botHttpPort, config.botToken)

    mc = minecraft.minecraft(config.minecraftLogPath)
    chatStream = mc.getChatStream()
    mc.silentSyncChat()
    asyncio.run(bot.run())
    while True:
        if chatStream.qsize() != 0:
            msg = chatStream.get()
            bot.sendMessage(msg.message)
