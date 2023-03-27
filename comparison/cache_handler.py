from spotipy.cache_handler import CacheHandler
import json

class FileCacheHandler(CacheHandler):
    def __init__(self, cache_path='.cache'):
        super(FileCacheHandler, self).__init__()
        self.cache_path = cache_path

    def get_cached_token(self):
        token_info = None
        try:
            with open(self.cache_path) as f:
                token_info = json.load(f)
        except IOError:
            pass
        return token_info

    def save_token_to_cache(self, token_info):
        with open(self.cache_path, 'w') as f:
            json.dump(token_info, f)