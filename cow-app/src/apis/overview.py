from src.lib.logmanager.logManage_se import formatLog
from src.lib.dbmanager.dbinit import connect_se, connect_nl


def overview_func():
    from src.lib.logmanager.logManage_se import formatLog
    se = formatLog()
    from src.lib.logmanager.logManage_nl import formatLog
    nl = formatLog()
    return [se, nl]


def size_overview():
    db = connect_se()
    cur = db.cursor()
    statement = 'SELECT table_name AS "Table", ' +\
                'ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)", ' +\
                'table_rows as "Num" ' +\
                'FROM information_schema.TABLES ' +\
                'WHERE table_schema = "se_cow"' +\
                'ORDER BY (data_length + index_length) DESC'
    cur.execute(statement)
    se = cur.fetchall()
    cur.close()
    se = list(map(lambda x: [x[0], x[2], str(x[1])+" MB"], se))

    db = connect_nl()
    cur = db.cursor()
    statement = 'SELECT table_name AS "Table", ' +\
                'ROUND(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)", ' +\
                'table_rows as "Num" ' +\
                'FROM information_schema.TABLES ' +\
                'WHERE table_schema = "nl_cow"' +\
                'ORDER BY (data_length + index_length) DESC'
    cur.execute(statement)
    nl = cur.fetchall()
    cur.close()
    nl = list(map(lambda x: [x[0], x[2], str(x[1])+" MB"], nl))
    return [se, nl]
