from config.database import es

class ElasticRepository:
    def __init__(self, index_name):
        self.index_name = index_name

    def insert(self, doc_id, data):
        es.index(index=self.index_name, id=doc_id, body=data)
        return True

    def get(self, doc_id):
        try:
            return es.get(index=self.index_name, id=doc_id)
        except:
            return None

    def update(self, doc_id, data):
        es.update(index=self.index_name, id=doc_id, body={"doc": data})
        return True

    def delete(self, doc_id):
        es.delete(index=self.index_name, id=doc_id)
        return True
