import requests
import json

# Tmap API - 보행자 경로 안내
# GeoJSON : (lon,lat)
def calc_length_of_crosswalk(sX, sY, eX, eY):
    return

url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian'

headers={
    "appkey": "{APPKEY}",   # appkey
    "version":"1",
    "callback":""

}
data ={
    "startX":126.97871544,      # start lon
    "startY" :37.56689860,      # start lat
    "endX" : 127.0016021,       # end lon
    "endY": 37.57081522,        # end lat
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

# save the start point of crosswalk
crosswalk_point = list()

# save the length of crosswalk
len_crosswalk = list()
flag = 0

# features
features = res['features']
len_idx = len(features)-1
for i in range(1,len_idx):
    if 'pointIndex' in features[i]['properties']:
        prop = features[i]['properties']
        turn_type = prop['turnType']
        if(flag==1):
            calc_length_of_crosswalk()
            continue
        if (turn_type in trun_type_crosswalk):
            # print(turn_type)
            flag = 1



# geometry
