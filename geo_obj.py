# coding=utf-8
from enum import Enum, unique

# from geo import AdminUtils
import AdminUtils

CHINA_NAME = "中国"
CHINA_ID = "CN"
OVERSEA_NAME_VAL = "海外"
UNKNOWN_NAME_VAL = "未知"
UNKNOWN_ID_VAL = -1
UNKNOWN_LOCATION_VAL = None


@unique
class CoordinateSystem(Enum):
    #
    WGS84 = 0  # GPS
    # 坐标系
    GCJ02 = 1  # 国测局坐标系(火星坐标系)
    BD09 = 2  # 百度坐标系
    BJ54 = 3  # 北京54坐标系
    XIAN80 = 4  # 西安80坐标系
    CGCS2000 = 5  # 2000
    # 国家大地坐标系
    XYZ = 6  # 笛卡尔坐标系
    MERCATOR = 7  # 墨卡托坐标系


@unique
class DistrictLevel(Enum):
    # / ** 国家 ** /
    Country = "country"
    # / ** 省, 自治区 ** /
    Province = "province"
    # / ** 地级市 ** /
    City = "city"
    # / ** 区, 县, 县级市 ** /
    District = "district"
    # / ** 街道 ** /
    Street = "street"


@unique
class AdminLevel(Enum):
    # / ** 海外 ** /
    Oversea = "oversea"
    # / ** 国家 ** /
    Country = "country"
    # / ** 省, 自治区 ** /
    Province = "province"
    # / ** 地级市 ** /
    City = "city"
    # / ** 省辖市(属县级市)
    # see: https: // baike.baidu.com / item / 省直辖县级行政单位 ** /
    ProvincialCity = "provincialcity"
    # / ** 区, 县, 县级市 ** /
    District = "district"
    # / ** 街道 ** /
    Street = "street"


class S2LatLng(object):
    def __init__(self, ):
        super(S2LatLng, self).__init__()


class Location(object):
    def __init__(self, lng: float, lat: float):
        super().__init__()
        self.lng = lng
        self.lat = lat

    def __str__(self):
        return f"Location({self.lng},{self.lat})"


