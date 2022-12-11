import telegram
import threading
from time import sleep
from base.authorization import Authorization
from base.configLoader import LoadConfig
import base.commands
from time import time
import os


class MyBot:
    __configFilePath = os.path.join(os.getcwd(),"config.yml")
    __LastServedUIDfile = os.path.join(os.getcwd(),"bot/base/resourceFiles/LSUID.json")
    _authorized_file = os.path.join(os.getcwd(),"bot/base/resourceFiles/authorized_users.json")
    __bot_token= LoadConfig.BotToken(__configFilePath)
    __update_list = []
    __lastServedUIDDict = {}
    bot = telegram.Bot(__bot_token)
    authorised_people = {-1001358301916:[1239653417,1972073012]}

    #Chat info

    owner_id = LoadConfig.ownerId(__configFilePath)
    __latestUpdateDict = {}



    @classmethod                                                
    def __updateList(cls):
        return MyBot.__update_list

    @classmethod
    def lastServedUID(cls, updateDictionary):                     #Returns last served Update ID
        chatId = MyBot.chatId(updateDictionary)
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
            MyBot.__update_list = MyBot.bot.getUpdates(offset = MyBot.lastServedUID(MyBot.__latestUpdateDict), timeout = 2)    
        except:                                    #When the last update Id file is NOT present and dictionary is NOT loaded from that file
             MyBot.__update_list = MyBot.bot.getUpdates(timeout = 2)
    
    
    @classmethod                     
    def startUpdatePolling(cls):
        MyBot.authorised_people = Authorization.readData(MyBot._authorized_file,MyBot.authorised_people)
        MyBot.readLastServedUID()
        print("Bot started...")
        while(1):
            MyBot.__latestUpdate()
            sleep(0.5)


    @classmethod
    def memberInfo(cls, updateDictionary):                  #Extracts all info about user from chat (return type:dictinoary)
        if 'message' in updateDictionary:
            return updateDictionary['message'].get('from')
        else:
            return updateDictionary['edited_message'].get('from')

    
    @classmethod
    def chatInfo(cls, updateDictionary):
        if 'message' in updateDictionary:
            return updateDictionary['message']['chat']
        else:
            return updateDictionary['edited_message']['chat']

    @classmethod
    def chatId(cls, updateDictionary):
        return MyBot.chatInfo(updateDictionary)['id']

    @classmethod
    def updateId(cls, updateDictionary):
        return updateDictionary['update_id']
    
    @classmethod
    def messageInfo(cls, updateDictionary):
        if 'message' in updateDictionary:
            return updateDictionary['message']
        else:
            return updateDictionary['edited_message']

    @classmethod
    def messageContent(cls, updateDictionary):
        latestMessageInfo = MyBot.messageInfo(updateDictionary)
        latestMessageInfoKeys = latestMessageInfo.keys()
        if 'text' in latestMessageInfoKeys:
            return latestMessageInfo['text']
        else:
            return None

    @classmethod
    def userId(cls, updateDictionary):
        return MyBot.memberInfo(updateDictionary)['id']

    @classmethod
    def messageId(cls, updateDictionary):
        return MyBot.messageInfo(updateDictionary)['message_id']

    @classmethod
    def sentMessageId(cls, sentMessageDictionary):
        return sentMessageDictionary.get('message_id')
    
    @classmethod
    def replyToMessage(cls, updateDictionary):
        latestMessageInfo = MyBot.messageInfo(updateDictionary)
        if('reply_to_message' in latestMessageInfo):
            return latestMessageInfo.get('reply_to_message')

        else:
            return None

    @classmethod
    def replyMemberInfo(cls, updateDictionary):
        replyToMessageInfo = MyBot.replyToMessage(updateDictionary)
        if(replyToMessageInfo == None):
            return None
        else:
            return replyToMessageInfo.get('from')

    @classmethod
    def replyMemberId(cls, updateDictionary):
        replyMemberInfo = MyBot.replyMemberInfo(updateDictionary)
        if(replyMemberInfo == None):
            return None
        else:
            return replyMemberInfo['id']

    @classmethod
    def __updateLastServedUIDDictionary(cls, latestUpdateDictionary):
        MyBot.__lastServedUIDDict[str(MyBot.chatId(latestUpdateDictionary))] = MyBot.updateId(latestUpdateDictionary)
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
            
            if(MyBot.updateId(MyBot.__latestUpdateDict) == MyBot.lastServedUID(MyBot.__latestUpdateDict)):
                continue

            MyBot.__reply(MyBot.__latestUpdateDict)
            MyBot.__updateLastServedUIDDictionary(MyBot.__latestUpdateDict)
            MyBot.writeLastServedUID()
            print(f"Incoming: {MyBot.userId(MyBot.__latestUpdateDict)}")
            print(f"Parsing...{MyBot.updateId(MyBot.__latestUpdateDict)} | Message: {MyBot.messageContent(MyBot.__latestUpdateDict)}",end = '\n')

    @classmethod                                    #Replies to a chat after checking if chat is authorised or not
    def __reply(cls, updateDictionary):                               
        if ( Authorization.isAuthorized(MyBot.chatInfo(updateDictionary), MyBot.userId(updateDictionary), MyBot.authorised_people, MyBot.owner_id) ):
            MyBot.__categorizeAnd__reply(updateDictionary)
            print(f"Is authorized.")
        else:
            print("Is not authorized")

    @classmethod                                    #Replies to a chat on the basis of Commands or normal chats
    def __categorizeAnd__reply(cls,updateDictionary):
        messageText = MyBot.messageContent(updateDictionary)
        try:
            if(messageText[0] == '/'):
                base.commands.Commands.replyToCommand(updateDictionary)
            else:
                    MyBot.____replyToChat(updateDictionary)
        except:
            print("My man is sending stickers :)")


            
        

    @classmethod
    def ____replyToChat(cls, updateDictionary):
        pass

