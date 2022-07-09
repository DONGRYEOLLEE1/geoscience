### Python Geopandas ###


# 1. packs ----
import numpy as np
import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point, Polygon, LineString
from shapely import wkt
from  pyproj import Proj, transform


# [타원체 바꾼 지리원 표준]
# 과거 지리원 좌표계에서 타원체와 lon_0 문제를 수정한 좌표계로 2000년대 초반에 잠시 많이 사용되었습니다.

# 2. set proj4 ----
UTMK = "+proj=tmerc +lat_0=38 +lon_0=127.5 +k=0.9996 +x_0=1000000 +y_0=2000000 +ellps=GRS80 +units=m +no_defs"
GRS80 = '+init=epsg:5181'  ## 중부원점(다음지도에서 사용중인 좌표계)



# 3. get admi data ----
## [출처] http://www.gisdeveloper.co.kr/?p=2332
admi = gpd.read_file('/home/ghks9209/HEE/ETC/DATA/PRACTICE/TL_SCCO_EMD.shp',encoding='euc-kr')  ## 읍면동
sig = gpd.read_file('/home/ghks9209/HEE/ETC/DATA/PRACTICE/TL_SCCO_SIG.shp',encoding='euc-kr')  ## 시군구
mega = gpd.read_file('/home/ghks9209/HEE/ETC/DATA/PRACTICE/TL_SCCO_CTPRVN.shp',encoding='euc-kr')  ## 시도

admi.drop(['EMD_ENG_NM'], axis='columns', inplace=True)
sig.drop(['SIG_ENG_NM','geometry'], axis='columns', inplace=True)
mega.drop(['CTP_ENG_NM','geometry'], axis='columns', inplace=True)

admi['SIG_CD'] = admi.EMD_CD.str[0:5]
admi['CTPRVN_CD'] = admi.EMD_CD.str[0:2]

admi = admi.merge(sig, on = "SIG_CD", how = "left")
admi = admi.merge(mega, on = "CTPRVN_CD", how = "left")

admi = admi[['CTP_KOR_NM','CTPRVN_CD','SIG_KOR_NM','SIG_CD','EMD_KOR_NM','EMD_CD','geometry']]

admi = admi.rename(columns={'CTP_KOR_NM':'MEGA_NM', 'CTPRVN_CD':'MEGA_CD', 'SIG_KOR_NM':'SIG_NM', 'EMD_KOR_NM':'EMD_NM'})

admi = admi.to_crs(UTMK)




# 4. create grid data ----
x_axis = range(900000+50, 950000-50, 50) 
y_axis = range(1900000+50, 1950000-50, 50)

x_axis = np.repeat(x_axis, 999)
y_axis = np.array(np.repeat([y_axis], 999, axis=0)).flatten()

idx = list(range(0,len(x_axis))) # for cell_id

# create data frame of grid
df = pd.DataFrame({"x_axis" : x_axis, "y_axis" : y_axis, "cell_id" : idx}) 
df = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.x_axis, df.y_axis), crs=UTMK)

# sjoin between grid and admi 
df = gpd.sjoin(df, admi, op='intersects', how='inner')
df = df.drop(columns=['index_right'])
df = df.dropna()

#set buffer to centroid point
df['geometry'][0:1].plot()
df.geometry = df.buffer(50, cap_style=3)
df['geometry'][0:1].plot()

df = df[['cell_id','MEGA_NM','MEGA_CD','SIG_NM','SIG_CD','EMD_NM','EMD_CD','geometry']]

df = df.loc[df['MEGA_CD'] == '11'] #서울만
df = df.reset_index().drop(columns=['index'])

df.SIG_NM.unique()



