import tika
tika.initVM()
from tika import parser
parsed = parser.from_file('/home/jimmylin/DESA2013InequalityMatters.pdf')
print(parsed["metadata"])
print(parsed["content"])
