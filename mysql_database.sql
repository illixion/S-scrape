# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.6.49)
# Database: sscrape
# Generation Time: 2020-08-08 23:24:12 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table destination
# ------------------------------------------------------------

DROP TABLE IF EXISTS `destination`;

CREATE TABLE `destination` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` text,
  `price` int(11) DEFAULT NULL,
  `model` text,
  `year` int(4) DEFAULT NULL,
  `engine` text,
  `transmission` text,
  `km_travelled` int(11) DEFAULT NULL,
  `color_hex` text,
  `type` text,
  `inspection_until` text,
  `vin` text,
  `plate_no` text,
  `features` text,
  `phone` text,
  `listing_images` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table source
# ------------------------------------------------------------

DROP TABLE IF EXISTS `source`;

CREATE TABLE `source` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` text CHARACTER SET latin1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
