
from s2sphere import CellId

from s2sphere import LatLng

import GeoUtils
import S2Utils, LineUtils
from geo_obj import *
# pip --trusted-host pypi.tuna.tsinghua.edu.cn install s2sphere
from data_loader import boundaryAdminCell, boundaryIndex, boundaryData, adminData, streetData, cityBusinessArea, \
    cityLevelData

min_level = 12


def init(needBoundary=True, needArea=False, needStreet=True, needCityLevel=False):
    """
     按需初始化数据, 离线数据处理可以不加载该方法
    :param needBoundary:   是否需要加载边界数据，用于经纬度转换省市区县
    :param needArea:       是否需要加载商圈数据
    :param needStreet:     是否需要加载街道数据
    :param needCityLevel:  是否需要加载城市级别数据
    :return:
    """

    adminData
    if needBoundary:
        boundaryData
        boundaryIndex
        boundaryAdminCell

    if needStreet:
        streetData
    if needArea:
        cityBusinessArea
    if needCityLevel:
        cityLevelData


def determineAdminCode(lonIn: float, latIn: float, coordSys: CoordinateSystem = CoordinateSystem.GCJ02):
    gcj02LonLat = GeoUtils.toGCJ02(lonIn, latIn, coordSys)
    lon = gcj02LonLat[0]
    lat = gcj02LonLat[1]
    # print(lon, lat)
    # lon = 112.989382
    # lat = 28.147062

    s2LatLng = LatLng.from_degrees(lat, lon)
    id1 = CellId.from_lat_lng(s2LatLng).parent(min_level).id()

    id2 = CellId.from_lat_lng(s2LatLng).parent(min_level - 2).id()
    if GeoUtils.outOfChina(lon, lat):
        return -1
    elif boundaryAdminCell.get(id1) is not None:
        return boundaryAdminCell.get(id1)
    elif boundaryAdminCell.get(id2) is not None:
        return boundaryAdminCell.get(id2)
    else:
        keys = []
        maxLevel = 2000  # 必须大于2000m，否则会出现格子半径过小选择错误问题
        # 最远距离 为新疆哈密市80公里
        while len(keys) == 0 and maxLevel < 200000:
            newKeys = S2Utils.getCellId(s2LatLng, maxLevel, min_level)
            # newKeys = []
            for key in newKeys:
                if boundaryIndex.get(key) is not None:
                    print("flatmap", key, maxLevel, boundaryIndex.get(key))
                    keys.extend(boundaryIndex.get(key))

            maxLevel = maxLevel * 2

        def fun_(key, s2LatLng):
            # 修改成 getutils distance
            # return (key, CellId(key).to_lat_lng().get_distance(s2LatLng))
            # return key, GeoUtils.get_earth_distance(CellId(key).to_lat_lng(), s2LatLng)
            latlng = CellId(key).to_lat_lng()
            dis = GeoUtils.get_earth_dist(latlng, s2LatLng)
            return key, dis

        print('keys', keys)
        if len(keys) > 0:
            # lines1 = map(lambda key: fun_(key, s2LatLng),newKeys)
            lines1 = []
            for key in keys:
                lines1.append(fun_(key, s2LatLng))
            lines1.sort(key=lambda x: x[1])
            # take 5
            lines1_tak5 = lines1[0:5]
            print("lines1_tak5 ", lines1_tak5)
            res1 = []
            # flatmap
            for startPoint in lines1_tak5:
                if boundaryData.get(startPoint[0]) is not None:
                    values = boundaryData.get(startPoint[0])
                    for value in values:
                        res1.extend(
                            [(startPoint[0], value[0], value[1], True), (startPoint[0], value[0], value[2], False)])
            lines1 = []
            for line in res1:
                start = CellId(line[0]).to_lat_lng()
                end = CellId(line[1]).to_lat_lng()
                if len(lines1)==18:
                    print(start,end)
                dis = LineUtils.pointToLineDis(start.lng().degrees, start.lat().degrees, end.lng().degrees,
                                               end.lat().degrees, lon, lat)
                lines1.append((((start.lng().degrees, start.lat().degrees), (end.lng().degrees, end.lat().degrees),
                                line[2], line[3]), dis))
            print("lines1 ", lines1)
            minDis = min([line[-1] for line in lines1])
            lines = [line[0] for line in lines1 if line[-1] == minDis]
            from itertools import groupby
            result = groupby(sorted(lines), key=lambda x: x[0])
            max_th = 0
            tp = []
            for key, group in result:
                group_list = list(group)
                if len(group_list) > max_th:
                    tp = group_list
                    max_th = len(group_list)
                elif len(group_list) == max_th:
                    pass
                    # tp.extend(group_list)
                # print(key, len(group_list))
            # print("lines ", tp)

            if len(tp) == 1:  # 国内海外边界
                line1 = tp[0]
                start = line1[0]
                end = line1[1]
                # 三点用行列式判断旋转方向
                angle = (start[0] - lon) * (end[1] - lat) - (end[0] - lon) * (start[1] - lat)
                if (angle < 0) == line1[3]:
                    return line1[2]
                else:
                    return -1
            elif len(tp) == 2:  # 两条线段，如果终点不同，则一定是国内和海外，并且点到线段距离最短点为起点，终点相同，则为国内两个区域边界
                line1 = tp[0]
                line2 = tp[-1]
                #  终点相同，为国内两个相邻区域，终点不同，为国界线
                start = line1[0] if (line1[1].__eq__(line2[1])) else line2[1]
                end = line1[1]
                #  三点用行列式判断旋转方向
                angle = (start[0] - lon) * (end[1] - lat) - (end[0] - lon) * (start[1] - lat)
                if (angle < 0) == line1[3]:
                    return line1[2]
                elif line1[1] == line2[1] and line1[3] != line2[3]:
                    return line2[2]
                else:
                    return -1
            else:  # 多区域顶点 判断
                #
                res1 = groupby(sorted(tp, key=lambda x: int(x[2])), key=lambda x: int(x[2]))
                res2 = []
                for key, group in res1:
                    group_list = list(group)
                    # print(len(group_list),group_list)
                    # continue
                    line1 = [s for s in group_list if s[3] == True][0]
                    line2 = [s for s in group_list if s[3] != True][0]
                    start = line2[1]
                    end = line1[1]
                    point = line1[0]
                    dis1 = LineUtils.lineDis(start[0], start[1], point[0], point[1])
                    dis2 = LineUtils.lineDis(end[0], end[1], point[0], point[1])
                    if dis1 > dis2:
                        start = (
                        point[0] + dis2 / dis1 * (start[0] - point[0]), point[1] + dis2 / dis1 * (start[1] - point[1]))
                    else:
                        end = (
                        point[0] + dis1 / dis2 * (end[0] - point[0]), point[1] + dis1 / dis2 * (end[1] - point[1]))
                    angle = (start[0] - lon) * (end[1] - lat) - (end[0] - lon) * (start[1] - lat)
                    res2.append((key, angle))
                res2 = sorted(res2, key=lambda x: x[1])
                return res2[0][0]
        else:
            return -1
    return -1


