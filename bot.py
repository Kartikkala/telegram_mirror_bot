import telegram
import threading
from time import sleep
from authorization import Authorization
from configLoader import LoadConfig


class MyBot:
    __configFilePath = 'config.yml'
    __LastServedUIDfile = 'LSUID.json'
    __bot_token= LoadConfig.BotToken(__configFilePath)
    __update_list = []
    __bot = telegram.Bot(__bot_token)
    __lastServedUIDDict = {}
    __authorised_people = {-1001358301916:[1239653417,1972073012]}

    #Chat info

    __owner_id = LoadConfig.ownerId(__configFilePath)
    __chat_info = {}
    __message = ''
    __MessageId = 0
    __repliedMessage ={}
    __user_id = 0


    @classmethod
    def _getMemberInfo(cls, index):                  #Extracts all info about user from chat (return type:dictinoary)
        return MyBot.__update_list[index]['message'].to_dict().get('from')

    @classmethod
    def __getChatId(cls, format=1):
        if format ==1:
            return str(MyBot.__chat_info['id'])
        else:
            return int(MyBot.__chat_info['id'])
    
    
    @classmethod
    def _getReplyMemberInfo(cls):
        try:
            return MyBot.__repliedMessage.to_dict().get('reply_to_message').get('from')
        except:
            return None


    @classmethod                                                
    def _getULIST(cls):
        return MyBot.__update_list

    @classmethod
    def _getLastServedUID(cls, chatId):                     #Returns last served Update ID
        try:
            return MyBot.__lastServedUIDDict[chatId]
        except:
            return 0

    @classmethod
    def readLastServedUID(cls):
        try:
            MyBot.__lastServedUIDDict = Authorization.readData(MyBot.__LastServedUIDfile, MyBot.__lastServedUIDDict)
        except:
            with open(MyBot.__LastServedUIDfile, 'w+') as LSUIDf:
                print("File created for first time use.")
    

    @classmethod
    def writeLastServedUID(cls,UpdateId,chatId):
        Authorization.writeData(MyBot.__LastServedUIDfile, MyBot.__lastServedUIDDict)
    

    @classmethod                                    #Returns JSON/Dictionary at a particular index in the Update list returned by Telegram API
    def _getJSON(cls , index):
        update_list = MyBot._getULIST()
        return update_list[index]

    @classmethod                                    #Returns the length of the update list returned by Telegram API
    def List_Len(cls):
        return len(MyBot.__update_list)


    @classmethod                              
    def __latestUpdate(cls):
        try:                                 
            MyBot.__update_list = MyBot.__bot.getUpdates(offset = MyBot._getLastServedUID(MyBot.__getChatId(1)), timeout = 2)    
        except:                                     #When the last update Id file is NOT present and dictionary is NOT loaded from that file
             MyBot.__update_list = MyBot.__bot.getUpdates(timeout = 2)
    
    
    @classmethod                     
    def startUpdatePolling(cls):
        MyBot.__authorised_people = Authorization.readData('authorized_users.json',MyBot.__authorised_people)
        MyBot.readLastServedUID()
        print("Bot started...")
        while(1):
            MyBot.__latestUpdate()
            sleep(0.5)


    
    @classmethod                                    #Parse the latest Update dictionary from telegram API, extracts info to class variables
    def parse(cls):                     
        while(1):
            while(MyBot.List_Len()==0):
                sleep(0.5)
            sleep(0.2)
            latest_message = MyBot.List_Len()-1
            json = MyBot._getJSON(latest_message)
            UpdateID = json['update_id']
            if json['message'] != None:
                MyBot.__chat_info = json['message']['chat']
                MyBot.__message = json['message']['text']
                try:
                    MyBot.__messageEntities = json['message'].to_dict().get('entities')[0]
                except:
                    MyBot.__messageEntities = None
                MyBot.__user_id = MyBot._getMemberInfo(latest_message)['id']
                MyBot.__MessageId = json['message']['message_id']
                MyBot.__repliedMessage = json['message']
            else:
                continue
            
            if(UpdateID == MyBot._getLastServedUID(MyBot.__getChatId(1))):
                continue

            MyBot.__reply()
            MyBot.__lastServedUIDDict[MyBot.__getChatId(1)] = UpdateID
            MyBot.writeLastServedUID(UpdateID, MyBot.__chat_info['id'])
            print(f"Incoming: {MyBot.__user_id}")
            print(f"Parsing...{UpdateID} | Message: {MyBot.__message} | Last served UID: {MyBot._getLastServedUID(MyBot.__getChatId(1))}",end = '\n')

    @classmethod                                    #Replies to a chat after checking if chat is authorised or not
    def __reply(cls):                               
        if ( Authorization.isAuthorized (MyBot.__chat_info, MyBot.__user_id, MyBot.__authorised_people, MyBot.__owner_id) ):
            MyBot.__categorizeAnd__reply(MyBot.__chat_info['id'],MyBot.__message)
            print(f"Is authorized, message: {MyBot.__message}")
        else:
            print("Is not authorized")

    @classmethod                                    #Replies to a chat on the basis of Commands or normal chats
    def __categorizeAnd__reply(cls,chat_id,message):
        try:
            if(message[0] == '/'):
                MyBot.____replyToCommand(chat_id, message)
            else:
                MyBot.____replyToChat(chat_id, message)
        except:
            print("My man is sending stickers :)")


    @classmethod
    def ____replyToCommand(cls, chat_id, message):
        if('/start' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chat_id, "Hello, Bot has been started!!!",reply_to_message_id = MyBot.__MessageId)

        elif('/help' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chat_id, "/help - Help command \n/start - Start the bot \n/mirror <Download link to the file>: Mirror a file", reply_to_message_id = MyBot.__MessageId)

        elif('/mirror' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chat_id, "This functionality has not been implemented yet!!!", reply_to_message_id = MyBot.__MessageId)

        elif('/authstatus' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            Auth_status = Authorization.auth_status(MyBot.__chat_info, MyBot._getReplyMemberInfo()['id'], MyBot.__authorised_people, MyBot.__owner_id)
            MyBot.__bot.sendMessage(chat_id, Auth_status, reply_to_message_id = MyBot.__MessageId)

        elif('/authorize' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            if MyBot._getReplyMemberInfo() == None:
                print(MyBot.__repliedMessage)
                MyBot.__bot.sendMessage(chat_id, "Reply to someone's message to authorize him.", reply_to_message_id = MyBot.__MessageId)
            else:
                Authorization_status = Authorization.authorize(MyBot.__chat_info, MyBot._getReplyMemberInfo()['id'], MyBot.__authorised_people, MyBot.__owner_id, MyBot.__user_id)
                MyBot.__bot.sendMessage(chat_id, Authorization_status, reply_to_message_id = MyBot.__MessageId)
        
        elif('/unauthorize' in message):
            MyBot.__bot.sendChatAction(chat_id = MyBot.__chat_info['id'], action = telegram.ChatAction.TYPING)
            if MyBot._getReplyMemberInfo() == None:
                MyBot.__bot.sendMessage(chat_id, "Reply to someone's message to unauthorize him.", reply_to_message_id = MyBot.__MessageId)
            else:
                Authorization_status = Authorization.unauthorize(MyBot.__chat_info, MyBot._getReplyMemberInfo()['id'], MyBot.__authorised_people, MyBot.__owner_id, MyBot.__user_id)
                MyBot.__bot.sendMessage(chat_id, Authorization_status, reply_to_message_id = MyBot.__MessageId)
        

    @classmethod
    def ____replyToChat(cls, chat_id, message):
        pass



thread1 = threading.Thread(target = MyBot.startUpdatePolling)
thread2 = threading.Thread(target = MyBot.parse)


thread1.start()
thread2.start()


    
