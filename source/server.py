import time
# 每秒向log.txt中写入计数作为模拟输出
# 此.py相当于mc服务器的服务端，将工作日志输出至此
# 日志格式 [11:48:22] [Server thread/INFO]: <Sorobot> Test
log_path = './logs/latest.log'
count = 0
print("I'm writing to latest log...")
while(1):
    with open(log_path, 'a') as f:
        f.write("[11:48:22] [Server thread/INFO]: <Sorobot> Test" + str(count) + '\n')
        count += 1
    time.sleep(3)
