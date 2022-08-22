# Coorindate reference systems

## Specity CRS
crs = QgsCoordinateReferenceSystem("EPSG:4326")
print(crs.isValid())

## WKT로도 가능
wkt = 'GEOGCS["WGS84", DATUM["WGS84", SPHEROID["WGS84", 6378137.0, 298.257223563]],' \
    'PRIMEM["Greenwich", 0.0], UNIT["degree",0.017453292519943295],' \
    'AXIS["Longitude",EAST], AXIS["Latitude",NORTH]]'
crs = QgsCoordinateReferenceSystem(wkt)
print(crs.isValid())

## Proj string
crs = QgsCoordinateReferenceSystem()
crs.createFromProj("+proj=lonlat +ellps=WGS84 +datum=WGS84 +no_defs")
print(crs.isValid())


## 
crs = QgsCoordinateReferenceSystem("EPSG:4326")

print("QGIS CRS ID:", crs.srsid())
print("PostGIS SRID:", crs.postgisSrid())
print("Description:", crs.description())
print("Projection Acronym:", crs.projectionAcronym())
print("Ellipsoid Acronym:", crs.ellipsoidAcronym())
print("Proj String:", crs.toProj())
# check whether it's geographic or projected coordinate system
print("Is geographic:", crs.isGeographic())
# check type of map units in this CRS (values defined in QGis::units enum)
print("Map units:", crs.mapUnits())


# CRS Trnasformation
## `QgsCoordinateTransform` 클래스틀 통해 두개의 다른 공간정보를 가진 것들을 변환시켜줄 수 있다.
## 가장 쉬운 방법으로는 원하는 CRS정보를 가진 source를 만들어주고 `QgsCoordinateTransform` 인스턴스를 활용하는 것. 그러고 나서 `transform()`함수를 반복적으로 사용해 변환!

crsSrc = QgsCoordinateReferenceSystem("EPSG:4326")    # WGS 84
crsDest = QgsCoordinateReferenceSystem("EPSG:32633")    # WGS 84 / UTM zone 33N
transformContext = QgsProject.instance().transformContext()
xfrom = QgsCoordinateTransform(crsSrc, crsDest, transformContext)

# src > dest
pt1 = xfrom.transform(QgsPointXY(18, 5))
print("Transformed point:", pt1)

# dest > src (다시 되돌리기)
pt2 = xfrom.transform(pt1, QgsCoordinateTransform.ReverseTransform)
print("Trnasformed back:", pt2)