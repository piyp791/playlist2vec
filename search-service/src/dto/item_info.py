class ItemInfo:
    def __init__(self, idx: int, name: str):
        self.idx: int = idx
        self.name: str = name
        self.id: str = None
        self.cover: str = None
        
    def set_id(self, id: str):
        self.id = id
    
    def set_cover(self, cover: str):
        self.cover = cover
    
    def __repr__(self):
        return str({'idx': self.idx, 'name': self.name, 'id': self.id, 'cover': self.cover})