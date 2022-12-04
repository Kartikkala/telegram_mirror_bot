import telegram
import threading
from time import sleep
from authorization import Authorization
from configLoader import LoadConfig
from time import time


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
    __latestUpdateDict = {}



    @classmethod                                                
    def __updateList(cls):
        return MyBot.__update_list

    @classmethod
    def lastServedUID(cls, updateDictionary):                     #Returns last served Update ID
        chatId = MyBot.__chatId(updateDictionary)
        chatId = str(chatId)
        if(chatId in MyBot.__lastServedUIDDict):
            return MyBot.__lastServedUIDDict[chatId]
        else:
            return 0

    @classmethod
    def readLastServedUID(cls):
        try:
            MyBot.__lastServedUIDDict = Authorization.readData(MyBot.__LastServedUIDfile, MyBot.__lastServedUIDDict)
        except:
            with open(MyBot.__LastServedUIDfile, 'w+') as LSUIDf:
                print("File created for first time use.")
    

    @classmethod
    def writeLastServedUID(cls):
        Authorization.writeData(MyBot.__LastServedUIDfile, MyBot.__lastServedUIDDict)
    

    @classmethod                                    #Returns JSON/Dictionary at a particular index in the Update list returned by Telegram API
    def __updateAtIndex(cls , index):
        update_list = MyBot.__updateList()
        return update_list[index]

    @classmethod                                    #Returns the length of the update list returned by Telegram API
    def List_Len(cls):
        return len(MyBot.__update_list)


    @classmethod                              
    def __latestUpdate(cls):
        try:                                 
            MyBot.__update_list = MyBot.__bot.getUpdates(offset = MyBot.lastServedUID(MyBot.__latestUpdateDict), timeout = 2)    
        except:                                    #When the last update Id file is NOT present and dictionary is NOT loaded from that file
             MyBot.__update_list = MyBot.__bot.getUpdates(timeout = 2)
    
    
    @classmethod                     
    def startUpdatePolling(cls):
        MyBot.__authorised_people = Authorization.readData('authorized_users.json',MyBot.__authorised_people)
        MyBot.readLastServedUID()
        print("Bot started...")
        while(1):
            MyBot.__latestUpdate()
            sleep(0.5)


    @classmethod
    def _memberInfo(cls, updateDictionary):                  #Extracts all info about user from chat (return type:dictinoary)
        return updateDictionary['message'].get('from')

    
    @classmethod
    def __chatInfo(cls, updateDictionary):
        return updateDictionary['message']['chat']

    @classmethod
    def __chatId(cls, updateDictionary):
        return MyBot.__chatInfo(updateDictionary)['id']

    @classmethod
    def __updateId(cls, updateDictionary):
        return updateDictionary['update_id']
    
    @classmethod
    def __messageInfo(cls, updateDictionary):
        return updateDictionary['message']

    @classmethod
    def __messageContent(cls, updateDictionary):
        latestMessageInfo = MyBot.__messageInfo(updateDictionary)
        latestMessageInfoKeys = latestMessageInfo.keys()
        if 'text' in latestMessageInfoKeys:
            return latestMessageInfo['text']
        else:
            return None

    @classmethod
    def __userId(cls, updateDictionary):
        return MyBot._memberInfo(updateDictionary)['id']

    @classmethod
    def __messageId(cls, updateDictionary):
        return MyBot.__messageInfo(updateDictionary)['message_id']

    @classmethod
    def __sentMessageId(cls, sentMessageDictionary):
        return sentMessageDictionary.get('message_id')
    
    @classmethod
    def __replyToMessage(cls, updateDictionary):
        latestMessageInfo = MyBot.__messageInfo(updateDictionary)
        if('reply_to_message' in latestMessageInfo):
            return latestMessageInfo.to_dict().get('reply_to_message')

        else:
            return None

    @classmethod
    def __replyMemberInfo(cls, updateDictionary):
        replyToMessageInfo = MyBot.__replyToMessage(updateDictionary)
        if(replyToMessageInfo == None):
            return None
        else:
            return replyToMessageInfo.to_dict().get('from')

    @classmethod
    def __replyMemberId(cls, updateDictionary):
        replyMemberInfo = MyBot.__replyMemberInfo(updateDictionary)
        if(replyMemberInfo == None):
            return None
        else:
            return replyMemberInfo['id']

    @classmethod
    def __updateLastServedUIDDictionary(cls, latestUpdateDictionary):
        MyBot.__lastServedUIDDict[str(MyBot.__chatId(latestUpdateDictionary))] = MyBot.__updateId(latestUpdateDictionary)
        return

    
    @classmethod                                    #Parse the latest Update dictionary from telegram API, extracts info to class variables
    def parseLatestUpdates(cls):                     
        while(1):
            while(MyBot.List_Len()==0):
                sleep(0.5)
            sleep(0.2)
        
            latestMessageIndex = MyBot.List_Len()-1
            updateJson = MyBot.__updateAtIndex(latestMessageIndex)
            MyBot.__latestUpdateDict = updateJson.to_dict()
            
            if(MyBot.__updateId(MyBot.__latestUpdateDict) == MyBot.lastServedUID(MyBot.__latestUpdateDict)):
                continue

            MyBot.__reply(MyBot.__latestUpdateDict)
            MyBot.__updateLastServedUIDDictionary(MyBot.__latestUpdateDict)
            MyBot.writeLastServedUID()
            print(f"Incoming: {MyBot.__userId(MyBot.__latestUpdateDict)}")
            print(f"Parsing...{MyBot.__updateId(MyBot.__latestUpdateDict)} | Message: {MyBot.__messageContent(MyBot.__latestUpdateDict)}",end = '\n')

    @classmethod                                    #Replies to a chat after checking if chat is authorised or not
    def __reply(cls, updateDictionary):                               
        if ( Authorization.isAuthorized(MyBot.__chatInfo(updateDictionary), MyBot.__userId(updateDictionary), MyBot.__authorised_people, MyBot.__owner_id) ):
            MyBot.__categorizeAnd__reply(updateDictionary)
            print(f"Is authorized.")
        else:
            print("Is not authorized")

    @classmethod                                    #Replies to a chat on the basis of Commands or normal chats
    def __categorizeAnd__reply(cls,updateDictionary):
        messageText = MyBot.__messageContent(updateDictionary)
        try:
            if(messageText[0] == '/'):
                MyBot.____replyToCommand(updateDictionary)
            else:
                MyBot.____replyToChat(updateDictionary)
        except:
            print("My man is sending stickers :)")


    @classmethod
    def ____replyToCommand(cls, updateDictionary):
        messageText = MyBot.__messageContent(updateDictionary)
        chatId = MyBot.__chatId(updateDictionary)
        messageID = MyBot.__messageId(updateDictionary)
        chatInfo = MyBot.__chatInfo(updateDictionary)
        userId = MyBot.__userId(updateDictionary)

        if('/start' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chatId, "Hello, Bot has been started!!!",reply_to_message_id = messageID)

        elif('/help' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chatId, "/help - Help command \n/start - Start the bot \n/mirror <Download link to the file>: Mirror a file", reply_to_message_id = messageID)

        elif('/mirror' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            MyBot.__bot.sendMessage(chatId, "This functionality has not been implemented yet!!!", reply_to_message_id = messageID)

        elif('/authstatus' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            Auth_status = Authorization.auth_status(chatInfo, MyBot.__replyMemberId(updateDictionary), MyBot.__authorised_people, MyBot.__owner_id)
            MyBot.__bot.sendMessage(chatId, Auth_status, reply_to_message_id = messageID)

        elif('/authorize' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            if MyBot.__replyMemberInfo() == None:
                MyBot.__bot.sendMessage(chatId, "Reply to someone's message to authorize him.", reply_to_message_id = messageID)
            else:
                Authorization_status = Authorization.authorize(chatInfo, MyBot.__replyMemberId(updateDictionary), MyBot.__authorised_people, MyBot.__owner_id, userId)
                MyBot.__bot.sendMessage(chatId, Authorization_status, reply_to_message_id = messageID)
        
        elif('/unauthorize' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            if MyBot.__replyMemberInfo() == None:
                MyBot.__bot.sendMessage(chatId, "Reply to someone's message to unauthorize him.", reply_to_message_id = messageID)
            else:
                Authorization_status = Authorization.unauthorize(chatInfo, MyBot.__replyMemberId(updateDictionary), MyBot.__authorised_people, MyBot.__owner_id, userId)
                MyBot.__bot.sendMessage(chatId, Authorization_status, reply_to_message_id = messageID)

        elif('/ping' in messageText):
            MyBot.__bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            startTime = int(time() * 1000)
            sentMessage = MyBot.__bot.sendMessage(chatId, "Calculating latency...", reply_to_message_id = messageID)
            endTime = int(time() * 1000)
            diffenceInTime = endTime-startTime
            sentMessage = sentMessage.to_dict()
            sentMessageID = MyBot.__sentMessageId(sentMessage)
            MyBot.__bot.editMessageText(chat_id=chatId,message_id=sentMessageID,text=f'latency: {diffenceInTime} ms')
            
        

    @classmethod
    def ____replyToChat(cls, updateDictionary):
        pass



thread1 = threading.Thread(target = MyBot.startUpdatePolling)
thread2 = threading.Thread(target = MyBot.parseLatestUpdates)


thread1.start()
thread2.start()


    
