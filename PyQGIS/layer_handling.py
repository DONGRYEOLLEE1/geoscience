# 불러오기 1
sobaek = QgsVectorLayer("D:/download/20211230/소백산.shp", 'sobaek yews1', 'ogr')
if sobaek.isValid():
    QgsProject.instance().addMapLayer(sobaek)
    
# 불러오기 2
sobaek = iface.addVectorLayer("D:/download/20211230/소백산.shp", 'sobaek yews2', 'ogr')

# 고정된 값으로 색상 불러오기
renderer = sobaek.renderer()
symbol = renderer.symbol()
symbol.setColor(QColor('#33e02c'))

# 색상 확인
QColor().colorNames()
symbol.setColor(QColor('greenyellow'))

# 범례 색상도 바꿔주기
iface.layerTreeView().refreshLayerSymbology(sobaek.id())


# 레스터 레이어 추가
