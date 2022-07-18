import math
from s2sphere import LatLng, Angle

from geo_obj import Location, CoordinateSystem

x_PI = math.pi * 3000.0 / 180.0
EE = 0.00669342162296594323
A = 6378245.0  # BJZ54坐标系地球长半轴, m
EQUATOR_C = 20037508.3427892  # 赤道周长, m
EARTH_RADIUS = 6378137.0  # WGS84, CGCS2000坐标系地球长半轴, m
EARTH_POLAR_RADIUS = 6356725.0  # 极半径, m

SQRT2 = 1.414213562


def outOfChina(lng, lat):
    return lng < 72.004 or lng > 137.8347 or lat < 0.8293 or lat > 55.8271


def transformLat(lng: float, lat: float):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + 0.1 * lng * lat + 0.2 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 * math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 * math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def transformLng(lng: float, lat: float):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + 0.1 * lng * lat + 0.1 * math.sqrt(abs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 * math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 * math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 * math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def rad(d: float):
    return d * math.pi / 180.0


def get_earth_dist(locA: LatLng, locB: LatLng, radius=6367000.0):
    """
    :param locA:
    :param locB:
    :param radius:
    :return:
    """
    lat1 = locA.lat().radians;
    lat2 = locB.lat().radians;
    lng1 = locA.lng().radians;
    lng2 = locB.lng().radians;
    dlat = math.sin(0.5 * (lat2 - lat1));
    dlng = math.sin(0.5 * (lng2 - lng1));
    x = dlat * dlat + dlng * dlng * math.cos(lat1) * math.cos(lat2);
    dis = (2.0 * math.atan2(math.sqrt(x), math.sqrt(max(0.0, 1.0 - x))))
    dist = dis * radius
    return dist


def get_earth_distance(locA: LatLng, locB: LatLng):
    """
    :param locA: .degrees or radians
    :param locB:
    :return:
    """
    try:
        # print(f'locA={locA},locB={locB}')
        lngA = float(str(locA).split(',')[1])
        latA = float(str(locA).split(',')[0].split(" ")[1])

        lngB = float(str(locB).split(',')[1])
        latB = float(str(locB).split(',')[0].split(" ")[1])

        f = rad((latA + latB) / 2)
        g = rad((latA - latB) / 2)
        l = rad((lngA - lngB) / 2)
        if g == 0 and l == 0:
            return 0
        sg = math.sin(g)
        sl = math.sin(l)
        sf = math.sin(f)
        s = .0
        c = .0
        w = .0
        r = .0
        d = .0
        h1 = .0
        h2 = .0
        dis = .0
        a = EARTH_RADIUS
        fl = 1 / 298.257
        sg = sg * sg
        sl = sl * sl
        sf = sf * sf
        s = sg * (1 - sl) + (1 - sf) * sl
        c = (1 - sg) * (1 - sl) + sf * sl
        w = math.atan(math.sqrt(s / c))
        r = math.sqrt(s * c) / w
        d = 2 * w * a
        h1 = (3 * r - 1) / 2 / c
        h2 = (3 * r + 1) / 2 / s
        dis = d * (1 + fl * (h1 * sf * (1 - sg) - h2 * (1 - sf) * sg))
    except:
        print('get_earth_distance failed')
        return -1
    return float(f"{dis:.2f}")


def distance(locA: Location, locB: Location):
    lngA = locA.lng
    latA = locA.lat
    lngB = locB.lng
    latB = locB.lat
    f = rad((latA + latB) / 2)
    g = rad((latA - latB) / 2)
    l = rad((lngA - lngB) / 2)
    if (g == 0 and l == 0):
        return 0
    sg = math.sin(g)
    sl = math.sin(l)
    sf = math.sin(f)
    s = .0
    c = .0
    w = .0
    r = .0
    d = .0
    h1 = .0
    h2 = .0
    dis = .0
    a = EARTH_RADIUS
    fl = 1 / 298.257
    sg = sg * sg
    sl = sl * sl
    sf = sf * sf
    s = sg * (1 - sl) + (1 - sf) * sl
    c = (1 - sg) * (1 - sl) + sf * sl
    w = math.atan(math.sqrt(s / c))
    r = math.sqrt(s * c) / w
    d = 2 * w * a
    h1 = (3 * r - 1) / 2 / c
    h2 = (3 * r + 1) / 2 / s
    dis = d * (1 + fl * (h1 * sf * (1 - sg) - h2 * (1 - sf) * sg))

    return float(f"{dis:.2f}")


def wgs84ToGCj02(lng: float, lat: float):
    """

    :param lng:
    :param lat:
    :return:
    """
    mglat = .0
    mglng = .0

    if outOfChina(lng, lat):
        mglat = lat
        mglng = lng

    else:
        dLat = transformLat(lng - 105.0, lat - 35.0)
        dLon = transformLng(lng - 105.0, lat - 35.0)
        radLat = lat / 180.0 * math.pi
        magic = math.sin(radLat)
        magic = 1 - EE * magic * magic
        sqrtMagic = math.sqrt(magic)
        dLat = (dLat * 180.0) / ((A * (1 - EE)) / (magic * sqrtMagic) * math.pi)
        dLon = (dLon * 180.0) / (A / sqrtMagic * math.cos(radLat) * math.pi)
        mglat = lat + dLat
        mglng = lng + dLon

    return mglng, mglat


def toGCJ02(lng: float, lat: float, coordType: CoordinateSystem):
    """
    判断坐标系转换
    :param lng:
    :param lat:
    :param coordType:
    :return:
    """
    if coordType.value == CoordinateSystem.WGS84.value:
        d = wgs84ToGCj02(lng, lat)
        return d
    if coordType.value == CoordinateSystem.BD09.value:
        d = bd09ToGCJ02(lng, lat)
        return d
    return lng, lat


def gcj02ToWgs84(lng: float, lat: float):
    if outOfChina(lng, lat):
        return lng, lat
    dlat = transformLat(lng - 105.0, lat - 35.0)
    dlng = transformLng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - EE * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((A * (1 - EE)) / (magic * sqrtmagic) * math.pi)
    dlng = (dlng * 180.0) / (A / sqrtmagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat


def toWGS84(lng: float, lat: float, coordType: CoordinateSystem):
    """
    判断坐标系转换
    :type lat: object
    :param lng:
    :param lat:
    :param coordType:
    :return:
    """
    # print("CoordinateSystem.GCJ02 compare", coordType == CoordinateSystem.GCJ02,dir(coordType),dir(CoordinateSystem.GCJ02))
    if coordType.value == CoordinateSystem.GCJ02.value:
        return gcj02ToWgs84(lng, lat)
    elif coordType.value == CoordinateSystem.BD09.value:
        d02 = bd09ToGCJ02(lng, lat)
        return gcj02ToWgs84(d02[0], d02[0])
    else:
        return lng, lat


def bd09ToGCJ02(lng: float, lat: float):
    if outOfChina(lng, lat):
        return lng, lat
    x = lng - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_PI)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return gg_lng, gg_lat
