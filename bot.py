import telegram
import threading
from collections import deque
from time import sleep



class MyBot:
    __bot_token = "5941804301:AAFptut_3g30maH6Ed1XAuWs7cQKfOK_fK8"
    __update_ids = deque()
    __bot = telegram.Bot(__bot_token)
    __lastServedUID = 0

    @classmethod
    def __latestUpdate(cls):
        updates = MyBot.__bot.getUpdates()
        latest_update_id = updates[len(updates)-1]['update_id']
    
        if(len(MyBot.__update_ids)==0 and latest_update_id > MyBot.__lastServedUID):
            MyBot.__update_ids.append(latest_update_id)
            MyBot.__lastServedUID = latest_update_id
        
        elif(MyBot.__update_ids[len(MyBot.__update_ids)-1] < latest_update_id):
            MyBot.__update_ids.append(latest_update_id)
            MyBot.__lastServedUID = latest_update_id

    def startUpdatePolling(self):
        while(1):
            MyBot.__latestUpdate()
            sleep(0.5)
            print(MyBot.__update_ids)
    



    def reply():
        pass

    

b1 = MyBot()
b1.startUpdatePolling()
