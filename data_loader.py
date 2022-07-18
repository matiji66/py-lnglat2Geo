# -*- coding: utf-8 -*-
"""

@Time  : 2022/6/30 13:49
@Author: Breeze
@File  : test.py
"""


from geo_obj import *
import pickle

base_dir = "D:\\chromedownload\\lnglat2Geo-master"
import os

boundaryAdminCell = {}

with open(os.path.join(base_dir, "boundaryAdminCell.txt")) as f:
    for line in f.readlines():
        idx, key, col1 = line.strip().split(",")
        if idx != 'idx':
            boundaryAdminCell[int(key)] = int(col1)

# '3689199061258207232' -1
boundaryIndex = {}  # Map[Long, List[Long]]

if os.path.exists(os.path.join(base_dir, "boundaryIndex.pkl")):
    with open(os.path.join(base_dir, "boundaryIndex.pkl"), 'rb') as f:
        # boundaryIndex = pickle.loads(f.read())
        boundaryIndex = pickle.load(f)
else:
    with open(os.path.join(base_dir, "boundaryIndex.txt")) as f:
        for line in f.readlines():
            idx, key, col1 = line.strip().split(",")
            if idx != 'idx':
                key = int(key)
                if boundaryIndex.get(key) is None:
                    boundaryIndex[key] = [int(e) for e in col1.split("|")]
                else:
                    data = boundaryIndex[key]
                    data.extend([int(e) for e in col1.split("|")])
                    boundaryIndex[key] = data

    with open(os.path.join(base_dir, "boundaryIndex.pkl"), 'wb') as f:
        pickle.dump(boundaryIndex, f)

#  Map[Long, List[(Long, Int, Int)]]
boundaryData = {}
if os.path.exists(os.path.join(base_dir, "boundaryData.pkl")):
    with open(os.path.join(base_dir, "boundaryData.pkl"), 'rb') as f:
        # boundaryAdminCell = pickle.loads(f.read())
        boundaryData = pickle.load(f)
else:
    with open(os.path.join(base_dir, "boundaryData.txt")) as f:
        for line in f.readlines():
            idx, key, col1, col2, col3 = line.strip().split(",")
            if idx != 'idx':
                data = boundaryData.get(int(key))
                if data is not None:
                    data.append((int(col1), int(col2), int(col3)))
                    boundaryData[int(key)] = data
                else:
                    boundaryData[int(key)] = [(int(col1), int(col2), int(col3))]

    with open(os.path.join(base_dir, "boundaryData.pkl"), 'wb') as f:
        pickle.dump(boundaryData, f)

# Map[Int, AdminNode]
adminData = {}
with open(os.path.join(base_dir, "adminData.txt"), encoding='utf-8') as f:
    for line in f.readlines():
        idx, key, name, shortName, center_lng, center_lat, level, parentId, children = line.strip().split(",")
        if idx != 'idx':
            children = [int(c) for c in children.split("|") if len(c)>0]
            center = Location(float(center_lng), float(center_lat))
            adminData[int(key)] = AdminNode(int(key), name, shortName, center, level, int(parentId), children)

# Map[Int, AdminNode]
streetData = {}
with open(os.path.join(base_dir, "streetData.txt"), encoding='utf-8') as f:
    for line in f.readlines():
        idx, id, name, shortName, center_lng, center_lat, level, parentId, children = line.strip().split(",")
        if idx != 'idx':
            children = [int(c) for c in children.split("|") if len(c)>0]
            center = Location(float(center_lng), float(center_lat))
            streetData[int(id)] = AdminNode(int(id), name, shortName, center, level, int(parentId), children)

cityBusinessArea = {}  # Map[Int, Array[BusinessAreaData]]
with open(os.path.join(base_dir, "cityBusinessArea.txt"), encoding='utf-8') as f:
    for line in f.readlines():
        idx,city_code, bussiness, center_lng,center_lat,area_code = line.strip().split(",")
        if idx != 'idx':

            center = Location(float(center_lng), float(center_lat))
            # name: str, center: Location, areaCode: int
            businessAreaDatas = cityBusinessArea.get(int(city_code))
            if businessAreaDatas is not None:
                businessAreaDatas.append(BusinessAreaData(bussiness,center,area_code))
                cityBusinessArea[int(city_code)] = businessAreaDatas
            else:
                cityBusinessArea[int(city_code)] = [BusinessAreaData(bussiness,center,area_code)]

cityLevelData = {}
with open(os.path.join(base_dir, "citylevels.txt"), encoding='utf-8') as f:
    for line in f.readlines():
        cityname,city_code,level = line.strip().split(",")
        cityLevelData[cityname] = level
        cityLevelData[city_code] = level

if __name__ == '__main__':
    print('init end')
