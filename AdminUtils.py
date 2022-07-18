# -*- coding: utf-8 -*-


import re

NATIONS = "阿昌族,鄂温克族,傈僳族,水族,白族,高山族,珞巴族,塔吉克族,保安族,仡佬族,满族,塔塔尔族,布朗族,哈尼族,毛南族,土家族,布依族,哈萨克族,门巴族,土族,朝鲜族,汉族,蒙古族,佤族,达斡尔族,赫哲族,苗族,维吾尔族,傣族,回族,仫佬族,乌孜别克族,德昂族,基诺族,纳西族,锡伯族,东乡族,京族,怒族,瑶族,侗族,景颇族,普米族,彝族,独龙族,柯尔克孜族,羌族,裕固族,俄罗斯族,拉祜族,撒拉族,藏族,鄂伦春族,黎族,畲族,壮族".split(
    ",")

p1 = """(.+)(?:省|市)"""
p2 = """(.+)自治区"""
p3 = """(.+)特别行政区"""

c0 = """^(.{2})$"""  # 2 长度为2的 "东区" "南区"
c1 = """(.+)(?:自治州|自治县)$"""  # 30 自治州  琼中黎族苗族自治县
c2 = """(.+)[市|盟|州]$"""  # 304 地级市, 盟; + 1恩施州
c3 = """(.+)地区$"""  # 8 地区
c4 = """(.+)(?:群岛|填海区)$"""  # 2 东沙群岛
c5 = """(.+[^地郊城堂])区$"""  # 20 港澳 不含"东区" "南区"2个字的
c6 = """(.+)(?:城区|郊县)$"""  # 6 九龙城区,上海城区,天津城区,北京城区,重庆城区,重庆郊县
c7 = """(.+[^郊])县$"""  # 12 台湾的xx县

d0 = """^(.{2})$"""  # 2 长度为2的 "随县"
d1 = """(.+)[市]$"""  # 304 城区 “赤水市”
d2 = """(.+)自治县$"""  # 30 自治县
d3 = """(.+)自治州直辖$"""  # 30 自治州直辖 "海西蒙古族藏族自治州直辖"
d4 = """(.+)[区|县]$"""  # 8 区县
d5 = """(.+)(?:乡|镇|街道)$"""  # 8 乡镇|街道

s0 = """^(.{2})$"""
s1 = """(.+)(?:特别行政管理区|街道办事处|旅游经济特区|民族乡|地区街道)$"""
s2 = """(.+)(?:镇|乡|村|街道|苏木|老街|管理区|区公所|苏木|办事处|社区|经济特区|行政管理区)$"""


def replaceNations(ncity: str):
    for e in NATIONS:
        ncity = ncity.replace(e, '')
    return ncity

    # return zip([ncity] ++ NATIONS).reduce((x, y) => x.replaceAll(y, "").replaceAll(if(y.length > 2) y.replaceAll("族", "") else "", ""))


def shortProvince(province: str):
    # (.+)特别行政区
    # (.+省|.+自治区)(.+市)
    res = re.match(p1, province, flags=0)
    if res:
        return res.group()

    res = re.match(p2, province, flags=0)
    if res:
        return res.group()

    res = re.match(p3, province, flags=0)
    if res:
        return res.group()
    # case p1(x) => x
    # case p2(x) => if(x== "内蒙古") x else replaceNations(x)
    # case p3(x) => x
    # case _ => province

    return province


def shortCityImp(city: str):
    """
    :param city:
    :return: (city,-1)
    """
    # 总数 383
    if re.match(c0, city, flags=0):
        return re.match(c0, city, flags=0).group(), 0
    elif re.match(c1, city, flags=0):
        return re.match(c1, city, flags=0).group(), 1
    elif re.match(c2, city, flags=0):
        return re.match(c2, city, flags=0).group(), 2
    elif re.match(c3, city, flags=0):
        return re.match(c3, city, flags=0).group(), 3
    elif re.match(c4, city, flags=0):
        return re.match(c4, city, flags=0).group(), 4
    elif re.match(c5, city, flags=0):
        return re.match(c5, city, flags=0).group(), 5
    elif re.match(c6, city, flags=0):
        return re.match(c6, city, flags=0).group(), 6
    elif re.match(c7, city, flags=0):
        return re.match(c7, city, flags=0).group(), 7

    # case c0(x) => (x, 0)
    # case c1(x) => (replaceNations(x), 2)
    # case c2(x) => if(x == "襄樊") ("襄阳",1) else (x, 1)
    # case c3(x) => (x,3)
    # case c4(x) => (x,4)
    # case c5(x) => (x,5)
    # case c6(x) => (x,6)
    # case c7(x) => (x,7)
    # case _ => (city, -1)
    return city, -1


def shortDistrictImp(district: str):
    """
    
    :param district: 
    :return: (String, Int) 
    """
    # // 总数 2963 56个内蒙八旗和新疆兵团没有处理
    if re.match(d0, district, flags=0):
        return re.match(d0, district, flags=0).group()
    elif re.match(d1, district, flags=0):
        return re.match(d1, district, flags=0).group()
    elif re.match(d2, district, flags=0):
        return replaceNations(re.match(d2, district, flags=0).group()),2
    elif re.match(d3, district, flags=0):
        return replaceNations(re.match(d3, district, flags=0).group()),3
    elif re.match(d4, district, flags=0):
        return re.match(d4, district, flags=0).group()
    elif re.match(d5, district, flags=0):
        return re.match(d5, district, flags=0).group()
    # match {
    #  case d0(x) => (x, 0)
    #  case d1(x) => (x, 1)
    #  case d2(x) => (replaceNations(x), 2)
    #  case d3(x) => (replaceNations(x), 3)
    #  case d4(x) => (x,4)
    #  case d5(x) => (x,5)
    #  case _ => (district, -1)


def replaceNationsNotEmpty(name: str):
    for e in NATIONS:
        name_ = name.replace(e, '').replace(e.replace('族', ''))
        if len(name_) >= 0:
            name = name_
    return name


def shortStreetImp(street: str):
    """
    :param street:
    :return:
    """
    # // 总数 42387
    # // 柘城县邵园乡人民政府, 保安镇, 鹅湖镇人民政府, 东风地区
    if re.match(s0, street, flags=0):
        return re.match(s0, street, flags=0).group(), 0
    elif re.match(s1, street, flags=0):
        return replaceNationsNotEmpty(re.match(s1, street, flags=0).group()), 1
    elif re.match(s2, street, flags=0):
        return replaceNationsNotEmpty(re.match(s2, street, flags=0).group()), 2
    # street match {
    #   case s0(x) => (x, 0)
    #   case s1(x) => (replaceNationsNotEmpty(x), 1)
    #   case s2(x) => (replaceNationsNotEmpty(x), 2)
    #   case _ => (street, -1)
    # }
    return street, -1


if __name__ == '__main__':
    shortProvince("安徽省宿州市埇桥区")
    shortProvince("天津市")
    shortProvince("内蒙古自治区")
    shortProvince("香港特别行政区")