# 5. sjoin / overlay data by geometry ----
##[출처] http://data.nsdi.go.kr/dataset/20180918ds00072
##[출처] http://data.nsdi.go.kr/dataset/14783
buld = gpd.read_file('/home/ghks9209/HEE/ETC/DATA/PRACTICE/Z_KAIS_TL_SPBD_BULD_11000.shp',encoding='euc-kr')
road = gpd.read_file('/home/ghks9209/HEE/ETC/DATA/PRACTICE/Z_KAIS_TL_SPRD_RW_11000.shp',encoding='euc-kr')

buld = buld.set_crs(GRS80)
buld = buld.to_crs(UTMK)

road = road.set_crs(GRS80)
road = road.to_crs(UTMK)

buld_type_n = {"comm": ['03000','03001','03002','03003','03004','03005','03006','03013','03014','03015','03016','03017','03018','03019','03020','03023','03999','04000','04001','04002','04003','04004','04005','04006','04007','04008','04009','04010','04011','04012','04014','04015','04016','04017','04018','04019','04020','04021','04022','04023','04101','04102','04103','04104','04105','04106','04107','04199','04201','04202','04203','04299','04301','04302','04303','04304','04305','04399','04401','04402','04403','04404','04405','04499','04999','05201','06000','06100','06201','06202','06203','06204','06205','06299','06301','06302','06303','06304','06305','06306','06307','06308','06309','06310','06999','08003','11000','11101','11102','11103','11199','11201','11202','11203','11204','11205','11299','12000','12001','12002','12003','12004','12005','12006','12007','12008','12009','12999','15000','15001','15002','15003','15004','15005','15006','15007','15008','15009','15999','16000','```16001','16002','16003','16004','16005','16006','16007','16008','16009','16010','16999','21005'], "work": ['10000','10101','10102','10103','10199','10201','10202','10203','10204','10299'], "resi": ['01000','01001','01002','01003','01004','02000','02001','02002','02003','02004','02005','02006','02007']}


#sjoin : geometry를 사용한 결합
#buld
tmp = gpd.sjoin(df, buld[['BDTYP_CD','geometry']], op='intersects', how='left')
tmp['geometry'][0:1].plot()

tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["comm"]), "buld_type"] = 'comm'
tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["work"]), "buld_type"] = 'work'
tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["resi"]), "buld_type"] = 'resi'

tmp = tmp.loc[~tmp['buld_type'].isna()]

##aggregate comm cnt
resSjoin = df.merge(pd.DataFrame(tmp.loc[tmp['buld_type'] == 'comm','cell_id'].value_counts() ).reset_index().rename(columns={'index':'cell_id', 'cell_id':'comm_cnt'}), on = "cell_id", how = "left" )
resSjoin.loc[resSjoin['comm_cnt'].isna(),'comm_cnt'] = 0
resSjoin['comm_cnt'] = resSjoin['comm_cnt'].astype(int)

##aggregate work cnt
resSjoin = resSjoin.merge(pd.DataFrame(tmp.loc[tmp['buld_type'] == 'work','cell_id'].value_counts() ).reset_index().rename(columns={'index':'cell_id', 'cell_id':'work_cnt'}), on = "cell_id", how = "left" )
resSjoin.loc[resSjoin['work_cnt'].isna(),'work_cnt'] = 0
resSjoin['work_cnt'] = resSjoin['work_cnt'].astype(int)

##aggregate resi cnt
resSjoin = resSjoin.merge(pd.DataFrame(tmp.loc[tmp['buld_type'] == 'resi','cell_id'].value_counts() ).reset_index().rename(columns={'index':'cell_id', 'cell_id':'resi_cnt'}), on = "cell_id", how = "left" )
resSjoin.loc[resSjoin['resi_cnt'].isna(),'resi_cnt'] = 0
resSjoin['resi_cnt'] = resSjoin['resi_cnt'].astype(int)

#road
tmp = gpd.sjoin(df, road[['geometry']], op='intersects', how='left')

tmp = tmp.loc[~tmp['index_right'].isna()]