class Admin(object):

    def __init__(self, country: str,
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
                 center: Location = None):
        super(Admin, self).__init__()
        self.country = country
        self.province = province
        self.city = city
        self.district = district
        self.town = town
        self.level = level
        self.countryCode = countryCode
        self.provinceCode = provinceCode
        self.cityCode = cityCode
        self.districtCode = districtCode
        self.townCode = townCode
        self.center = center

    def __str__(self):
        return f"Admin({self.country},{self.province},{self.city},{self.district},{self.town},{self.level}" \
         + f",{self.countryCode},{self.provinceCode},{self.cityCode},{self.districtCode},{self.townCode},{self.center})"

    def hasCenter(self):
        return self.center != Admin.UNKNOWN_LOCATION_VAL

    def hasProvince(self):
        return self.province != Admin.UNKNOWN_NAME_VAL

    def hasCity(self):
        return self.city != Admin.UNKNOWN_NAME_VAL

    def hasDistrict(self):
        return self.district != Admin.UNKNOWN_NAME_VAL

    def hasCityId(self):
        return self.cityCode != Admin.UNKNOWN_ID_VAL

    def hasDistrictId(self):
        return self.districtCode != Admin.UNKNOWN_ID_VAL

    def hasTown(self):
        return self.town != Admin.UNKNOWN_NAME_VAL

    def shortProvince(self):
        return AdminUtils.shortProvince(self.province)

    def shortCity(self):
        return AdminUtils.shortCity(self.city)

    def toShort(self):
        return self.Admin(self.country,
                          AdminUtils.shortProvince(self.province),
                          AdminUtils.shortCity(self.city),
                          AdminUtils.shortDistrict(self.district),
                          AdminUtils.shortStreet(self.town),
                          self.level, self.countryCode, self.provinceCode,
                          self.cityCode, self.districtCode, self.townCode, self.center)

    def toNamestr(self):
        return f"$country${self.province if (self.hasProvince()) else ''} " \
               + f"{self.city if (self.hasCity()) else ''}${self.district if (self.hasDistrict()) else ''}" \
               + f"$ {self.town if (self.hasTown()) else ''}"

    @staticmethod
    def createOversea():
        return Admin(OVERSEA_NAME_VAL,
                     province=OVERSEA_NAME_VAL,
                     city=OVERSEA_NAME_VAL,
                     district=OVERSEA_NAME_VAL,
                     town=OVERSEA_NAME_VAL,
                     level=AdminLevel.Oversea,
                     countryCode="",
                     provinceCode=UNKNOWN_ID_VAL,
                     cityCode=UNKNOWN_ID_VAL,
                     districtCode=UNKNOWN_ID_VAL,
                     townCode=UNKNOWN_ID_VAL,
                     center=UNKNOWN_LOCATION_VAL
                     )

    @staticmethod
    def createCountry(country: str, countryID: str, center: Location):
        return Admin(
            country,
            province=UNKNOWN_NAME_VAL,
            city=UNKNOWN_NAME_VAL,
            district=UNKNOWN_NAME_VAL,
            town=UNKNOWN_NAME_VAL,
            level=AdminLevel.Country,
            countryCode=countryID,
            provinceCode=UNKNOWN_ID_VAL,
            cityCode=UNKNOWN_ID_VAL,
            districtCode=UNKNOWN_ID_VAL,
            townCode=UNKNOWN_ID_VAL,
            center=center
        )

    @staticmethod
    def createProvince(province: str, provinceId: int, center: Location):
        return Admin(
            country=CHINA_NAME,
            province=province,
            city=UNKNOWN_NAME_VAL,
            district=UNKNOWN_NAME_VAL,
            town=UNKNOWN_NAME_VAL,
            level=AdminLevel.Province,
            countryCode=CHINA_ID,
            provinceCode=provinceId,
            cityCode=UNKNOWN_ID_VAL,
            districtCode=UNKNOWN_ID_VAL,
            townCode=UNKNOWN_ID_VAL,
            center=center
        )

    @staticmethod
    def createCity(province: str, city: str, provinceId: int, cityId: int, center: Location):
        return Admin(
            country=CHINA_NAME,
            province=province,
            city=city,
            district=UNKNOWN_NAME_VAL,
            town=UNKNOWN_NAME_VAL,
            level=AdminLevel.City,
            countryCode=CHINA_ID,
            provinceCode=provinceId,
            cityCode=cityId,
            districtCode=UNKNOWN_ID_VAL,
            townCode=UNKNOWN_ID_VAL,
            center=center
        )

    @staticmethod
    def createProvincialCity(province: str, city: str, provinceId: int, cityId: int, center: Location):
        return Admin(
            country=CHINA_NAME,
            province=province,
            city=city,
            district=city,
            town=UNKNOWN_NAME_VAL,
            level=AdminLevel.ProvincialCity,
            countryCode=CHINA_ID,
            provinceCode=provinceId,
            cityCode=cityId,
            districtCode=cityId,
            townCode=UNKNOWN_ID_VAL,
            center=center
        )

    @staticmethod
    def createDistrict(province: str, city: str, district: str,
                       provinceId: int, cityId: int, districtId: int, center: Location):
        return Admin(
            country=CHINA_NAME,
            province=province,
            city=city,
            district=district,
            town=UNKNOWN_NAME_VAL,
            level=AdminLevel.District,
            countryCode=CHINA_ID,
            provinceCode=provinceId,
            cityCode=cityId,
            districtCode=districtId,
            townCode=UNKNOWN_ID_VAL,
            center=center
        )

    @staticmethod
    def createStreet(province: str, city: str, district: str, town: str,
                     provinceId: int, cityId: int, districtId: int, streetId: int, center: Location):
        return Admin(
            country=CHINA_NAME,
            province=province,
            city=city,
            district=district,
            town=town,
            level=AdminLevel.Street,
            countryCode=CHINA_ID,
            provinceCode=provinceId,
            cityCode=cityId,
            districtCode=districtId,
            townCode=streetId,
            center=center
        )


class AdminNode(object):
    def __init__(self, id: int,
                 name: str,
                 shortName: str,
                 center: Location,
                 level: DistrictLevel,
                 parentId: int,
                 children: list):
        super().__init__()
        self.id = id
        self.name = name
        self.shortName = shortName
        self.center = center
        self.parentId = parentId
        self.level = level
        self.children = children

    def __str__(self):
        """
        :return: AdminNode(430000,湖南省,湖南,Location(112.9836,28.112743),province,100000,List(430700, 431000, 430400, 431300, 430500, 433100, 430300, 431100, 430900, 430800, 430200, 430600, 430100, 431200))
        """
        return f"AdminNode({self.id},{self.name},{self.shortName},{self.center},{self.level},{self.children})"


class BusinessAreaData(object):
    def __init__(self, name: str, center: Location, areaCode: int):
        super().__init__()
        self.name = name
        self.center = center
        self.areaCode = areaCode


class BusinessAreaGroup(object):
    # list(BusinessAreaData)
    def __init__(self, cityAdCode: int, areas):
        super().__init__()
        self.cityAdCode = cityAdCode
        self.areas = areas


class BusinessArea(object):
    def __init__(self,
                 name: str, areaCode: int, distance: int):
        super().__init__()
        self.name = name
        self.areaCode = areaCode
        self.distance = distance


class BusinessAreaInfo(object):
    def __init__(self, admin: Admin, areas):  # : list(BusinessArea)
        super().__init__()
        self.admin = admin
        self.areas = areas

# case class BusinessAreaData(name: str, center: Location, areaCode: int) extends Serializable
#
# @SerialVersionUID(-5899680396800964972L)
# case class BusinessAreaGroup(cityAdCode: int, areas: Array[BusinessAreaData]) extends Serializable
#
# case class BusinessArea(name: str, areaCode: int, distance:int)
#
# case class BusinessAreaInfo(admin: Admin, areas: Seq[BusinessArea])


if __name__ == '__main__':
    print(CoordinateSystem.GCJ02 ==CoordinateSystem.GCJ02)
