#coding:utf-8
import pyodbc
import pywalk
import copy
import binascii
import os


def positionMagicChange(self):
    self.x += 100
    self.y += 100


pywalk.pointZ.positionchange = positionMagicChange

def run(dirpath):
    for root,dir,files in os.walk(dirpath):
        for file in files:
            if os.path.splitext(file)[1].upper() == '.MDB':
                fc = os.path.join(root, file)
                conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + fc + ";Uid=;Pwd=;")
                cursor = conn.cursor()
                tables = []
                for table in cursor.tables():
                    tablename = copy.deepcopy(table[2])
                    tables.append(tablename)
                for tablename in tables:
                    if tablename[-8:] == 'Features':
                        SQL = "select Geometry,FeatureID from {0}".format(tablename)
                        rows = cursor.execute(SQL)
                        for row in [row for row in rows]:
                            wkb = row[0]
                            FeatureID = row[1]
                            try:
                                geo = pywalk.FromWalkWKB(wkb)
                                cursor.execute("update {1} set Geometry = ? where FeatureID = {0}".format(str(FeatureID),tablename), geo.towalkWKB())
                                conn.commit()
                            except:
                                print('dbpath {3}, table {0} ,FeatureID {1} failed ,binary :{2}'.format(tablename, FeatureID, binascii.b2a_hex(bytes(wkb)),fc))
                    if tablename[-11:] == 'Annotations':
                        SQL = "select Location,AnnotationID,Annotation from {0}".format(tablename)
                        rows = cursor.execute(SQL)
                        for row in [row for row in rows]:
                            wkb = row[0]
                            FeatureID = row[1]
                            try:
                                geo = pywalk.FromWalkWKB(wkb)
                                cursor.execute("update {1} set Location = ? where AnnotationID = {0}".format(str(FeatureID),tablename), geo.towalkWKB())
                                conn.commit()
                            except:
                                print('dbpath {3},table {0} ,AnnotationID {1} failed ,binary :{2},{3}'.format(tablename, FeatureID, binascii.b2a_hex(bytes(wkb)), str(row[2]),fc))
                cursor.close()
                conn.close()


if __name__ == '__main__':
    run(r'E:\坐标转换\杭州\walk')