lon = 127.947727443701; lat = 37.337061376149
page = 1

api_key = "자신의 API키 입력"

def search_CVS(lon, lat):
    df = pd.DataFrame(columns = ["place_name", 'road_address_name', 'distance', 'x', 'y'])
    page = 1
    while True:
        url = "https://dapi.kakao.com/v2/local/search/category.json?&category_group_code=CS2&x="\
        +str(lon)+"&y="+str(lat)+"&page="+str(page)+"&radius=1000"
        json_obj = requests.get(url = url,headers={"Authorization":f"KakaoAK {api_key}"}).json()
        
        for document in json_obj['documents']:
            df_s = pd.DataFrame(document, index = [0])[['place_name', 'road_address_name', 'distance', 'x', 'y']]
            df = df.append(df_s)
        if json_obj['meta']['is_end'] == False:
            page += 1
        else:
            vl = QgsVectorLayer("Point?crs=EPSG:4326", "CVS", "memory")
            pr = vl.dataProvider()
            pr.addAttributes([QgsField("place_name", QVariant.String),
            QgsField("road_address_name", QVariant.String),
            QgsField("distance", QVariant.Int),
            QgsField("lon", QVariant.Double),
            QgsField("lat", QVariant.Double)])
            vl.updateFields()
            
            for i in range(len(df)):
                f = QgsFeature()
                f.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(float(df.iloc[i, 3]), float(df.iloc[i, 4]))))  ## lat, lon
                f.setAttributes([df.iloc[i, 0], df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 4], df.iloc[i, 3]])    ## lon, lat
                pr.addFeature(f)
                
            vl.updateExtents()
            QgsProject.instance().addMapLayer(vl)
            break