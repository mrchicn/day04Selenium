/*
Navicat MySQL Data Transfer

Source Server         : 172.20.5.134_3306
Source Server Version : 50725
Source Host           : 172.20.5.134:3306
Source Database       : Python_db

Target Server Type    : MYSQL
Target Server Version : 50725
File Encoding         : 65001

Date: 2019-04-03 17:00:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for TB_Books
-- ----------------------------
DROP TABLE IF EXISTS `TB_Books`;
CREATE TABLE `TB_Books` (
  `book_Image_Url` varchar(255) DEFAULT NULL COMMENT '书的图片',
  `book_Address` varchar(255) DEFAULT NULL COMMENT '书的地址',
  `book_Price` varchar(255) DEFAULT NULL COMMENT '书的价格',
  `book_Count` varchar(255) DEFAULT NULL COMMENT '销售的数量',
  `book_Title` varchar(255) DEFAULT NULL COMMENT '书的标题',
  `book_Shop_Address` varchar(255) DEFAULT NULL COMMENT '店铺地址',
  `shop_locate` varchar(255) DEFAULT NULL COMMENT '店铺的位置'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
