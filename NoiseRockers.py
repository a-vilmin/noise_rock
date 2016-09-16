import facebook


class NoiseRockers():

    def __init__(self):
        keys = []
        with open('access.txt') as f:
            keys = f.read().splitlines()

        self.nrn_id = keys[0]
        self.app_id = keys[1]
        self.app_secret = keys[2]
        self.key = keys[3]
        self.init_fb()

    def init_fb(self):
        
        self.graph = facebook.GraphAPI(access_token = self.key)
        self.extended_token = self.graph.extend_access_token(self.app_id,
                                                             self.app_secret)

    def read_posts(self):

        posts = self.graph.get_object(self.nrn_id+"/feed", limit = 100)
        links = [] 
        for each in posts['data']:
            try:
                links.append(each['link'])
            except KeyError:
                continue
        return links

if __name__ == '__main__':
    reader = NoiseRockers()
    posts = reader.read_posts()
    



