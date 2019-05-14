import sqlite3
import datetime as dt

class entryDB(object):
    _db_connection = None
    _db_cur = None
    def __init__(self):
        self._db_connection =sqlite3.connect("entryDB.db");
        self._db_cur = self._db_connection.cursor();
    def query(self, animID):
        self._db_cur.execute("SELECT animID, allowed,nextDate FROM entry;")
        perms =self. _db_cur.fetchall();
        print ('perms:')
        print(perms)
        for anim,allow,nDate in perms:
            if anim==animID:
                d=matlab2Date(nDate);
                if d<= dt.datetime.now():
                    return allow ;
        return 0;
    def assignNextDate(self,animID,nDate):
        resp=self._db_cur.execute('UPDATE entry set nextDate = {nd} WHERE animID ="{ai}"'\
                                  .format(nd=str(nDate),ai=animID))
        self._db_connection.commit();
        return resp; 
    def commit(self):
        print('b')
        self._db_connection.commit();
#        self._db_connection.close();
    def __del__(self):
        self._db_connection.close()


def matlab2Date(matlab_datenum):
    day = dt.datetime.fromordinal(int(matlab_datenum))
    dayfrac = dt.timedelta(days=matlab_datenum%1) - dt.timedelta(days = 366)
    return day + dayfrac
