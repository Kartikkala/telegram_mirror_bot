import telegram
import threading
from collections import deque
from time import sleep



class MyBot:
    __bot_token = "5941804301:AAFptut_3g30maH6Ed1XAuWs7cQKfOK_fK8"
    __update_list = []
    __bot = telegram.Bot(__bot_token)
    __lastServedUID = 0

    @classmethod
    def getULIST(cls):
        return MyBot.__update_list

    @classmethod
    def getLastServedUID(cls):
        return MyBot.__lastServedUID

    @classmethod
    def getJSON(cls , index):
        update_list = MyBot.getULIST()
        return update_list[index]

    @classmethod
    def List_Len(cls):
        return len(MyBot.__update_list)


    @classmethod
    def __latestUpdate(cls):
        MyBot.__update_list = MyBot.__bot.getUpdates(offset = MyBot.getLastServedUID(), timeout = 2)       # List with JSON
    
    
    @classmethod
    def startUpdatePolling(cls):
        while(1):
            MyBot.__latestUpdate()
            # print("Checking for updates...",end = '\n')
            # print(f" Latest UID: {MyBot.__update_list[MyBot.List_Len()-1]['update_id']}", end = '\t')
            sleep(0.5)
    
    @classmethod
    def parse(cls):
        while(1):
            while(MyBot.List_Len()==0):
                sleep(0.5)
            sleep(0.2)
            json = MyBot.getJSON(MyBot.List_Len()-1)
            UpdateID = json['update_id']
            if(UpdateID == MyBot.getLastServedUID()):
                continue
            chat_id = json['message']['chat']['id']
            message = json['message']['text']
            MyBot.categorizeAndReply(chat_id, message)
            MyBot.__lastServedUID = UpdateID
            print(f"Replied to: {chat_id} | His message: {message}")
            print(f"Parsing...{UpdateID} | Last served UID: {MyBot.getLastServedUID()}",end = '\n')


    @classmethod
    def categorizeAndReply(cls,chat_id,message):
        if(message[0] == '/'):
            MyBot.replyToCommand(chat_id, message)
        else:
            MyBot.replyToChat(chat_id, message)

    @classmethod
    def replyToCommand(cls, chat_id, message):
        if(message == '/start' or message == "/start"):
            MyBot.__bot.sendMessage(chat_id, "Hello, Bot has been started!!!")
        

    @classmethod
    def replyToChat(cls, chat_id, message):
        pass


thread1 = threading.Thread(target = MyBot.startUpdatePolling)
thread2 = threading.Thread(target = MyBot.parse)


thread1.start()
thread2.start()


# bot_token = "5941804301:AAFptut_3g30maH6Ed1XAuWs7cQKfOK_fK8"
# bot = telegram.Bot(bot_token)





# updates = bot.getUpdates(200739451)
# latest_update_id = updates
# print(*latest_update_id,end ="\n\n")
    
