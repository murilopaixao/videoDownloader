from tinydb import TinyDB, Query
from datetime import datetime

db = TinyDB('db.json', indent=4)
db_dados = db.table("dados")
q = Query()

#db_dados.truncate()

def selectAll(): #select All
    dados = db_dados.all()
    #for x in dados:
        #print(x)
    return dados

def selectOne(query): #select one
    pesquisa = db_dados.search(q.url == query)
    return pesquisa

def insertOne(titulo,thumbnail,url):
    dataHora = datetime.now().strftime('%Y%m%d-%H-%M-%S')
    myDoc = {
        "id": dataHora,
        "titulo": titulo,
        "thumbnail": thumbnail,
        "url": url
    }
    db_dados.insert(myDoc)


