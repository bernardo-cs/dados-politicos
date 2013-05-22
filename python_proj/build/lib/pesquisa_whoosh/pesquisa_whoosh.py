from whoosh.index import open_dir
from whoosh.qparser import *
from whoosh.index import create_in
from whoosh.fields import *
import sqlite_db.bdsql as bd

def indexer(queryCurs):

    data = bd.getDescricao(queryCurs)

    schema = Schema(id = NUMERIC(stored=True), content=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    for line in data:
        writer.add_document(id=int(line[0]), content=line[2])

    writer.commit() 


def procura(input):
    a=[]
    ix = open_dir("indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema, group=OrGroup).parse(unicode(input, "UTF-8"))
        results = searcher.search(query, limit=1000)

        for r in results:
            a.append(str(r["id"]))
    return a