def determineAdmin(lon: float, lat: float, needStreet=False, coordSys: CoordinateSystem = CoordinateSystem.GCJ02):
    wgs84LonLat = GeoUtils.toWGS84(lon, lat, coordSys)
    code = determineAdminCode(wgs84LonLat[0], wgs84LonLat[1])
    if code != -1:
        district = adminData.get(code)
        if district.level == 'district':
            city = adminData.get(district.parentId)
        else:
            city = district

        if city.level == 'city':
            province = adminData.get(city.parentId)
        else:
            province = city

        street_code = 0
        street_name = ""
        min_dis = 100000000
        if needStreet:
            if len(district.children) > 0:
                for s in district.children:
                    value = streetData.get(s)
                    dis = GeoUtils.distance(value.center, Location(wgs84LonLat[0], wgs84LonLat[1]))
                    if min_dis > dis:
                        min_dis = dis
                        street_code = value.id
                        street_name = value.name

        if street_code > 0:
            return Admin.createStreet(province.name, city.name, district.name, street_name, province.id, city.id,
                                      district.id, street_code, district.center)
        else:
            return Admin.createDistrict(province.name, city.name, district.name, province.id, city.id, district.id,
                                        district.center)
    else:
        return Admin.createOversea()
    return code


def getCityLevelByAdmin(admin: Admin):
    return getCityLevel(str(admin.cityCode))


