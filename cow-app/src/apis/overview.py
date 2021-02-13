from src.lib.logmanager.logManage_se import formatLog
from src.lib.dbmanager.dbinit import connect_se, connect_nl


def overview_func():
    return formatLog()


def size_overview():
    db_nl = connect_nl()
    db = connect_se()
    cur = db.cursor()
    statement = 'SELECT table_name AS "Table", ' +\
                'ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)", ' +\
                'table_rows as "Num" ' +\
                'FROM information_schema.TABLES ' +\
                'WHERE table_schema = "CowData"' +\
                'ORDER BY (data_length + index_length) DESC'
    cur.execute(statement)
    result = cur.fetchall()
    result = list(map(lambda x: [x[0], x[2], str(x[1])+" MB"], result))
    return result