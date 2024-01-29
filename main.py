import logging
from config import config
import minecraft
import qqbot


def qqbot_main():
    # bot.silentStart()
    # bot.sendMessage(629995608, "private", "1")
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

    bot = qqbot.qqbot([None], [None])
    qqbot_main()
    mc = minecraft.minecraft(config.minecraftLogPath)
    chatStream = mc.getChatStream()
    mc.silentSyncChat()
    while True:
        if chatStream.qsize() != 0:
            msg = chatStream.get()
            logging.info(f'收到 Minecraft 消息: {msg}')
            bot.sendMessage(config.targetQid, config.targetType, msg.message)
