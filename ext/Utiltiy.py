import json
class Josnify(object):
    def __init__(self,query: str):
        self.query = query.strip()
        self.MainData = {self.query:{}}