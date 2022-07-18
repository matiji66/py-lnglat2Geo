# // 计算两点之间的距离

import math


def lineDis(x1: float, y1: float, x2: float, y2: float):
    return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def pointToLineDis(x1: float, y1: float, x2: float, y2: float, x0: float, y0: float):
    a = lineDis(x1, y1, x2, y2)  # 线段的长度
    b = lineDis(x1, y1, x0, y0)  # 点到起点的距离
    c = lineDis(x2, y2, x0, y0)  # 点到终点的距离
    # 点在端点上
    if c <= 0.000001 or b <= 0.000001:
        return 0

    # 直线距离过短
    if a <= 0.000001:
        return b

    #  点在起点左侧，距离等于点到起点距离
    if c * c >= a * a + b * b:
        return b

    # 点在终点右侧，距离等于点到终点距离
    if b * b >= a * a + c * c:
        return c
    # 点在起点和终点中间，为垂线距离
    # k = (y2 - y1) / (x2 - x1)
    # z = y1 - k * x1
    p = (a + b + c) / 2
    #  半周长
    s = math.sqrt(p * (p - a) * (p - b) * (p - c))  # 海伦公式求面积
    dis = 2 * s / a  # 回点到线的距离（利用三角形面积公式求高）
    return dis
