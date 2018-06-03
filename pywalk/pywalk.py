#coding:utf-8
import struct

__author = '浙测一院-杨子健'
__tel = '15651785611'

def main():
    import pyodbc
    fc = r'C:\Users\uuiit\Desktop\B201801006.MDB'
    conn = pyodbc.connect(r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + fc + ";Uid=;Pwd=;")
    cursor = conn.cursor()
    SQL = "select Geometry,FeatureID from 界址点Features"
    rows = cursor.execute(SQL)
    for row in [row for row in rows]:
        wkb = row[0]
        geo = FromWalkWKB(wkb)
        FeatureID = row[1]
        cursor.execute("update 界址点Features set Geometry = ? where FeatureID = {0}".format(str(FeatureID)), geo.towalkWKB)
        conn.commit()
    cursor.close()
    conn.close()


def bin2dbl(binary):
    binary = binary[::-1]
    return struct.unpack('!d', binary)[0]
def dbl2bin(double):
    return struct.pack("<d", double)
def bin2int(binary):
    binary = binary[::-1]
    return struct.unpack('!i', binary)[0]
def int2bin(i):
    return struct.pack("<i", i)

class pointZ:
    def __init__(self,binary):
        #通过24字节来初始化pointZ
        if len(binary) != 24:
            raise ValueError('this binary cannot initialize a polylineZ')
        self.x = bin2dbl(binary[0:8])     
        self.y = bin2dbl(binary[8:16])
        self.z = bin2dbl(binary[16:24])
        self.positionchange()

    def tostring(self):
        return '({0},{1},{2})'.format(self.x,self.y,self.z)

    def positionchange(self):
        pass

    def tobinary(self):
        return dbl2bin(self.x) + dbl2bin(self.y) + dbl2bin(self.z)

    def towalkWKB(self):
        return bytearray(bytearray.fromhex('01000000')+self.tobinary())

    def __repr__(self):
        return 'pointZ' + self.tostring()


class SegmentZ:
    def __init__(self,binary):
        self.pointZnum = bin2int(binary[0:4])
        self.length = 4 + self.pointZnum * 24
        if len(binary) < self.length:
            raise ValueError('this binary cannot initialize a SegmentZ')
        self.listpointZs = []
        for i in range(4, self.length, 24):
            self.listpointZs.append(pointZ(binary[i:i+24]))

    def tobinary(self):
        return int2bin(self.pointZnum)+b''.join([ptZ.tobinary() for ptZ in self.listpointZs])

    def __repr__(self):
        return 'SegmentZ('+','.join([ptZ.__repr__() for ptZ in self.listpointZs])+')'

    
class polylineZ:
    def __init__(self,binary):
        #通过字节来初始化polylineZ
        self.SegmentZnum = bin2int(binary[0:4])
        self.listSegmentZs = []
        try:
            for i in range(0,self.SegmentZnum):
                binarybeginning = 4
                for segZ in self.listSegmentZs:
                    binarybeginning += segZ.length
                segZ = SegmentZ(binary[binarybeginning:])
                self.listSegmentZs.append(segZ)
        except ValueError:
            raise ValueError('this binary cannot initialize a polylineZ')
        self.length = 4
        for segZ in self.listSegmentZs:
            self.length += segZ.length
    def tobinary(self):
        return int2bin(self.SegmentZnum)+b''.join([segZ.tobinary() for segZ in self.listSegmentZs])
    def __repr__(self):
        return 'polylineZ('+','.join([segZ.__repr__() for segZ in self.listSegmentZs])+')'
    
class multipolylineZ:
    def __init__(self,binary):
        #通过字节来初始化polygoneZ
        self.polylineZnum = bin2int(binary[0:4])
        self.listpolylineZs = []
        try:
            for i in range(0,self.polylineZnum):
                binarybeginning = 4
                for plZ in self.listpolylineZs:
                    binarybeginning += plZ.length
                plZ = polylineZ(binary[binarybeginning:])
                self.listpolylineZs.append(plZ)
        except ValueError:
            raise ValueError('this binary cannot initialize a multipolylineZ')
        self.length = 4
        for plZ in self.listpolylineZs:
            self.length += plZ.length
    def tobinary(self):
        return int2bin(self.polylineZnum)+b''.join([plZ.tobinary() for plZ in self.listpolylineZs])
    def towalkWKB(self):
        return bytearray(bytearray.fromhex('02000000')+self.tobinary())
    def __repr__(self):
        return 'multipolylineZ('+','.join([plZ.__repr__() for plZ in self.listpolylineZs])+')'

    
