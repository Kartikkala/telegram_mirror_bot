from aria2p import API as aria2API, Client as aria2Client
from time import sleep
import multiprocessing

class Download:
    downloadList = []
    downloadGidList = [] 
    cancelDownloadList = []
    aria2Instance = aria2API(aria2Client(host='http://localhost', port=6800, secret='', timeout=60.0))

    @classmethod
    def getDownload(cls, gid):
        return cls.aria2Instance.get_download(gid)

    
    @classmethod
    def addDownload(cls, link):
        cls.downloadList = Download.aria2Instance.add(link, {'max_concurrent_downloads':2},len(cls.downloadList))
        cls.downloadGidList.append(cls.downloadList[-1].gid)
        return cls.downloadGidList[-1]

    @classmethod
    def getSpeed(cls, download):
        download = download.live
        return download.download_speed_string()

    @classmethod
    def cancelDownload(cls, gid, downloadInfoProcess):
        cls.cancelDownloadList.append(cls.getDownload(gid))
        cls.aria2Instance.remove(cls.cancelDownloadList,True,True, True)
        downloadInfoProcess.terminate()
        return downloadInfoProcess.is_alive()

    



# download.add_uri([''],{'max_concurrent_downloads':2})
