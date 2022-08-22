# get the path
path_to_airports_layer = "D:/download/QGIS-Documentation/qgis-projects/python_cookbook/airports.shp"

# shape of format : vlayer = QgsVectorLayer(data_source, layer_name, provider_name)
vlayer = QgsVectorLayer(path_to_airports_layer, 'Airports layer', 'ogr')
if not vlayer.isValid():
    print("layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    
    
# get the path to a geopackage
path_to_gpkg = os.path.join(QgsApplication.pkgDataPath(), 'resources', 'data', 'world_map.gpkg')

# append the layername part
gpkg_countries_layer = path_to_gpkg = "/layername=countries"
vlayer = QgsVectorLayer(gpkg_countries_layer, "Countires layer", "ogr")

if not vlayer.isValid():
    print("layer failed to load!")
else:
    QgsProject.instance().addMapLayer(vlayer)
    
# 가장 빠른 방법은 `addVectorLayer()` method의 `QgisInterface`를 사용하는것
vlayer = iface.addVectorLayer(path_to_airports_layer, "Airports layer", "ogr")
if not vlayer:
    print("layer failed to load!")

# 다양한 파일 불러오기
## shapefile
vlayer = QgsVectorLayer("D:/download/QGIS-Documentation/qgis-projects/python_cookbook/airports.shp", "공항_정보", "ogr")
QgsProject.instance().addMapLayer(vlayer)

## dxf file
uri = "D:/download/QGIS-Documentation/qgis-projects/python_cookbook/sample.dxf|layername = entities|geometrytype = Polygon"
vlayer = QgsVectorLayer(uri, "샘플", "ogr")
QgsProject.instance().addMapLayer(vlayer)
