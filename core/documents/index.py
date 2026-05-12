class DocumentIndex:
    def __init__(self): self.items = {}
    def add(self, metadata: dict): self.items[metadata['doc_id']] = metadata
