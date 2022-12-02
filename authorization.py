import json
class Authorization:
    _authorized_file = 'authorized_users.json'
    @classmethod
    def isGroupChat(cls, chat_info):                    #Returns true of chat is a group chat, else returns false
        if(chat_info['type'] == 'private'):
            return False
        else:
            return True


    @classmethod
    def readData(cls, filename, dictionary):
        try:
            with open (filename, 'r') as filehehe:
                return json.load(filehehe)
        except:
            Authorization.writeData(filename, dictionary)
            print("\nFirst write of JSON data successful!!!")
            return Authorization.readData(filename, dictionary)

    @classmethod
    def writeData(cls, filename, dictionary):
        try:
            with open(filename, 'w+') as filehehe:
                json.dump(dictionary, filehehe)
        except:
            print("Write error!!!", end = '\n')
            return None

    @classmethod                                        #Returns true if sender is authorized on the basis of user_id
    def isAuthorized(cls, chat_info, user_id, allowedDictinoary_List, owner_id):
        chat_id = str(chat_info['id'])

        if(Authorization.isGroupChat(chat_info)):
            try:
                Authorization.readData(Authorization._authorized_file,allowedDictinoary_List)

                try:                                                       #If group not available in dictionary, then add that group and add owner to group list
                    allowedIds = allowedDictinoary_List[chat_id]
                except:
                    allowedDictinoary_List[chat_id] = []
                    allowedDictinoary_List[chat_id].append(owner_id)
                    Authorization.writeData(Authorization._authorized_file, allowedDictinoary_List)


                if user_id == owner_id:
                    return True
                elif user_id in allowedIds:
                    return True
                else:
                    return False
            except:
                print("Some error occured while checking groups!!!")
                print(allowedDictinoary_List)

        else:
            if(user_id == owner_id):
                return True
            else:
                return False


    @classmethod                                                #For /auth_status command                                            
    def auth_status(cls, chat_info, user_id, allowedDictinoary_List, owner_id ):
        if(Authorization.isAuthorized(chat_info, user_id, allowedDictinoary_List, owner_id)):
            return "This person is authorized to use this bot."
        else:
            return "This person is not authorized to use this bot yet."
        


    @classmethod
    def authorize(cls,chat_info, target_user_id, allowedDictionary_List, owner_id, user_id):
        chat_id = str(chat_info['id'])


        if(user_id == owner_id):
            if(Authorization.isAuthorized(chat_info,user_id,allowedDictionary_List,owner_id)):
                return "This person is already authorized"
            else:
                Authorization.readData(Authorization._authorized_file, allowedDictionary_List)
                allowedDictionary_List[chat_id].append(target_user_id)
                Authorization.writeData(Authorization._authorized_file,allowedDictionary_List)
                return "This person is now authorized"
        else:
            return "Haha, Nice try kid!!!"
    
    @classmethod
    def unauthorize(cls,chat_info, target_user_id, allowedDictionary_List, owner_id ,user_id):
        chat_id= str(chat_info['id'])

        if(user_id == owner_id):
            if(Authorization.isAuthorized(chat_info,user_id,allowedDictionary_List,owner_id)):
                Authorization.readData(Authorization._authorized_file, allowedDictionary_List)
                allowedDictionary_List[chat_id].remove(target_user_id)
                Authorization.writeData(Authorization._authorized_file, allowedDictionary_List)
                return "This person in now unauthorized"
            
            else:
                return "This person is already unauthorized"
        else:
            return "Haha, Nice try kid!!!"



