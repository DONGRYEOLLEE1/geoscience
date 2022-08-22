# `GDAL` 라이브러리 사용 - 다양한 파일 포맷 지원

# get the path
path_to_tif = "D:/download/QGIS-Documentation/qgis-projects/python_cookbook/data/srtm.tif"
rlayer = QgsRasterLayer(path_to_tif, "SRTM layer")
if not rlayer.isValid():
    print("layer failed to load!")
    
# geopackage로 래스터를 로드

## get the path to a geopackage
path_to_gpkg = os.path.join("D:/download/QGIS-Documentation/qgis-projects/python_cookbook", 'testdata', 'sublayers.gpkg')

## gpkg_raster_layer
gpkg_raster_layer = "GPKG:" + path_to_gpkg + ":srtm"

rlayer = QgsRasterLayer(gpkg_raster_layer, "layer name", "gdal")

if not rlayer.isValid():
    print("layer failed to load!")