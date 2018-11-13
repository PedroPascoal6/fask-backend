import sqlite3
from datetime import datetime
data = {}
con = sqlite3.connect("politiciansBD.db")



def updatePolitician():
    subordinates,politicians = {}
    for row in con.execute("select * from politician"):
        politicians[row[0]] = {"name": row[1],
                        "superiorid": row[2],
                        "superiorName": row[3],
                        "subordinateid": row[4],
                        "subordinateName": row[5]}

    for row in con.execute("select * from politicianEvent"):
        if row[3] == 1:
            subordinates[row[2]] = {"subordinates": row[4].split(";")[0].split("=") + data[row[2]].get("subordinates")}
    data = {subordinates,politicians}
    return data


def getData():
    return data

def updateData():

    sql = ''' INSERT INTO politician VALUES(0,'Wibeu',null,'',1,'Curusego',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(1,'Curusego',1,'Curusego',2,'Nalvar',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(2,'Nalvar',1,'Curusego',null,'',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(3,'Alberto',1,'Curusego',null,'',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(4,'Bufiobere',1,'Curusego',null,'',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(5,'Flunodae',0,'',6,'Osceo',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(6,'Osceo',5,'Flunodae',null,'',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politician VALUES(7,'Envailslag',null,'',null,'',1) '''
    con.execute(sql)
    sql = ''' INSERT INTO politicianEvent VALUES(0,'''+str(datetime.now())+''',0,'1',"added=1") '''
    print(sql)
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(1,'''+str(datetime.now())+''',0,'1',"added=2") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(2,'''+str(datetime.now())+''',0,'1',"added=3") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(3,'''+str(datetime.now())+''',0,'1',"added=4") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(4,'''+str(datetime.now())+''',1,'1',"added=5") '''
    # con.execute(sql)
    # sql = ''' INSERT INTO politicianEvent VALUES(5,'''+str(datetime.now())+''',1,'1',"added=6") '''
    # con.execute(sql)
    return True