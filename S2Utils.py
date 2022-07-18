import math
from s2sphere import Cap
from s2sphere import RegionCoverer
from s2sphere import *

kEarthCircumferenceMeters = 1000 * 40075.017


def earthMeters2Radians(meters: float)  :
    return (2 * math.pi) * (meters / 40075017)


# // 预算，提升速度
def earthMeters2Radians_(radius):
    rad = earthMeters2Radians(radius * 1000)
    return radius * 1000, rad * rad * 2


capHeightMap_ = map(lambda radius:earthMeters2Radians_(radius),[2, 4, 8, 16, 32, 64, 128, 256])
capHeightMap = {}
for e1,e2 in capHeightMap_:
    capHeightMap[e1] = e2
print(capHeightMap)


def getLevel(inputs: int):
    """
    :param inputs:
    :return:
    """
    n = 0
    input = inputs
    # print(input, inputs)
    while input % 2 == 0:
        input = input / 2
        n += 1
    return 30 - n / 2


def getCellId(s2LatLng: LatLng, radius: int, desLevel: int):

    capHeight = capHeightMap.get(radius) if capHeightMap.get(radius) else 0

    cap = Cap.from_axis_height(s2LatLng.to_point(), capHeight)

    coverer = RegionCoverer()
    coverer.min_level = desLevel
    coverer.max_level = desLevel
    """
    >>> a = A()
    >>> getattr(a, 'bar')          # 获取属性 bar 值
    >>> setattr(a, 'bar', 5)       # 设置属性 bar 值
    """
    #  圆形内的cell会自动做聚合，手动拆分

    res = []
    cellIds = coverer.get_covering(cap)

    for s2CellId in cellIds:
        cellLevel = getLevel(s2CellId.id())
        if (cellLevel == desLevel):
            res.append(s2CellId.id())
        else:
            res.extend([cellid.id() for cellid in childrenCellId(s2CellId, cellLevel, desLevel)])
    return res


def childrenCellId(s2CellId: CellId, curLevel: int, desLevel: int):
    list = []
    if (curLevel < desLevel) :
      inter= (s2CellId.childEnd.id - s2CellId.childBegin.id) / 4
      for i in range(0,5):
          id = s2CellId.childBegin.id + inter * i
          cellId = CellId(id)
          list.append( childrenCellId(cellId, curLevel + 1, desLevel))
    else:
        list.append(s2CellId)
    return list


if __name__ == '__main__':
    getLevel(100)