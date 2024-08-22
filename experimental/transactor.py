from index import (
    Data, Datom,
    EAVT, AEVT, VAET,
    LogIndex
)

# from indexes import AVET

class Transactor:
    def __init__(self):
        self.eavt = EAVT()
        self.aevt = AEVT()
        self.vaet = VAET()
        self.log_index = LogIndex()
        self.t = 0
        self.id = 0

    def insert(self, data):
        try:
            datom = Datom(data.entity, data.attribute, data.value, self.t)
            self.eavt.insert(datom)
            self.aevt.insert(datom)
            self.vaet.insert(datom)
            self.log_index.insert(datom)
            self.t += 1
        except Exception as e:
            print(e)

    def create_entity(self, schema):
        for k, v in schema.items():
            self.insert(Data(self.id, f'{k}', v))
        self.id += 1
        return True

    def create_table(self, schema):
        pass

    def delete_entity(self, entity):
        pass
