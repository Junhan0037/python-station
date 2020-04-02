#!/usr/bin/env python3 
#셀프 주유소 가격 분석

import pandas as pd
from glob import glob

#경로 적용
stations_files = glob('/Users/JunHan/Desktop/Python/Station-Project/지역*.xls')

tmp_raw = []

#엑셀파일 하나씩 뽑아서 합치기
for file_name in stations_files:
    tmp = pd.read_excel(file_name, header=2)
    tmp_raw.append(tmp)
    
#데이터프레임 병합
station_raw = pd.concat(tmp_raw)

#정보를 확인하니 가격정보를 숫자형으로 전환이 필요
print(station_raw.info())

#필요한 열만 가져오면서 속성(열) 이름 변경
stations = pd.DataFrame({'Oil_store':station_raw['상호'],
                             '주소':station_raw['주소'],
                             '가격':station_raw['휘발유'],
                             '셀프':station_raw['셀프여부'],
                             '상표':station_raw['상표']})   
print(stations.head())

#'주소'속성에서 '구'만 추출해서 '구'열을 생성
stations['구'] = [eachAddress.split()[1] for eachAddress in stations['주소']]
print(stations.head())

#'구'속성 중복제거하여 출력
print(stations['구'].unique())

#서울특별시라는 value가 '구'속성에 잘못 들어있는지 확인 및 변경 (예외 상황 처리)
print(stations[stations['구']=='서울특별시'])
stations.loc[stations['구']=='서울특별시', '구'] == '성동구'
print(stations['구'].unique())

#'가격'란 예외 상황 처리
print(stations[stations['가격']=='-'])    #가격이 없을시 '-'로 표시해져있다.
stations = stations[stations['가격'] != '-']  #가격이 '-'으로 되어있는경우 제외
print(stations.head())

#'가격'란 변수형을 float형으로 변경
stations['가격'] = [float(value) for value in stations['가격']]

#엑셀을 합치는 과정에서 index가 중복될수도 있기 때문에 reset_index 명령으로 인덱스를 재정렬
stations.reset_index(inplace=True)

#reset_index로 인해 index라는 컬럼이 하나 더 생기기때문에 하나 제거
del stations['index']
print(stations.info())

import matplotlib.pyplot as plt
import seaborn as sns

#matplotlib 폰트 변경 (한글지원 X 때문)
import platform
from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:\Windows\Fonts\malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')

#boxplot으로 간편하게 셀프 컬럼을 기준으로 가격 분포 확인
stations.boxplot(column='가격', by='셀프', figsize=(12,8))

#주유소의 상표별로 셀프주유소가 얼마나 저렴한지 확인
plt.figure(figsize=(12,8))
sns.boxplot(x='상표', y='가격', hue='셀프', data=stations, palette='Set3')
plt.show()

#swarmplot으로 자세한 데이터 분포 확인
plt.figure(figsize=(12,8))
sns.boxplot(x='상표', y='가격', hue='셀프', data=stations, palette='Set3')
sns.swarmplot(x='상표', y='가격', data=stations, color=".6")
plt.show()

import json
import folium
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

#'가격'순으로 정리
print(stations.sort_values(by='가격', ascending=False).head(10))
print('=======================================================')
print(stations.sort_values(by='가격', ascending=True).head(10))

#pivot_table을 이용해서 구별 가격 정보로 변경, 가격은 평균값으로 정리
import numpy as np
gu_data = pd.pivot_table(stations, index=["구"], values=["가격"], aggfunc=np.mean)
print(gu_data.head())

#지도에 표현
geo_path = '/Users/JunHan/Desktop/Python/Station-Project/02. folium_us-states.json'
geo_str = json.load(open(geo_path, encoding='utf-8'))
map = folium.Map(location=[35.1643, 128.931], zoom_start=10.5, tiles='Stamen Toner')
map.choropleth(geo_data = geo_str,
               data = gu_data,
               columns = [gu_data.index, '가격'],
               fill_color = 'PuRd', #PuRd, YlGnBu
               key_on = 'feature.id')
map.save('map1.html')

#주유가격 상위 10개 주유소 이름 지정
oil_price_top10 = stations.sort_values(by='가격', ascending=False).head(10)
print(oil_price_top10)

#주유가격 하위 10개 주유소 이름 지정
oil_price_bottom10 = stations.sort_values(by='가격', ascending=True).head(10)
print(oil_price_bottom10)


#Google Maps API 로그인
import googlemaps
gmaps_key = "AIzaSyDMgtEhS_gxWY2RETnV-wdUFa3UoH2xOPM"
gmaps = googlemaps.Client(key=gmaps_key)


#주유가격 상위 10개 주유소에 대해 위도, 경도 정보를 읽어옴
from tqdm import tqdm_notebook
lat = []
lng =[]
for n in tqdm_notebook(oil_price_top10.index):
    try:
        tmp_add = str(oil_price_top10['주소'][n]).split('(')[0]
        tmp_map = gmaps.geocode(tmp_add)
        tmp_loc = tmp_map[0].get('geometry')
        lat.append(tmp_loc['location']['lat'])
        lng.append(tmp_loc['location']['lng'])
    except:
        lat.append(np.nan)
        lng.append(np.nan)
        print("Here is nan !")
        
oil_price_top10['lat'] = lat
oil_price_top10['lng'] = lng
print(oil_price_top10)

#주유가격 하위 10개 주유소에 대해 위도, 경도 정보를 읽어옴
from tqdm import tqdm_notebook
lat = []
lng =[]
for n in tqdm_notebook(oil_price_bottom10.index):
    try:
        tmp_add = str(oil_price_bottom10['주소'][n]).split('(')[0]
        tmp_map = gmaps.geocode(tmp_add)
        tmp_loc = tmp_map[0].get('geometry')
        lat.append(tmp_loc['location']['lat'])
        lng.append(tmp_loc['location']['lng'])
        
    except:
        lat.append(np.nan)
        lng.append(np.nan)
        print("Here is nan !")
        
oil_price_bottom10['lat'] = lat
oil_price_bottom10['lng'] = lng
print(oil_price_bottom10)

#지도에 주유가격 상위, 하위 10개 주유소 CircleMarker로 표시
map = folium.Map(location=[35.1643, 128.931], zoom_start=10.5)

for n in oil_price_top10.index:
    if pd.notnull(oil_price_top10['lat'][n]):
        folium.CircleMarker([oil_price_top10['lat'][n], oil_price_top10['lng'][n]],
                             radius=15, color='#CD3181',
                             fill_color='#CD3181').add_to(map)
        folium.Marker([oil_price_top10['lat'][n], oil_price_top10['lng'][n]]).add_to(map)

                        
for n in oil_price_bottom10.index:
     if pd.notnull(oil_price_bottom10['lat'][n]):
        folium.CircleMarker([oil_price_bottom10['lat'][n], oil_price_bottom10['lng'][n]],
                             radius=15, color='#3186cc',
                             fill_color='#3186cc').add_to(map)
        folium.Marker([oil_price_bottom10['lat'][n], oil_price_bottom10['lng'][n]]).add_to(map)
                    
map.save('map2.html')
