from sqlalchemy.orm import Session

class BaseRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, model, record_id):
        return self.session.query(model).filter(model.id == record_id).first()

    def create(self, model, data):
        record = model(**data)
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def update(self, model, record_id, data):
        record = self.get(model, record_id)
        if not record:
            return None
        for key, value in data.items():
            setattr(record, key, value)
        self.session.commit()
        return record

    def delete(self, model, record_id):
        record = self.get(model, record_id)
        if not record:
            return False
        self.session.delete(record)
        self.session.commit()
        return True





# from sqlalchemy.orm import Session

# class BaseRepository:
#     def __init__(self, session: Session):
#         self.session = session

#     def get(self, model, record_id):
#         return self.session.query(model).filter(model.id == record_id).first()

#     def create(self, model, data):
#         record = model(**data)
#         self.session.add(record)
#         self.session.commit()
#         return record

#     def update(self, model, record_id, data):
#         record = self.get(model, record_id)
#         if not record:
#             return None
#         for key, value in data.items():
#             setattr(record, key, value)
#         self.session.commit()
#         return record

#     def delete(self, model, record_id):
#         record = self.get(model, record_id)
#         if not record:
#             return False
#         self.session.delete(record)
#         self.session.commit()
#         return True
