from base import MyBot
import threading

thread1 = threading.Thread(target = MyBot.startUpdatePolling)
thread2 = threading.Thread(target = MyBot.parseLatestUpdates)


thread1.start()
thread2.start()
