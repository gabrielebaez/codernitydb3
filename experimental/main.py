from transactor import Transactor, Data

db = Transactor()

db.insert(Data('JC', 'Lives in', b'Rome'))
db.insert(Data('B', 'Lives in', b'Rome'))
db.insert(Data('JC', 'Died in', b'1200'))
db.insert(Data('Cleo', 'Lives in', b'Egypt'))
db.insert(Data('Rome', 'river', b'Tiber'))
db.insert(Data('Egypt', 'river', b'Nile'))


print("EAVT: ")
db.eavt.EAVT_index.show()
print("------")
print("AEVT: ")
db.aevt.AEVT_index.show()
print("------")
print("VAET: ")
db.vaet.VAET_index.show()