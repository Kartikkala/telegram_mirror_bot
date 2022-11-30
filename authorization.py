class Authorization:
    @classmethod
    def isGroupChat(cls, chat_info):                    #Returns true of chat is a group chat, else returns false
        if(chat_info['type'] == 'private'):
            return False
        else:
            return True

    @classmethod                                        #Returns true if sender is authorized on the basis of user_id
    def isAuthorized(cls, chat_info, user_id, allowedDictinoary_List, owner_id):
        if(Authorization.isGroupChat(chat_info)):
            try:
                allowedIds = allowedDictinoary_List[chat_info['id']]
                if user_id in allowedIds:
                    return True
                else:
                    return False
            except:
                print("Some error occured while checking groups!!!")

        else:
            if(user_id == owner_id):
                return True
            else:
                return False

    @classmethod
    def approve(cls):
        pass

