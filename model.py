db = dict()

class User:
    def __init__(self, name, key) -> None:
        self.name = name
        self.key = key 
        
    @classmethod
    def find_by_name(cls, name):
        return db[name] if name in db else False
    
    def save_to_db(self):
        db[self.name] = self.key