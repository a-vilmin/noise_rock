import httplib2
import sys
from NoiseRockers import NoiseRockers

from urllib.parse import urlparse, parse_qs
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

class YouTubeHandler():

    def __init__(self):
        secret = "client_id.json"
        rw_scope = "https://www.googleapis.com/auth/youtube"
        dev_key = 'AIzaSyCtzkBXa4us6QVTLp_Y_UgS1jnldKGuae0'
        self.you_tube = self._auth(secret, rw_scope, dev_key)
        self.playlist = 'PLSs2EARcZ9y5wCkGjyvckl2eSWUMpXe4c'
        self.NRN = NoiseRockers()
        
    def _auth(self, secret, rw_scope, dev_key):
        flow = flow_from_clientsecrets(secret, scope = rw_scope,
                                       message="config correctly")

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build("youtube", "v3",
                     http=credentials.authorize(httplib2.Http()))

    def _video_id(self, value):
        """
        Examples:
        - http://youtu.be/SA2iWivDJiE
        - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
        - http://www.youtube.com/embed/SA2iWivDJiE
        - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
        """
        query = urlparse(value)
        if query.hostname == 'youtu.be':
            return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch':
                p = parse_qs(query.query)
                return p['v'][0]
            if query.path[:7] == '/embed/':
                return query.path.split('/')[2]
            if query.path[:3] == '/v/':
                return query.path.split('/')[2]
        # fail?
        return None

    def create_playlist(self):
        playlists_insert_response = self.you_tube.playlists().insert(
            part="snippet,status",
            body=dict(
                snippet=dict(
                    title="NOISE_ROCK_NOW_!!!",
                    description="A Noise Rock Now Playlist"),
                status=dict(
                    privacyStatus="public"
                )
            )
        ).execute()
        return playlists_insert_response

    def add_to_playlist(self, videoID):
        add_video_request= self.you_tube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': self.playlist, 
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': videoID
                    }
                    #'position': 0
                }
            }
        ).execute()
        return add_video_request

    def get_links(self):
        posts = self.NRN.read_posts()
        link_ids = []
        for each in posts:
            id = self._video_id(each)
            if id != None:
                link_ids.append(id)
        return link_ids
        
if __name__ == '__main__':
    youTube = YouTubeHandler()

    new_adds = youTube.get_links()

    for each in new_adds:
        try:
            youTube.add_to_playlist(each)
        except Exception as e:
            print(str(e))
            continue
    

