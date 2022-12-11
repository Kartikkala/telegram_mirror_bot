import base.bot
import base.authorization
import telegram
import time


class Commands:
    @classmethod
    def replyToCommand(cls, updateDictionary):
        messageText = base.bot.MyBot.messageContent(updateDictionary)
        chatId = base.bot.MyBot.chatId(updateDictionary)
        messageID = base.bot.MyBot.messageId(updateDictionary)
        chatInfo = base.bot.MyBot.chatInfo(updateDictionary)
        userId = base.bot.MyBot.userId(updateDictionary)
        repliedMessageUserID = base.bot.MyBot.replyMemberId(updateDictionary)

        if('/start' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            base.bot.MyBot.bot.sendMessage(chatId, "Hello, Bot has been started!!!",reply_to_message_id = messageID)

        elif('/help' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            base.bot.MyBot.bot.sendMessage(chatId, "/help - Help command \n/start - Start the bot \n/mirror <Download link to the file>: Mirror a file", reply_to_message_id = messageID)

        elif('/mirror' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            base.bot.MyBot.bot.sendMessage(chatId, "This functionality has not been implemented yet!!!", reply_to_message_id = messageID)

        elif('/authstatus' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            if base.bot.MyBot.replyMemberInfo(updateDictionary) == None:
                base.bot.MyBot.bot.sendMessage(chatId, "Reply to someone's message to check authorization status.", reply_to_message_id = messageID)
            else:
                Auth_status = base.authorization.Authorization.auth_status(chatInfo, base.bot.MyBot.replyMemberId(updateDictionary), base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id)
                base.bot.MyBot.bot.sendMessage(chatId, Auth_status, reply_to_message_id = messageID)
            

        elif('/authorize' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            if base.bot.MyBot.replyMemberInfo(updateDictionary) == None:
                base.bot.MyBot.bot.sendMessage(chatId, "Reply to someone's message to authorize him.", reply_to_message_id = messageID)
            else:
                Authorization_status = base.authorization.Authorization.authorize(chatInfo, repliedMessageUserID, base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id, userId)
                base.bot.MyBot.bot.sendMessage(chatId, Authorization_status, reply_to_message_id = messageID)
        
        elif('/unauthorize' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            if base.bot.MyBot.replyMemberInfo(updateDictionary) == None:
                base.bot.MyBot.bot.sendMessage(chatId, "Reply to someone's message to unauthorize him.", reply_to_message_id = messageID)
            else:
                Authorization_status = base.authorization.Authorization.unauthorize(chatInfo, repliedMessageUserID, base.bot.MyBot.authorised_people, base.bot.MyBot.owner_id, userId)
                base.bot.MyBot.bot.sendMessage(chatId, Authorization_status, reply_to_message_id = messageID)

        elif('/ping' in messageText):
            base.bot.MyBot.bot.sendChatAction(chat_id = chatId, action = telegram.ChatAction.TYPING)
            startTime = int(time() * 1000)
            sentMessage = base.bot.MyBot.bot.sendMessage(chatId, "Calculating latency...", reply_to_message_id = messageID)
            endTime = int(time() * 1000)
            diffenceInTime = endTime-startTime
            sentMessage = sentMessage.to_dict()
            sentMessageID = base.bot.MyBot.sentMessageId(sentMessage)
            base.bot.MyBot.bot.editMessageText(chat_id=chatId,message_id=sentMessageID,text=f'latency: {diffenceInTime} ms')