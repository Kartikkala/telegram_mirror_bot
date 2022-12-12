import base.bot
import base.authorization
import telegram
from time import time
from utils.download_utils.downloader import Download
import multiprocessing

MAX_LOOP = 10


class Commands:

    updateDictionary = {}        #To make sure that this is never empty
    messageText = ''
    chatId = 0
    messageID = 0
    chatInfo = {}
    userId = 0
    repliedMessageUserID = 0


    @classmethod
    def updateClassInformation(cls, newUpdateDictionary):
        cls.updateDictionary = newUpdateDictionary
        cls.messageText = base.bot.MyBot.messageContent(cls.updateDictionary)
        cls.chatId = base.bot.MyBot.chatId(cls.updateDictionary)
        cls.messageID = base.bot.MyBot.messageId(cls.updateDictionary)
        cls.chatInfo = base.bot.MyBot.chatInfo(cls.updateDictionary)
        cls.userId = base.bot.MyBot.userId(cls.updateDictionary)
        cls.repliedMessageUserID = base.bot.MyBot.replyMemberId(cls.updateDictionary)
        return


    @classmethod
    def sendDownloadInfo(cls, gid, sentMessage_ID, chat_Id):
         while(1):
                try:
                    base.bot.MyBot.bot.editMessageText(chat_id=chat_Id,message_id=sentMessage_ID,text=f"{Download.getSpeed(Download.getDownload(gid))} GiD: {gid}")
                    time.sleep(3)
                except:
                    pass

    @classmethod
    def authstatus(cls):
        base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
        if base.bot.MyBot.replyMemberInfo(cls.updateDictionary) == None:
            base.bot.MyBot.bot.sendMessage(cls.chatId, "Reply to someone's message to check authorization status.", reply_to_message_id = cls.messageID)
        else:
            Auth_status = base.authorization.Authorization.auth_status(cls.chatInfo, base.bot.MyBot.replyMemberId(cls.updateDictionary), base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id)
            base.bot.MyBot.bot.sendMessage(cls.chatId, Auth_status, reply_to_message_id = cls.messageID)

    @classmethod
    def authorize(cls):
        base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
        if base.bot.MyBot.replyMemberInfo(cls.updateDictionary) == None:
            base.bot.MyBot.bot.sendMessage(cls.chatId, "Reply to someone's message to authorize him.", reply_to_message_id = cls.messageID)
        else:
            Authorization_status = base.authorization.Authorization.authorize(cls.chatInfo, cls.repliedMessageUserID, base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id, cls.userId)
            base.bot.MyBot.bot.sendMessage(cls.chatId, Authorization_status, reply_to_message_id = cls.messageID)


    @classmethod
    def unauthorize(cls):
        base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
        if base.bot.MyBot.replyMemberInfo(cls.updateDictionary) == None:
            base.bot.MyBot.bot.sendMessage(cls.chatId, "Reply to someone's message to unauthorize him.", reply_to_message_id = cls.messageID)
        else:
            Authorization_status = base.authorization.Authorization.unauthorize(cls.chatInfo, cls.repliedMessageUserID, base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id, cls.userId)
            base.bot.MyBot.bot.sendMessage(cls.chatId, Authorization_status, reply_to_message_id = cls.messageID)

    @classmethod
    def ping(cls):
        base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
        startTime = int(time() * 1000)
        sentMessage = base.bot.MyBot.bot.sendMessage(cls.chatId, "Calculating latency...", reply_to_message_id = cls.messageID)
        endTime = int(time() * 1000)
        diffenceInTime = endTime-startTime
        sentMessage = sentMessage.to_dict()
        sentMessageID = base.bot.MyBot.sentMessageId(sentMessage)
        base.bot.MyBot.bot.editMessageText(chat_id=cls.chatId,message_id=sentMessageID,text=f'latency: {diffenceInTime} ms')



    @classmethod
    def replyToCommand(cls, newUpdateDictionary):
        cls.updateClassInformation(newUpdateDictionary)
        sentMessage = ''
        sentMessageID = 0
        downloadInfoProcess = multiprocessing.Process()        #For making multiprocessing variable accessible by all conditions

        if('/start' in cls.messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
            base.bot.MyBot.bot.sendMessage(cls.chatId, "Hello, Bot has been started!!!",reply_to_message_id = cls.messageID)

        elif('/help' in cls.messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = cls.chatId, action = telegram.ChatAction.TYPING)
            base.bot.MyBot.bot.sendMessage(cls.chatId, "/help - Help command \n/start - Start the bot \n/mirror <Download link to the file>: Mirror a file", reply_to_message_id = cls.messageID)

        elif('/authstatus' in cls.messageText):
            cls.authstatus()
            
        elif('/authorize' in cls.messageText):
           cls.authorize()
        
        elif('/unauthorize' in cls.messageText):
           cls.unauthorize()

        elif('/ping' in cls.messageText):
            cls.ping()

        elif('/mirror' in cls.messageText):

            link = ''
            i=len('/mirror')+1
            if(i<len(cls.messageText)):
                while(cls.messageText[i] == ' ' and i < i+MAX_LOOP):
                    i+=1

            for i in range(i, len(cls.messageText)):
                link += str(cls.messageText[i])

            newDownloadGid = Download.addDownload(link)

            sentMessage = base.bot.MyBot.bot.sendMessage(cls.chatId, f"Speed: {0} b/S GiD: {newDownloadGid}", reply_to_message_id = cls.messageID)
            sentMessage = sentMessage.to_dict()
            sentMessageID = base.bot.MyBot.sentMessageId(sentMessage)

            print(newDownloadGid)

            downloadInfoProcess = multiprocessing.Process(target=cls.sendDownloadInfo, args=(newDownloadGid, sentMessageID, cls.chatId,))


            downloadInfoProcess.start()


        elif('/cancel' in cls.messageText):

            gid = ''
            i=len('/cancel')+1

            if(i<len(cls.messageText)):
                while(cls.messageText[i] == ' ' and i < i+MAX_LOOP):
                    i+=1

            for i in range(i, len(cls.messageText)):
                gid += str(cls.messageText[i])

            if Download.cancelDownload(gid, downloadInfoProcess):
                base.bot.MyBot.bot.deleteMessage(chat_id = cls.chatId, message_id = sentMessageID)
                base.bot.MyBot.bot.sendMessage(cls.chatId, f"Download with gid: {newDownloadGid} cancelled", reply_to_message_id = cls.messageID)

            else:
                base.bot.MyBot.bot.sendMessage(cls.chatId, "Some error occured while closing download info thread...", reply_to_message_id = cls.messageID)
