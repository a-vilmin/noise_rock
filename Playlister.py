from NoiseRockers import NoiseRockers
from YouTubeHandler import YouTubeHandler
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Playlister():

    def __init__(self):
        self.NRN = NoiseRockers()
        self.YouTube = YouTubeHandler()

    def email_error(self, error):
        fp = open("logs.txt", 'r')
        info = [x.strip('\n') for x in fp.readlines()]

        msg = MIMEMultipart()
        msg['From'] = info[0]
        msg['To'] = info[1]
        msg['Subject'] = "Error at" + time.strftime("%x")   

        body = "The NOISE has been stopped by "+str(error[0])
        body +=". Argument passed was "+ str(error[1])+".\n FUCK!,\nAdam"

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(info[0], info[2])
        txt = msg.as_string()
        server.sendmail(info[0], info[1], txt)
        server.quit()

    
    def youtube_post(self):
        posts = self.NRN.read_posts()
        link_ids = []

        #find links that are youtube videos
        for each in posts:
            id = self.YouTube._video_id(each)
            if id != None:
                link_ids.append(id)

        #add them to the YouTube playlist
        for each in link_ids:
            if self.YouTube.not_repost(each):
                self.YouTube.add_to_playlist(each)

if __name__ == '__main__':
    playlist_manager = Playlister()
    
    try:
        while True:    
            playlist_manager.youtube_post()
            time.sleep(6000)
    except Exception as ex:
        message = (type(ex).__name__, ex.args)
        playlist_manager.email_error(message)
        
