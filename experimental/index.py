from collections import namedtuple
from b_plus_tree import BPlusTree

Data = namedtuple('Data', ['entity', 'attribute', 'value'])
Datom = namedtuple('Datom', ['entity', 'attribute', 'value', 'tx'])

class EAVT:
    def __init__(self):
        self.EAVT_index = BPlusTree()  # Initialize the BPlusTree instead of a dictionary
    
    def insert(self, datom):
        key = datom.entity

        # Retrieve the entity's attribute dictionary from the BPlusTree
        entity_data = self.EAVT_index.query(key)

        if entity_data:
            # If the entity exists, update its attribute dictionary
            entity_data[datom.attribute] = [datom.value, datom.tx]
            self.EAVT_index.change(key, entity_data)  # Update the tree with the modified dictionary
        else:
            # If the entity does not exist, create a new attribute dictionary and insert it
            entity_data = {datom.attribute: [datom.value, datom.tx]}
            self.EAVT_index.insert(key, entity_data)

    def get(self, key):
        try:
            # Retrieve the entity's attribute dictionary from the BPlusTree
            return self.EAVT_index.query(key)
        except Exception as e:
            raise e



class AEVT:
    def __init__(self):
        self.AEVT_index = BPlusTree()
    
    def insert(self, datom):
        key = datom.attribute
        data = self.AEVT_index.query(key)
        if data:
            data[datom.attribute] = [datom.entity, datom.value]
            self.AEVT_index.change(key, data)
        else:
            data = {datom.attribute: [datom.entity, datom.value]}
            self.AEVT_index.insert(key, data)
   
    def get(self, key):
        try:
            return self.AEVT_index.query(key)
        except Exception as e:
            raise e


class VAET:
    def __init__(self):
        self.VAET_index = BPlusTree()
    
    def insert(self, datom):
        key = datom.value
        data = self.VAET_index.query(key)
        if data:
            data[key] = [datom.attribute, datom.entity]
            self.VAET_index.change(key, data)
        else:
            data = {key: [datom.attribute, datom.entity]}
            self.VAET_index.insert(key, data)
    
    def get(self, key):
        try:
            return self.VAET_index.query(key)
        except Exception as e:
            raise e


class AVET:
    pass


class LogIndex:
    def __init__(self):
        self.log_index = []
    
    def insert(self, datom):
        self.log_index.append(datom)