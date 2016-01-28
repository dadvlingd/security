/*
SQLyog Ultimate v11.24 (64 bit)
MySQL - 5.1.28-rc-community : Database - ttlwifi
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`ttlwifi` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `ttlwifi`;

/*Table structure for table `keydata` */

DROP TABLE IF EXISTS `keydata`;

CREATE TABLE `keydata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `ssid` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `createtime` varchar(24) NOT NULL,
  `country` varchar(20) NOT NULL,
  `province` varchar(20) NOT NULL,
  `city` varchar(20) NOT NULL,
  `isp` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6970 DEFAULT CHARSET=utf8;

/*Table structure for table `keydatatmp` */

DROP TABLE IF EXISTS `keydatatmp`;

CREATE TABLE `keydatatmp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(20) NOT NULL,
  `ssid` varchar(50) NOT NULL,
  `password` varchar(64) NOT NULL,
  `createtime` varchar(24) NOT NULL,
  `country` varchar(20) DEFAULT NULL,
  `province` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `isp` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
