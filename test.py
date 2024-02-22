from nakuru import (
    CQHTTP,
    GroupMessage,
    Notify,
    GroupMessageRecall,
    FriendRequest
)
from nakuru.entities.components import Plain, At


def get_args():
    host = input("输入ip:")
    port = int(input("输入正向websocket端口:"))
    http_port = int(input("输入正向http端口:"))
    token = input("输入access_token(没有直接回车):")
    qid = int(input("群号:"))
    if token == "":
        token = None
    return host, port, http_port, token, qid


if __name__ == "__main__":
    args = get_args()

    app = CQHTTP(
        host=args[0],
        port=args[1],
        http_port=args[2],
        token=args[3]  # 可选，如果配置了 Access-Token
    )


    @app.receiver("GroupMessage")
    async def _(bot: CQHTTP, source: GroupMessage):
        global args
        if source.group_id != args[4]:
            return

        msg = (f"收到群{source.group_id}的信息：\n"
               f"    原始信息：{source.raw_message}，类型：{type(source.raw_message)}\n"
               f"    信息：{source.message}，类型：{type(source.message)}\n"
               f"    发送者：{source.sender}，类型：{type(source.sender)}\n"
               f"    发送者ID：{source.sender.user_id}，类型：{type(source.sender.user_id)}\n"
               f"    消息ID：{source.message_id}，类型：{type(source.message_id)}\n"
               f"    原始信息对象：{source}，类型：{type(source)}")

        print(msg)
        print(f"尝试发回消息...\n")
        await bot.sendGroupMessage(
            group_id=source.group_id,
            message=[At(source.sender), Plain("我收到了你的消息！")]
        )

    print("启动bot中...请确保支持onebot协议的机器人启动")
    app.run()
