# 종종, 하나의 geometry는 단순한 geometry들의 구성으로 이루어질 때가 있는데 이를 `multi-part geometry`라고 한다.
# 만약 동일한 타입의 단순 geometry가 포함되어있으면 multi-point, multi-linestring, multi-polygon이라고 칭한다. 예를 들어, 국가 정보는 multi-polygon으로써 다수의 섬 정보를 구성하고 있다.

# geometry의 좌표 정보는 어떠한 CRS(coordinate reference system)정보가 될 수 있다. 

## PyQGIS는 geometry 정보를 구성하는데 몇가지 옵션을 제공해준다.

### from coordinates
gPnt = QgsGeometry.fromPointXY(QgsPointXY(1, 1))
print(gPnt)

gLine = QgsGeometry.fromPolyline([QgsPoint(1, 1), QgsPoint(2, 2)])
print(gLine)

gPolygon = QgsGeometry.fromPolygonXY([[QgsPointXY(1, 1), QgsPointXY(2, 2), QgsPointXY(2, 1)]])
print(gPolygon)

### from WKT(well-known text)
geom = QgsGeometry.fromWkt("POINT(3 4)")
print(geom)

### from WKB(well-known binary)
g = QgsGeometry()
wkb = bytes.fromhex("010100000000000000000045400000000000001440")
g.fromWkb(wkb)

print(g.asWkt())

## Access to Geometry

# `wkbType()` 메소드를 이용해 geometry 타입에 대해 탐색 할 수 있다. 
if gPnt.wkbType() == QgsWkbTypes.Point:
    print(gPnt.wkbType())
    # 1은 point
if gLine.wkbType() == QgsWkbTypes.LineString:
    print(gLine.wkbType())
    # 2는 line
if gPolygon.wkbType() == QgsWkbTypes.Polygon:
    print(gPolygon.wkbType())
    # 3은 polygon
    
# 대체제로 `type()`메소드를 사용 가능하다. 또한 `displayString()` 함수를 사용하여 geometry type을 얻을 수 있다.
print(QgsWkbTypes.displayString(gPnt.wkbType()))
print(QgsWkbTypes.displayString(gLine.wkbType()))
print(QgsWkbTypes.displayString(gPolygon.wkbType()))

## 튜플 형태의(x,y)는 실제 튜플 형식이 아니며 `QgsPoint` 객체입니다. 또한 값들은 `x()`, `y()` 메소드를 이용해 접근 가능합니다.


## Geometry Predicates and operations

### GEOS 라이브러리를 사용하여 `contains()`, `intersects()`, `combine()`, `difference()`와 같은 좀 더 심화된 geometry operation을 사용할 수 있습니다.
### 또한 좌표의 geometric properties를 연산할 수 있습니다. (영역, 길이)

# access the 'countires' layer
layer = QgsProject.instance().mapLayersByName('countries')[0]

# filter for countires that begin with Z, then get their features
query = '"name" LIKE \'Z%\''
features = layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))

# 루프문을 돌면서 공간정보 연산 그리고 결과 프린팅
for f in features:
    geom = f.geometry()
    name = f.attribute("NAME")
    print(name)
    print("Area: ", geom.area())
    print("Perimeter: ", geom.length())