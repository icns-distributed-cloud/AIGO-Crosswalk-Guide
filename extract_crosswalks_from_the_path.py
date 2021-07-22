from haversine import haversine
import requests
import math
import json

# Tmap API - 보행자 경로 안내
# GeoJSON : (lon,lat)

# calculate
# 지구가 둥글기 때문에 유클리디안 거리를 이용하면 안된다.
# Haversine formuala 이용
def calc_length_of_crosswalk(start, end):
    res = haversine(start,end)*1000
    return res

url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'

headers={
    "appkey": "{APPKEY}",       # appkey
    "version":"1",
    "callback":""

}

# default
'''    "startX":126.97871544,   # start lon
    "startY" :37.56689860,      # start lat
    "endX" : 127.0016021,       # end lon
    "endY": 37.57081522,        # end lat
'''
data ={
    "startX":127.076444,        # start lon
    "startY" :37.248176,        # start lat
    "endX" : 127.077443,        # end lon
    "endY": 37.256968,          # end lat
    "startName":"test_start",
    "endName":"test_end"
}

res = requests.post(url, headers=headers, data=data)
res = json.loads(res.text)
#print(res)

# trunType: 211 : 횡단보도
#           212 : 좌측 횡단보도
#           213 : 우측 횡단보도
#           214: 8시 방향 횡단보도
#           215: 10시 방향 횡단보도
#           216: 2시 방향 횡단보도
#           217: 4시 방향 횡단보도
trun_type_crosswalk = [211,212,213,214,215,216,217]
line_type_crosswalk = 21
# save the start point of crosswalk
crosswalk_start_point = list()

# save the length of crosswalk
all_crosswalks = list()
all_crosswalks_from_tmap=list()
flag = 0

# features
features = res['features']
# print(features)
len_idx = len(features)-1

# extract and calculate
for i in range(1,len_idx):
    prop = features[i]['properties']
    geom = features[i]['geometry']
    if 'lineIndex' in prop:
        if(flag == 1):
            desc = prop['description'].split(',')
            all_crosswalks_from_tmap.append(desc[1])
            #flag = 0

    if 'pointIndex' in prop:
        turn_type = prop['turnType']
        if(flag==1):
            crosswalk_end_point = geom['coordinates']
            all_crosswalks.append(calc_length_of_crosswalk(crosswalk_start_point, crosswalk_end_point))
            flag = 0
            continue
        if (turn_type in trun_type_crosswalk):
            flag = 1
            desc = prop['description']
            crosswalk_start_point = geom['coordinates']



# result
if(len(all_crosswalks_from_tmap)==len(all_crosswalks)):
    print("Completes")
for i in range(len(all_crosswalks)):
    print(i, all_crosswalks[i], all_crosswalks_from_tmap[i])