resSjoin = resSjoin.merge(pd.DataFrame(tmp['cell_id'].value_counts() ).reset_index().rename(columns={'index':'cell_id', 'cell_id':'road_cnt'}), on = "cell_id", how = "left" )
resSjoin.loc[resSjoin['road_cnt'].isna(),'road_cnt'] = 0
resSjoin['road_cnt'] = resSjoin['road_cnt'].astype(int)




#overlay : geometry 간의 연산
tmp = gpd.overlay(df, buld[['BDTYP_CD','UND_FLO_CO','GRO_FLO_CO','geometry']], how = 'intersection')
tmp['geometry'][0:1].plot()

tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["comm"]), "buld_type"] = 'comm'
tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["work"]), "buld_type"] = 'work'
tmp.loc[tmp['BDTYP_CD'].isin(buld_type_n["resi"]), "buld_type"] = 'resi'

tmp = tmp.loc[~tmp['buld_type'].isna()]

##aggregate comm area
tmp['comm_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'comm' ,'geometry'], crs=UTMK).area
tmp['comm_tot_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'comm' ,'geometry'], crs=UTMK).area * (tmp['GRO_FLO_CO'] + tmp['UND_FLO_CO'])

resOverlay = df.merge(pd.DataFrame(tmp.groupby('cell_id')['comm_area'].sum()).reset_index(), on = "cell_id", how = "left" )
resOverlay = resOverlay.merge(pd.DataFrame(tmp.groupby('cell_id')['comm_tot_area'].sum()).reset_index(), on = "cell_id", how = "left" )

resOverlay.loc[resOverlay['comm_area'].isna(),'comm_area'] = 0
resOverlay.loc[resOverlay['comm_tot_area'].isna(),'comm_tot_area'] = 0


##aggregate work area
tmp['work_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'work' ,'geometry'], crs=UTMK).area
tmp['work_tot_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'work' ,'geometry'], crs=UTMK).area * (tmp['GRO_FLO_CO'] + tmp['UND_FLO_CO'])

resOverlay = resOverlay.merge(pd.DataFrame(tmp.groupby('cell_id')['work_area'].sum()).reset_index(), on = "cell_id", how = "left" )
resOverlay = resOverlay.merge(pd.DataFrame(tmp.groupby('cell_id')['work_tot_area'].sum()).reset_index(), on = "cell_id", how = "left" )

resOverlay.loc[resOverlay['work_area'].isna(),'work_area'] = 0
resOverlay.loc[resOverlay['work_tot_area'].isna(),'work_tot_area'] = 0


##aggregate resi area
tmp['resi_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'resi' ,'geometry'], crs=UTMK).area
tmp['resi_tot_area'] = gpd.GeoSeries(tmp.loc[tmp['buld_type'] == 'resi' ,'geometry'], crs=UTMK).area * (tmp['GRO_FLO_CO'] + tmp['UND_FLO_CO'])

resOverlay = resOverlay.merge(pd.DataFrame(tmp.groupby('cell_id')['resi_area'].sum()).reset_index(), on = "cell_id", how = "left" )
resOverlay = resOverlay.merge(pd.DataFrame(tmp.groupby('cell_id')['resi_tot_area'].sum()).reset_index(), on = "cell_id", how = "left" )

resOverlay.loc[resOverlay['resi_area'].isna(),'resi_area'] = 0
resOverlay.loc[resOverlay['resi_tot_area'].isna(),'resi_tot_area'] = 0


resSjoin
resOverlay


## create wkt 
resOverlay['str_geom'] = resOverlay.geometry.apply(lambda x: wkt.dumps(x))

resOverlay['geometry'][0:1].plot()
resOverlay['str_geom'][0:1].plot()

resOverlay.drop(['geometry'], axis=1, inplace=True)

resOverlay = gpd.GeoDataFrame(
	resOverlay,
	geometry=[wkt.loads(shape_wkt) for shape_wkt in resOverlay['str_geom']],
	crs=UTMK
)

resOverlay['geometry'][0:1].plot()
resOverlay['str_geom'][0:1].plot()