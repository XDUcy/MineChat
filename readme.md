# MineChat debug version

1. 运行 `server.py` 扮演服务端，它会定时（默认三秒）向日志文件 `latest.log` 中写入玩家消息格式的内容
2. 运行 `listener.py` 作为监听，它会实例化一个 listener，每当日志文件有玩家消息写入时，抛出提示
3. More TODO...
