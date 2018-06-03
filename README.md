# pywalk
pywalk提供了一个纯Python的walkgis中wkb读写的功能，是一个比较好的gis数据结构入门的例子

由于walkgis中的几何数据存储形式并不是标准的wkb数据格式，但是比较类似

首先walkgis中的数据首位并没有一个字节来指示二进制数据的字节顺序

walkgis点的格式如下：

struct point{
  double X;
  double Y;
  double Z;
}

struct walkpoint{
  uint geometrytype = 1
  point pt;
}

二进制形式为：
0100000096438b6c19c8f34021b072680bc0f2400000000000000000

walkgis线的格式如下：

struct segment{
  uint pointnum;
  point[pointnum] pts;
}

struct polyline{
  uint segmentnum;
  segment[segmentnum] sgms;
}

struct walkpolyline{
  uint geometrytype = 2
  uint polylinenum;
  polyline[polylinenum] pls;
}

二进制形式为：
020000000100000001000000020000004260e5d0b6c5f340f2d24d62e6c3f24000000000000000000e2db29db7c5f340fed478e91ac4f2400000000000000000


walkgis面的格式如下：

struct polygon{
  uint polylinenum;
  polyline[polylinenum] pls;
}


struct walkpolygon{
  uint polygonnum;
  polygon[polygonnum] plgs;
}

二进制形式为：
03000000010000000100000001000000030000004260e5d0b6c5f340f2d24d62e6c3f24000000000000000000e2db29db7c5f340fed478e91ac4f24000000000000000002db29defc1c5f340508d976e4ec4f2400000000000000000