def getCityLevel(adcode_or_name: str):

    cityLevel = cityLevelData.get(adcode_or_name)
    if cityLevel is not None:
        return cityLevel
    return "未知"


def getGeoInfo(lng,lat):
    """

    :param lng:
    :param lat:
    :return:
     country: str,
     province: str,
     city: str,
     district: str,
     town: str,
     level: str,
     countryCode: str,
     provinceCode: int,
     cityCode: int,
     districtCode: int,
     townCode: int,
     center: Location
     adcode_or_name:
    """
    res = determineAdmin(lng, lat, needStreet=True, coordSys=CoordinateSystem.GCJ02)
    cityLevel = getCityLevelByAdmin(res)
    return cityLevel,res.country,res.province,res.city,res.district,res.town,res.level


if __name__ == '__main__':
    # res = determineAdmin(112.989382, 28.147062, CoordinateSystem.WGS84)
    init(needBoundary=True, needArea=True, needStreet=True, needCityLevel=True)
    # 102.5 29.200000762939453这个经纬度你可以试一下嘛
    # res = determineAdmin(102.5, 29.200000762939453, needStreet=True, coordSys=CoordinateSystem.WGS84)
    res = determineAdmin(102.5, 29.200000762939453,needStreet=True,  coordSys=CoordinateSystem.GCJ02)
    # res = determineAdmin(116.9565868378, 39.6513677208, needStreet=True, coordSys=CoordinateSystem.WGS84)
    # res = determineAdmin(85.5670166016, 41.5548386631, needStreet=True, coordSys=CoordinateSystem.WGS84)
    print(res)
    # for e in [
    #     (87.6, 43.8),  # 中国台湾省南投县仁爱乡
    #     (114.2,22.3),  # 中国台湾省南投县仁爱乡
    #     (118.4,24.8),  # 中国台湾省南投县仁爱乡
    #     # (121.1572265625, 23.9260130330),  # 中国台湾省南投县仁爱乡
    #     # (112.567757, 35.096176),  # 济源
    #     # (116.9565868378, 39.6513677208),  # 天津市武清区河西务镇
    #     # (100.4315185547, 21.7594997307),  # 中国云南省西双版纳傣族自治州勐海县勐混镇
    #     # (85.5670166016, 41.5548386631),  # 中国新疆维吾尔自治区巴音郭楞蒙古自治州库尔勒市 普惠乡
    #     # (117.9969406128, 27.7447712551),  # 中国福建省南平市武夷山市 崇安街道
    #     # (110.8520507813, 34.0526594214),  # 河南省三门峡市卢氏县 瓦窑沟乡下河村
    #     # (116.4811706543, 39.9255352817),  # 北京市朝阳区 六里屯街道甜水园
    #     # (116.3362348080, 40.0622912084),  # 北京市昌平区 回龙观地区吉晟别墅社区
    #     # (116.3362830877, 40.0594500522),  # 北京市北京市昌平区 建材城西路65号
    #     # (116.3325601816, 40.0397393499),  # 北京市海淀区 清河街道
    #     # (117.0977783203, 36.5085323575),  # 山东省济南市历城区
    #     # (118.6358642578, 35.8356283889),  # 山东省临沂市沂水县
    #     # (119.7853088379, 36.3029520437),  # 山东省潍坊市高密市柏城镇
    #     # (119.8567199707, 36.2808142593),  # 山东省青岛市胶州市胶西镇
    #     # (120.3892135620, 36.2777698228),  # 山东省青岛市城阳区流亭街道于家社区
    #     # (120.152983, 36.119759),  # 海外
    #     # (98.774694, 23.706633)    # 海外
    # ]:
    #     lng, lat = e
    #     print('start', e)
    #     res = determineAdmin(lng, lat, needStreet=True, coordSys=CoordinateSystem.GCJ02)
    #     cityLevel = getCityLevelByAdmin(res)
    #     print(cityLevel, res)

    # 85.5670166016, 41.5548386631
