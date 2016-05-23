from NoiseRockers import NoiseRockers
from YouTubeHandler import YouTubeHandler
from time import sleep

class Playlister():

    def __init__(self):
        self.NRN = NoiseRockers()
        self.YouTube = YouTubeHandler()


    
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

        
    playlist_manager.youtube_post()
    #sleep(6000)
