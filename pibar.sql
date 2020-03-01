-- MySQL dump 10.16  Distrib 10.2.29-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: pibar
-- ------------------------------------------------------
-- Server version	10.2.29-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `idadmin` int(11) NOT NULL AUTO_INCREMENT,
  `befehl` varchar(25) NOT NULL,
  PRIMARY KEY (`idadmin`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'test'),(2,'haus'),(3,'Storno');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tagid` varchar(255) NOT NULL,
  `firstName` varchar(255) CHARACTER SET latin1 NOT NULL,
  `lastName` varchar(255) CHARACTER SET latin1 NOT NULL,
  `admin` tinyint(4) NOT NULL DEFAULT 0,
  `usergroup` int(11) DEFAULT 0,
  `userCard` varchar(25) NOT NULL,
  `balance` decimal(7,2) DEFAULT 0.00,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tagid` (`tagid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'21223190229','Tom','Erber',0,0,'User Card 1',0.00),(2,'16515423243','Maria','Mustermann',0,0,'User Card 2',0.00),(3,'1571996217','Max','Mustermann',0,1,'User Card 3',15.00),(4,'1092486217','Hans','Wurst',0,0,'User Card 4',0.00),(5,'1411616217','Noch','Jemand',0,0,'User Card 5',0.00),(6,'29217250216','Irgend','Jemand',0,0,'User Card 6',0.00),(7,'2021138235','Admin','Key',1,0,'Admin Key 2',0.00),(8,'13218111626','Tom','Erber',1,0,'Admin Key 1',0.00),(9,'244201232230','01:57:37','Blanko',0,0,'01:57:37',0.00),(10,'1512082169','01:57:50','Blanko',0,0,'01:57:50',0.00);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `orderDate` timestamp NOT NULL DEFAULT current_timestamp(),
  `customerId` int(11) NOT NULL,
  `productId` int(11) NOT NULL,
  `isPaid` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'2014-10-31 20:30:50',1,24,1),(2,'2014-10-31 20:31:00',2,24,1),(3,'2014-10-31 20:31:09',3,24,1),(6,'2014-11-07 19:56:58',1,30,1),(7,'2014-11-07 19:57:07',3,30,1),(8,'2014-11-07 20:45:42',3,36,1),(9,'2014-11-07 20:45:51',1,36,1),(10,'2014-11-15 19:41:59',1,30,1),(11,'2014-11-15 19:48:09',2,3,1),(12,'2014-11-15 20:27:39',2,24,1),(13,'2014-11-15 20:27:49',2,24,1),(14,'2014-11-15 20:27:58',1,24,1),(15,'2014-11-30 01:22:54',1,11,1),(17,'2014-12-06 20:39:43',1,31,1),(21,'2014-12-11 18:39:09',1,26,1),(22,'2014-12-11 18:39:45',1,26,1),(25,'2014-12-11 19:02:31',2,6,1),(26,'2014-12-27 20:30:46',1,24,1),(27,'2014-12-27 20:31:08',1,40,1),(28,'2014-12-27 20:31:31',2,24,1),(29,'2014-12-27 20:31:43',3,40,1),(33,'2014-12-31 19:27:03',1,24,0),(34,'2014-12-31 19:27:12',3,24,0),(35,'2014-12-31 19:45:44',5,41,1),(36,'2014-12-31 19:48:35',2,24,0),(37,'2014-12-31 19:56:40',1,24,0),(38,'2014-12-31 20:31:01',3,40,0),(40,'2014-12-31 20:32:51',2,46,0),(41,'2014-12-31 20:33:01',4,46,0),(42,'2014-12-31 20:35:26',5,26,1),(43,'2014-12-31 20:36:48',6,25,1),(44,'2014-12-31 20:38:04',1,46,0),(45,'2014-12-31 20:39:29',4,11,0),(46,'2014-12-31 21:20:06',1,36,0),(47,'2014-12-31 21:20:21',2,36,0),(48,'2014-12-31 21:48:47',3,37,0),(49,'2014-12-31 22:00:09',4,33,0),(50,'2014-12-31 22:11:50',6,26,1),(51,'2014-12-31 23:35:50',1,26,0),(52,'2014-12-31 23:56:43',5,11,1),(53,'2015-01-01 00:42:54',4,11,0),(54,'2015-01-01 00:44:16',2,24,0),(55,'2015-01-01 00:54:09',6,25,1),(56,'2015-01-01 01:48:25',1,24,0),(57,'2015-01-01 02:28:19',1,46,0),(58,'2015-01-01 02:28:29',1,46,0);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ean` varchar(13) CHARACTER SET latin1 NOT NULL,
  `name` varchar(255) CHARACTER SET latin1 NOT NULL,
  `price` decimal(13,2) NOT NULL,
  `stock` int(10) unsigned NOT NULL,
  `drinktype` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ean` (`ean`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (2,'42111702','BECK\'S GREEN LEMON',1.00,4,2),(3,'4025127016938','SALITOS ICE',1.50,4,2),(4,'42150213','BECK\'S TWISTED ORANGE',1.00,2,2),(5,'75033927','Corona Extra',1.50,2,2),(6,'41001301','BECK\'S ',1.00,4,2),(7,'42178194','BECK\'S LIME',1.00,2,2),(8,'4053400273358','Schöfferhofer HEFEWEITZEN',1.00,2,2),(11,'4014086093432','2,5 ORGINAL RADLER',0.50,24,2),(12,'4014086093364','5,0 ORGINAL PILS',0.50,24,2),(13,'4014086093333','5,0 ORGINAL EXPORT ',0.50,24,2),(14,'4025127020997','EFFECT ENERGY DRINK',1.00,2,2),(15,'5000112546415','Coca Cola',0.50,100,1),(16,'5000112547726','Coca Cola',0.50,100,1),(17,'87126853','Coca Cola Flasche',0.90,24,1),(18,'90162565','Red Bull ENERGY DRINK',1.50,24,2),(19,'4004752252492','Kleiner Feigling',1.00,10,2),(20,'4009415262191','Holla die Waldfee',0.50,10,2),(47,'0','Leitungswasser',0.00,123,0);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-01-13 17:36:36
