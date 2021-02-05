from src.backend.lib.dbinit import connect
from src.backend.lib.read import readPos


def insertpos(fileName, Insertor):
    ## data read
    data = readPos(fileName)

    ## connect to sql server
    db = connect()
    #
    ## data preparation
    insertor = Insertor()
    vals = insertor.convert(data)

    ## data insertion
    insertor.insert(db, vals)
    db.close()

