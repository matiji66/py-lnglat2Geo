package com.dengxq.lnglat2Geo

import java.io.FileOutputStream

import com.dengxq.lnglat2Geo.GeoTransImpl.min_level
import com.dengxq.lnglat2Geo.build.{AdminDataProvider, CityAreaDataProvider, CityLevelDataProvider}
import com.dengxq.lnglat2Geo.entity.DistrictLevel.DistrictLevel
import com.dengxq.lnglat2Geo.entity.{Admin, AdminNode, BusinessAreaData, CoordinateSystem, Location}
import com.google.common.geometry.S2CellId

object MyAreaObj {

  def main(args: Array[String]): Unit = {

    GeoTrans.init(needArea=true, needCityLevel = true)
    val cityLevelData: Map[String, String] = CityLevelDataProvider.csv2Map
//
//    // ���� ��Ȧ �������������ƾ���
//    lazy val cityBusinessArea: Map[Int, Array[BusinessAreaData]] = CityAreaDataProvider.loadBusinessAreaData
//
//    lazy val adminData: Map[Int, AdminNode] = AdminDataProvider.AdminLoader.loadAdminData
//    lazy val streetData: Map[Int, AdminNode] = AdminDataProvider.AdminLoader.loadStreetData.map(s => (s.id, s)).toMap
////    val countryCode: Map[String, String] = AdminDataProvider.AdminLoader.loadCountryCode
//
//    lazy val boundaryData: Map[Long, List[(Long, Int, Int)]] = AdminDataProvider.AdminLoader.loadBoundaryData
//    lazy val boundaryIndex: Map[Long, List[Long]] = boundaryData
//      .keySet
//      .map(s => (new S2CellId(s).parent(min_level).id(), s))
//      .groupBy(_._1)
//      .map(s => (s._1, s._2.map(_._2).toList))
//
//    lazy val boundaryAdminCell: Map[Long, Int] = AdminDataProvider.AdminLoader.loadBoundaryCellData
    // println(boundaryIndex)


//    println("get boundaryAdminCell "+ boundaryAdminCell.get(3689199061258207232L) )
    println("processing adminData ")
//    var biIdx = 0
//    val fileOutputStreamBi = new FileOutputStream("boundaryIndex.txt")
//    fileOutputStreamBi.write("idx,key,values\r\n".getBytes)
//    for( key <- boundaryIndex.keys){
//        val boundaryIndexValue = boundaryIndex.get(key).get
//
//        val childrenString = boundaryIndexValue.mkString("|")
//        // key+","  == adminNode.id
//        val line = biIdx+","+  key +","+ childrenString
//      fileOutputStreamBi.write(line.getBytes)
//      fileOutputStreamBi.write("\r\n".getBytes)
//      biIdx+=1
//    }
//    fileOutputStreamBi.close()


//    var res:Admin = GeoTrans.determineAdmin(116.9565868378,39.6513677208, CoordinateSystem.WGS84)
//    println(res)
//    var res = GeoTrans.determineAdmin(102.5, 29.200000762939453, CoordinateSystem.WGS84)
    var res = GeoTrans.determineAdmin(102.5, 29.200000762939453, CoordinateSystem.GCJ02)
    // var res = GeoTrans.determineAdmin(85.5670166016, 41.5548386631, CoordinateSystem.WGS84)
    println(res)
//    val testSource = Array(
////      (121.1572265625,23.9260130330),  // �й�̨��ʡ��Ͷ���ʰ���
////      (112.567757,35.096176),         // ��Դ
//      (116.9565868378,39.6513677208), // �������������������
//      (100.4315185547,21.7594997307), // �й�����ʡ��˫���ɴ����������º����»���
//      (85.5670166016,41.5548386631),  // �й��½�ά������������������ɹ������ݿ������ �ջ���
//      (117.9969406128,27.7447712551), // �й�����ʡ��ƽ������ɽ�� �簲�ֵ�
//      (110.8520507813,34.0526594214), // ����ʡ����Ͽ��¬���� ��Ҥ�����ºӴ�
//      (116.4811706543,39.9255352817), // �����г����� �����ͽֵ���ˮ԰
//      (116.3362348080,40.0622912084), // �����в�ƽ�� �����۵������ɱ�������
//      (116.3362830877,40.0594500522), // �����б����в�ƽ�� ���ĳ���·65��
//      (116.3325601816,40.0397393499), // �����к����� ��ӽֵ�
//      (117.0977783203,36.5085323575), // ɽ��ʡ������������
//      (118.6358642578,35.8356283889), // ɽ��ʡ��������ˮ��
//      (119.7853088379,36.3029520437), // ɽ��ʡΫ���и����аس���
//      (119.8567199707,36.2808142593), // ɽ��ʡ�ൺ�н����н�����
//      (120.3892135620,36.2777698228), // ɽ��ʡ�ൺ�г�������ͤ�ֵ��ڼ�����
//      (120.152983,36.119759), // ����
//      (98.774694,23.706633) // ����
//      //    (116.3830447197,39.9467430610),  // �й������б�������������¥�����171��
//      //    (116.3854265213,39.9444070723)   // ������������ʲɲ���ֵ���������
//      // (116.3363742828, 40.0300297342) // �����к�������ӽֵ� ��ʳǹ������Ķ���
//    )
//    testSource.foreach( {
//      case (lnglat) =>
//        val admin = GeoTrans.determineAdmin(lnglat._1, lnglat._2,  CoordinateSystem.GCJ02)
//        println(lnglat, admin)
//    })
//    println("processing adminData ")
//    var adminDataIdx = 0
//    val fileOutputStreamAd = new FileOutputStream("adminData.txt")
//    fileOutputStreamAd.write("idx,key,name,shortName,center_lng,center_lat,level,parentId,children\r\n".getBytes)
//
//    //      var id: Int,
//    //      name: String,
//    //      shortName:String,
//    //      center: Location,
//    //      level: DistrictLevel,
//    //      parentId: Int,
//    //      var children: List[Int]
//    for( key <- adminData.keys){ //    Map[Int, AdminNode]
//      val adminNode: AdminNode  = adminData.get(key).get
//        val children = adminNode.children
//        val childrenString = children.mkString("|")
//        // key+","  == adminNode.id
//        val line = adminDataIdx+","+  adminNode.id+","+ adminNode.name+","+ adminNode.shortName + "," + adminNode.center.lng+","+adminNode.center.lat+","+adminNode.level+","+ adminNode.parentId+"," +childrenString
//        fileOutputStreamAd.write(line.getBytes)
//      fileOutputStreamAd.write("\r\n".getBytes)
//        adminDataIdx+=1
//
//    }
//    fileOutputStreamAd.close()

//    println("processing streetData") // Map[Int, AdminNode]
//    var streetDataIdx = 0
//    val fileOutputStreamSD = new FileOutputStream("streetData.txt")
//    fileOutputStreamSD.write("idx,id,name,shortName,center_lng,center_lat,level,parentId,children\r\n".getBytes)
//    for( key <- streetData.keys){
//      val adminNode: AdminNode  = streetData.get(key).get
//      val children = adminNode.children
//      val childrenString = children.mkString("|")
//      // key+","  == adminNode.id
//      val line = adminDataIdx+","+  adminNode.id+","+ adminNode.name+","+ adminNode.shortName + "," + adminNode.center.lng+","+adminNode.center.lat+","+adminNode.level+","+ adminNode.parentId+"," +childrenString
//
//      fileOutputStreamSD.write(line.getBytes)
//      fileOutputStreamSD.write("\r\n".getBytes)
//      streetDataIdx += 1
//    }
//    fileOutputStreamSD.close()


//    println("processing cityBusinessArea ")
////    print("res "+res)
//    var cityBusinessAreaIdx = 0
//    val fileOutputStreamCBA = new FileOutputStream("cityBusinessArea.txt")
//    fileOutputStreamCBA.write("idx,city_code,bussiness,center_lng,center_lat,area_code\r\n".getBytes)
//    for( key <- cityBusinessArea.keys){
//      val businessAreaDataS: Array[BusinessAreaData] = cityBusinessArea.get(key).get
//      for(businessAreaData <- businessAreaDataS) {
//        val line = cityBusinessAreaIdx+","+ key+"," + businessAreaData.name+","+ businessAreaData.center.lng+","+businessAreaData.center.lat+","+businessAreaData.areaCode+"\r\n"
//
//        fileOutputStreamCBA.write(line.getBytes)
//
//        cityBusinessAreaIdx+=1
//      }
//    }
//    fileOutputStreamCBA.close()

//    var idx = 0
//    val fileOutputStream = new FileOutputStream("boundaryData.txt")
//    fileOutputStream.write("idx,key,col1,col2,col3\r\n".getBytes)
//
//    for(key <- boundaryData.keys ){
//      val boundaryDataList: List[(Long,Int,Int)] = boundaryData.get(key).get
//      for(boundaryDataElement <- boundaryDataList) {
//        if( idx % 10000 == 0){
//          println(idx+","+ key+"," + boundaryDataElement._1+","+ boundaryDataElement._2 +","+boundaryDataElement._3 )
//        }
//        val line = idx+","+ key+"," + boundaryDataElement._1+","+ boundaryDataElement._2 +","+boundaryDataElement._3+"\r\n"
//        fileOutputStream.write( line.getBytes)
//        idx+=1
//      }
//    }
//    fileOutputStream.close()


//    var bc_idx = 0
//    val fileOutputStreamBAC = new FileOutputStream("boundaryAdminCell.txt")
//
//    fileOutputStreamBAC.write("idx,key,col1\r\n".getBytes)
//
//    for(key <- boundaryAdminCell.keys ){
//      val boundaryAdminCellValue: Int = boundaryAdminCell.get(key).get
//
//        if( bc_idx % 10000 == 0){
//          println(bc_idx+","+ key+"," + boundaryAdminCellValue  )
//        }
//        val line = bc_idx+","+ key+"," + boundaryAdminCellValue +"\r\n"
//        fileOutputStreamBAC.write(line.getBytes)
//        bc_idx+=1
//    }
//
//    fileOutputStreamBAC.close()



  }

}