class polygonZ:
    def __init__(self,binary):
        #通过字节来初始化polygoneZ
        self.multipolylineZnum = bin2int(binary[0:4])
        self.listmultipolylineZs = []
        try:
            for i in range(0,self.multipolylineZnum):
                binarybeginning = 4
                for mplg in self.listmultipolylineZs:
                    binarybeginning += mplg.length
                mplg = multipolylineZ(binary[binarybeginning:])
                self.listmultipolylineZs.append(mplg)
        except ValueError:
            raise ValueError('this binary cannot initialize a polygonZ')
        self.length = 4
        for mplg in self.listmultipolylineZs:
            self.length += mplg.length
    def tobinary(self):
        return int2bin(self.multipolylineZnum)+b''.join([mplg.tobinary() for mplg in self.listmultipolylineZs])
    def towalkWKB(self):
        return bytearray(bytearray.fromhex('03000000')+self.tobinary())
    def __repr__(self):
        return 'polygonZ('+','.join([mplg.__repr__() for mplg in self.listmultipolylineZs])+')'
    
    
class polygonZ1:
    def __init__(self,binary):
        #通过字节来初始化polygoneZ
        self.multipolylineZnum = bin2int(binary[0:4])
        self.listmultipolylineZs = []
        try:
            for i in range(0,self.multipolylineZnum):
                binarybeginning = 4
                for mplg in self.listmultipolylineZs:
                    binarybeginning += mplg.length
                mplg = multipolylineZ(binary[binarybeginning:])
                self.listmultipolylineZs.append(mplg)
        except ValueError:
            raise ValueError('this binary cannot initialize a polygonZ')
        self.length = 4
        for mplg in self.listmultipolylineZs:
            self.length += mplg.length
    def tobinary(self):
        return int2bin(self.multipolylineZnum)+b''.join([mplg.tobinary() for mplg in self.listmultipolylineZs])
    def towalkWKB(self):
        return bytearray(bytearray.fromhex('05000000')+self.tobinary())
    def __repr__(self):
        return 'polygonZ1('+','.join([mplg.__repr__() for mplg in self.listmultipolylineZs])+')'

class multipolygon:
    def __init__(self,binary):
        self.polygonZnum = bin2int(binary[0:4])
        self.listpolygonZs = []
        try:
            for i in range(0, self.polygonZnum):
                binarybeginning = 4
                for plg in self.listpolygonZs:
                    binarybeginning += plg.length
                plg = polygonZ(binary[binarybeginning:])
                self.listpolygonZs.append(plg)
        except ValueError:
            raise ValueError('this binary cannot initialize a multipolygon')
        self.length = 4
        for plg in self.listpolygonZs:
            self.length += plg.length

    def tobinary(self):
        return int2bin(self.polygonZnum) + b''.join([plg.tobinary() for plg in self.listpolygonZs])

    def towalkWKB(self):
        return bytearray(bytearray.fromhex('06000000') + self.tobinary())

    def __repr__(self):
        return 'multipolygon(' + ','.join([plg.__repr__() for plg in self.listpolygonZs]) + ')'


class location:
    def __init__(self, binary):
        self.point = pointZ(binary[16:40])
        self.left = binary[0:16]
        self.right = binary[32:]
    def tobinary(self):
        return self.point.tobinary()[0:16]
    def towalkWKB(self):
        return bytearray(self.left + self.tobinary() + self.right)
    def __repr__(self):
        return self.point.__repr__()
        
def FromWalkWKB(binary):
    #通过walk的WKB初始化几何
    try:
        binary = bytes(binary)
        if binary[0:4] == bytearray.fromhex('01000000'):
            return pointZ(binary[4:])
        if binary[0:4] == bytearray.fromhex('02000000'):
            return multipolylineZ(binary[4:])
        if binary[0:4] == bytearray.fromhex('03000000'):
            return polygonZ(binary[4:])
        if binary[0:4] == bytearray.fromhex('05000000'):
            return polygonZ1(binary[4:])
        if binary[0:4] == bytearray.fromhex('06000000'):
            return multipolygon(binary[4:])
        if binary[0:14] == bytearray.fromhex('0300060000000000000000000000'):
            return location(binary)
    except ValueError:
        raise Exception('this binary cannot initialize as a WKB')
    raise Exception('this binary cannot initialize as a pointZ,a multipolylineZ or a polygonZ')
        
    
if __name__ == '__main__':
    main()