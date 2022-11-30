import telegram
import threading
from time import sleep



class MyBot:
    __bot_token = "5941804301:AAFptut_3g30maH6Ed1XAuWs7cQKfOK_fK8"
    __update_list = []
    __bot = telegram.Bot(__bot_token)
    __lastServedUID = 0
    __authorised_people = {-1001358301916:[1239653417,1972073012]}
    __owner_id = 1239653417
    __chat_info = {}
    __message = ''
    __user_id = 0


    @classmethod
    def _getMemberInfo(cls, index):
        return MyBot.__update_list[index]['message'].to_dict().get('from')


    @classmethod
    def _getULIST(cls):
        return MyBot.__update_list

    @classmethod
    def _getLastServedUID(cls):
        return MyBot.__lastServedUID

    @classmethod
    def _getJSON(cls , index):
        update_list = MyBot._getULIST()
        return update_list[index]

    @classmethod
    def List_Len(cls):
        return len(MyBot.__update_list)


    @classmethod
    def __latestUpdate(cls):
        MyBot.__update_list = MyBot.__bot.getUpdates(offset = MyBot._getLastServedUID(), timeout = 2)       # List with JSON
    
    
    @classmethod
    def startUpdatePolling(cls):
        while(1):
            MyBot.__latestUpdate()
            sleep(0.5)


    @classmethod
    def approve(cls):
        pass
    
    @classmethod
    def parse(cls):
        while(1):
            while(MyBot.List_Len()==0):
                sleep(0.5)
            sleep(0.2)
            latest_message = MyBot.List_Len()-1
            json = MyBot._getJSON(latest_message)
            UpdateID = json['update_id']
            if(UpdateID == MyBot._getLastServedUID()):
                continue
            MyBot.__chat_info = json['message']['chat']
            MyBot.__message = json['message']['text']
            MyBot.__user_id = MyBot._getMemberInfo(latest_message)['id']

            MyBot.__reply()
            MyBot.__lastServedUID = UpdateID
            print(f"Incoming: {MyBot.__user_id}")
            print(f"Parsing...{UpdateID} | Message: {MyBot.__message} | Last served UID: {MyBot._getLastServedUID()}",end = '\n')
        
    @classmethod
    def __isGroupChat(cls, chat_info):
        if(chat_info['type'] == 'private'):
            return False
        else:
            return True
    
    @classmethod 
    def __isAuthorized(cls, chat_info, user_id):
        if(MyBot.__isGroupChat(chat_info)):
            try:
                allowedIds = MyBot.__authorised_people[chat_info['id']]
                if user_id in allowedIds:
                    return True
                else:
                    return False
            except:
                print("Some error occured while checking groups!!!")

        else:
            if(user_id == MyBot.__owner_id):
                return True
            else:
                return False

    @classmethod
    def __reply(cls):
        if(MyBot.__isAuthorized(MyBot.__chat_info,MyBot.__user_id)):
            MyBot.__categorizeAnd__reply(MyBot.__chat_info['id'],MyBot.__message)
            print(f"Is authorized, message: {MyBot.__message}")
        else:
            print("Is not authorized")
            pass

    @classmethod
    def __categorizeAnd__reply(cls,chat_id,message):
        if(message[0] == '/'):
            MyBot.____replyToCommand(chat_id, message)
        else:
            MyBot.____replyToChat(chat_id, message)

    @classmethod
    def ____replyToCommand(cls, chat_id, message):
        if(message == '/start' or message == "/start"):
            MyBot.__bot.sendMessage(chat_id, "Hello, Bot has been started!!!")
        elif(message == '/help'):
            MyBot.__bot.sendMessage(chat_id, "/help - Help command \n/start - Start the bot \n/mirror <Download link to the file>: Mirror a file")
        elif(message == '/mirror'):
            MyBot.__bot.sendMessage(chat_id, "This functionality has not been implemented yet!!!")
        

    @classmethod
    def ____replyToChat(cls, chat_id, message):
        pass


thread1 = threading.Thread(target = MyBot.startUpdatePolling)
thread2 = threading.Thread(target = MyBot.parse)


thread1.start()
thread2.start()


    
