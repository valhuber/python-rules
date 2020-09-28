CREATE DATABASE  IF NOT EXISTS `banking` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `banking`;
-- MySQL dump 10.13  Distrib 8.0.17, for macos10.14 (x86_64)
--
-- Host: 127.0.0.1    Database: banking
-- ------------------------------------------------------
-- Server version	8.0.16

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ALERT`
--

DROP TABLE IF EXISTS `ALERT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ALERT` (
  `AlertID` mediumint(9) NOT NULL AUTO_INCREMENT,
  `CustNum` mediumint(9) NOT NULL,
  `AcctNum` mediumint(9) NOT NULL,
  `WhenBalance` decimal(10,2) NOT NULL,
  `AccountBalance` decimal(10,2) DEFAULT NULL,
  `EmailAddress` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AlertID`),
  KEY `fk_Alert_CUSTOMER1_idx` (`CustNum`),
  KEY `idx_alter_custAcct` (`CustNum`,`AcctNum`),
  CONSTRAINT `fk_Alert_CUSTOMER1` FOREIGN KEY (`CustNum`) REFERENCES `CUSTOMER` (`CustNum`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ALERT`
--

LOCK TABLES `ALERT` WRITE;
/*!40000 ALTER TABLE `ALERT` DISABLE KEYS */;
INSERT INTO `ALERT` VALUES (1,1,1,1000.00,0.00,'tylerm007@gmail.com');
/*!40000 ALTER TABLE `ALERT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CHECKING`
--

DROP TABLE IF EXISTS `CHECKING`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CHECKING` (
  `AcctNum` mediumint(9) NOT NULL,
  `CustNum` mediumint(9) NOT NULL,
  `Deposits` decimal(10,2) DEFAULT '0.00',
  `Withdrawls` decimal(10,2) DEFAULT '0.00',
  `CurrentBalance` decimal(10,2) DEFAULT '0.00',
  `AvailableBalance` decimal(10,2) DEFAULT '0.00',
  `ItemCount` mediumint(9) DEFAULT '0',
  `CreditCode` smallint(6) DEFAULT NULL,
  `CreditLimit` decimal(10,2) DEFAULT '0.00',
  `AcctType` varchar(2) NOT NULL,
  PRIMARY KEY (`AcctNum`,`CustNum`),
  KEY `U_Name_CHKG_CUST` (`CustNum`),
  KEY `idx_credit_code` (`CreditCode`),
  KEY `fk_valid_acctTypeCK_idx` (`AcctType`),
  CONSTRAINT `fk_CHECKING_CUSTOMER1` FOREIGN KEY (`CustNum`) REFERENCES `CUSTOMER` (`CustNum`) ON DELETE CASCADE,
  CONSTRAINT `fk_valid_credit` FOREIGN KEY (`CreditCode`) REFERENCES `valid_credit` (`creditCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CHECKING`
--

LOCK TABLES `CHECKING` WRITE;
/*!40000 ALTER TABLE `CHECKING` DISABLE KEYS */;
INSERT INTO `CHECKING` VALUES (1,1,0.00,0.00,0.00,0.00,0,1,1000.00,'C'),(2,2,0.00,0.00,0.00,0.00,0,1,0.00,'C');
/*!40000 ALTER TABLE `CHECKING` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CHECKINGTRANS`
--

DROP TABLE IF EXISTS `CHECKING_TRANS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CHECKING_TRANS` (
  `TransId` mediumint(9) NOT NULL AUTO_INCREMENT,
  `AcctNum` mediumint(9) NOT NULL,
  `CustNum` mediumint(9) NOT NULL,
  `TransDate` datetime DEFAULT NULL,
  `DepositAmt` decimal(10,2) DEFAULT '0.00',
  `WithdrawlAmt` decimal(10,2) DEFAULT '0.00',
  `Total` decimal(10,2) DEFAULT '0.00',
  `ChkNo` varchar(9) DEFAULT NULL,
  `ImageURL` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`TransId`),
  KEY `U_Name_CHKG_CUST` (`AcctNum`,`CustNum`),
  CONSTRAINT `fk_CHECKING_TRANS_CHECKING1` FOREIGN KEY (`AcctNum`, `CustNum`) REFERENCES `CHECKING` (`AcctNum`, `CustNum`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CHECKINGTRANS`
--

LOCK TABLES `CHECKING_TRANS` WRITE;
/*!40000 ALTER TABLE `CHECKING_TRANS` DISABLE KEYS */;
INSERT INTO `CHECKING_TRANS` VALUES (100,2,2,'2020-10-01 00:00:00',1000.00,0.00,1000.00,NULL,NULL);
/*!40000 ALTER TABLE `CHECKING_TRANS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CUSTOMER`
--

DROP TABLE IF EXISTS `CUSTOMER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CUSTOMER` (
  `CustNum` mediumint(9) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `CheckingAcctBal` decimal(10,2) DEFAULT '0.00',
  `SavingsAcctBal` decimal(10,2) DEFAULT '0.00',
  `TotalBalance` decimal(10,2) DEFAULT '0.00',
  `Street` varchar(32) DEFAULT NULL,
  `City` varchar(24) DEFAULT 'ORLANDO',
  `State` varchar(2) DEFAULT 'FL',
  `ZIP` int(11) DEFAULT '32751',
  `Phone` varchar(45) DEFAULT NULL,
  `emailAddress` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`CustNum`),
  UNIQUE KEY `U_Name_CUSTOMERS` (`Name`),
  KEY `idx_state` (`State`),
  CONSTRAINT `fk_valid_state` FOREIGN KEY (`State`) REFERENCES `valid_state` (`stateCode`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CUSTOMER`
--

LOCK TABLES `CUSTOMER` WRITE;
/*!40000 ALTER TABLE `CUSTOMER` DISABLE KEYS */;
INSERT INTO `CUSTOMER` VALUES (1,'Tyler Band',0.00,0.00,0.00,'1521 N BEACH ST','ORMOND BEACH','FL',32174,'4076078094','tyler.band@broadcom.com'),(2,'Tyler',0.00,0.00,0.00,'123 main','Ormond','FL',32751,NULL,NULL);
/*!40000 ALTER TABLE `CUSTOMER` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LINE_OF_CREDIT`
--

DROP TABLE IF EXISTS `LINE_OF_CREDIT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LINE_OF_CREDIT` (
  `CustNum` mediumint(9) NOT NULL,
  `AcctNum` mediumint(9) DEFAULT NULL,
  `OverdaftFeeAmt` decimal(10,2) DEFAULT NULL,
  `LineOfCreditAmt` decimal(10,2) DEFAULT NULL,
  `TotalCharges` decimal(10,2) DEFAULT NULL,
  `TotalPayments` decimal(10,2) DEFAULT NULL,
  `AvailableBalance` decimal(10,2) DEFAULT NULL,
  `Id` mediumint(9) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`),
  KEY `fk_LOC_CUSTOMER1_idx` (`CustNum`),
  KEY `idx_loc_custAcct` (`CustNum`,`AcctNum`),
  CONSTRAINT `fk_LINE_OF_CREDIT_CUSTOMER1` FOREIGN KEY (`CustNum`) REFERENCES `CUSTOMER` (`CustNum`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LINE_OF_CREDIT`
--

LOCK TABLES `LINE_OF_CREDIT` WRITE;
/*!40000 ALTER TABLE `LINE_OF_CREDIT` DISABLE KEYS */;
INSERT INTO `LINE_OF_CREDIT` VALUES (1,1,35.00,1000.00,0.00,0.00,0.00,1);
/*!40000 ALTER TABLE `LINE_OF_CREDIT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `LOC_TRANSACTIONS`
--

DROP TABLE IF EXISTS `LOC_TRANSACTIONS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LOC_TRANSACTIONS` (
  `TransId` mediumint(9) NOT NULL AUTO_INCREMENT,
  `TransDate` datetime DEFAULT NULL,
  `PaymentAmt` decimal(10,2) DEFAULT NULL,
  `ChargeAmt` decimal(10,2) DEFAULT NULL,
  `ChargeType` varchar(45) DEFAULT NULL COMMENT 'fee, OD, Payment',
  `CustNum` mediumint(9) NOT NULL,
  `AcctNum` mediumint(9) NOT NULL,
  PRIMARY KEY (`TransId`),
  KEY `fk_LOC_TRANSACTIONS_LINE_OF_CREDIT1_idx` (`CustNum`,`AcctNum`),
  CONSTRAINT `fk_LOC_TRANSACTIONS_LINE_OF_CREDIT1` FOREIGN KEY (`CustNum`, `AcctNum`) REFERENCES `LINE_OF_CREDIT` (`CustNum`, `AcctNum`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `LOC_TRANSACTIONS`
--

LOCK TABLES `LOC_TRANSACTIONS` WRITE;
/*!40000 ALTER TABLE `LOC_TRANSACTIONS` DISABLE KEYS */;
/*!40000 ALTER TABLE `LOC_TRANSACTIONS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SAVINGS`
--

DROP TABLE IF EXISTS `SAVINGS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SAVINGS` (
  `AcctNum` mediumint(9) NOT NULL,
  `CustNum` mediumint(9) NOT NULL,
  `Deposits` decimal(10,2) DEFAULT '0.00',
  `Withdrawls` decimal(10,2) DEFAULT '0.00',
  `CurrentBalance` decimal(10,2) DEFAULT '0.00',
  `AvailableBalance` decimal(10,2) DEFAULT '0.00',
  `ItemCount` mediumint(9) NOT NULL DEFAULT '0',
  `AcctType` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`AcctNum`,`CustNum`),
  KEY `U_Name_CHKG_CUST` (`CustNum`),
  KEY `fk_savings_acct_type_idx` (`AcctType`),
  CONSTRAINT `fk_SAVINGS_CUSTOMER1` FOREIGN KEY (`CustNum`) REFERENCES `CUSTOMER` (`CustNum`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SAVINGS`
--

LOCK TABLES `SAVINGS` WRITE;
/*!40000 ALTER TABLE `SAVINGS` DISABLE KEYS */;
INSERT INTO `SAVINGS` VALUES (1,1,0.00,0.00,0.00,0.00,0,'S');
/*!40000 ALTER TABLE `SAVINGS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SAVINGSTRANS`
--

DROP TABLE IF EXISTS `SAVINGS_TRANS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SAVINGS_TRANS` (
  `TransId` mediumint(9) NOT NULL AUTO_INCREMENT,
  `AcctNum` mediumint(9) NOT NULL,
  `CustNum` mediumint(9) NOT NULL,
  `TransDate` datetime DEFAULT NULL,
  `DepositAmt` decimal(10,2) DEFAULT '0.00',
  `WithdrawlAmt` decimal(10,2) DEFAULT '0.00',
  `Total` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`TransId`),
  KEY `U_Name_CHKG_CUST` (`AcctNum`,`CustNum`),
  CONSTRAINT `fk_SAVINGS_TRANS_SAVINGS1` FOREIGN KEY (`AcctNum`, `CustNum`) REFERENCES `SAVINGS` (`AcctNum`, `CustNum`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SAVINGSTRANS`
--

LOCK TABLES `SAVINGS_TRANS` WRITE;
/*!40000 ALTER TABLE `SAVINGS_TRANS` DISABLE KEYS */;
/*!40000 ALTER TABLE `SAVINGS_TRANS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRANSFER_FUNDS`
--

DROP TABLE IF EXISTS `TRANSFER_FUNDS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TRANSFER_FUNDS` (
  `TransId` mediumint(9) NOT NULL AUTO_INCREMENT,
  `FromAcct` mediumint(9) NOT NULL,
  `FromCustNum` mediumint(9) NOT NULL,
  `ToAcct` mediumint(9) NOT NULL,
  `ToCustNum` mediumint(9) NOT NULL,
  `TransferAmt` decimal(10,2) DEFAULT '0.00',
  `TransDate` datetime DEFAULT NULL,
  PRIMARY KEY (`TransId`),
  KEY `fk_TRANSFR_FUNDS_CUSTOMER1_idx` (`FromCustNum`),
  KEY `fk_TRANSFR_FUNDS_CUSTOMER2_idx` (`ToCustNum`),
  CONSTRAINT `fk_TRANSFR_FUNDS_CUSTOMER1` FOREIGN KEY (`FromCustNum`) REFERENCES `CUSTOMER` (`CustNum`),
  CONSTRAINT `fk_TRANSFR_FUNDS_CUSTOMER2` FOREIGN KEY (`ToCustNum`) REFERENCES `CUSTOMER` (`CustNum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRANSFER_FUNDS`
--

LOCK TABLES `TRANSFER_FUNDS` WRITE;
/*!40000 ALTER TABLE `TRANSFER_FUNDS` DISABLE KEYS */;
/*!40000 ALTER TABLE `TRANSFER_FUNDS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Valid_Acct_Type`
--

DROP TABLE IF EXISTS `Valid_Acct_Type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Valid_Acct_Type` (
  `AcctType` varchar(2) NOT NULL,
  `AcctDescription` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`AcctType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Valid_Acct_Type`
--

LOCK TABLES `Valid_Acct_Type` WRITE;
/*!40000 ALTER TABLE `Valid_Acct_Type` DISABLE KEYS */;
/*!40000 ALTER TABLE `Valid_Acct_Type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_permission`
--

DROP TABLE IF EXISTS `ab_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_permission`
--

LOCK TABLES `ab_permission` WRITE;
/*!40000 ALTER TABLE `ab_permission` DISABLE KEYS */;
INSERT INTO `ab_permission` VALUES (8,'can_add'),(15,'can_chart'),(7,'can_delete'),(5,'can_download'),(9,'can_edit'),(16,'can_get'),(6,'can_list'),(4,'can_show'),(1,'can_this_form_get'),(2,'can_this_form_post'),(3,'can_userinfo'),(14,'copyrole'),(13,'menu_access'),(10,'resetmypassword'),(11,'resetpasswords'),(12,'userinfoedit');
/*!40000 ALTER TABLE `ab_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_permission_view`
--

DROP TABLE IF EXISTS `ab_permission_view`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_permission_view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) DEFAULT NULL,
  `view_menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_id` (`permission_id`,`view_menu_id`),
  KEY `view_menu_id` (`view_menu_id`),
  CONSTRAINT `ab_permission_view_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `ab_permission` (`id`),
  CONSTRAINT `ab_permission_view_ibfk_2` FOREIGN KEY (`view_menu_id`) REFERENCES `ab_view_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_permission_view`
--

LOCK TABLES `ab_permission_view` WRITE;
/*!40000 ALTER TABLE `ab_permission_view` DISABLE KEYS */;
INSERT INTO `ab_permission_view` VALUES (1,1,5),(3,1,6),(5,1,7),(2,2,5),(4,2,6),(6,2,7),(7,3,9),(8,4,9),(19,4,12),(37,4,23),(45,4,26),(52,4,28),(59,4,30),(66,4,32),(73,4,34),(80,4,36),(87,4,38),(94,4,40),(101,4,42),(108,4,44),(115,4,46),(9,5,9),(20,5,12),(41,5,23),(49,5,26),(56,5,28),(63,5,30),(70,5,32),(77,5,34),(84,5,36),(91,5,38),(98,5,40),(105,5,42),(112,5,44),(119,5,46),(10,6,9),(21,6,12),(29,6,16),(31,6,18),(33,6,20),(40,6,23),(48,6,26),(55,6,28),(62,6,30),(69,6,32),(76,6,34),(83,6,36),(90,6,38),(97,6,40),(104,6,42),(111,6,44),(118,6,46),(11,7,9),(22,7,12),(38,7,23),(46,7,26),(53,7,28),(60,7,30),(67,7,32),(74,7,34),(81,7,36),(88,7,38),(95,7,40),(102,7,42),(109,7,44),(116,7,46),(12,8,9),(23,8,12),(36,8,23),(44,8,26),(51,8,28),(58,8,30),(65,8,32),(72,8,34),(79,8,36),(86,8,38),(93,8,40),(100,8,42),(107,8,44),(114,8,46),(13,9,9),(24,9,12),(39,9,23),(47,9,26),(54,9,28),(61,9,30),(68,9,32),(75,9,34),(82,9,36),(89,9,38),(96,9,40),(103,9,42),(110,9,44),(117,9,46),(14,10,9),(15,11,9),(16,12,9),(17,13,10),(18,13,11),(26,13,13),(28,13,15),(30,13,17),(32,13,19),(34,13,21),(42,13,24),(43,13,25),(50,13,27),(57,13,29),(64,13,31),(71,13,33),(78,13,35),(85,13,37),(92,13,39),(99,13,41),(106,13,43),(113,13,45),(120,13,47),(25,14,12),(27,15,14),(35,16,22);
/*!40000 ALTER TABLE `ab_permission_view` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_permission_view_role`
--

DROP TABLE IF EXISTS `ab_permission_view_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_permission_view_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_view_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_view_id` (`permission_view_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `ab_permission_view_role_ibfk_1` FOREIGN KEY (`permission_view_id`) REFERENCES `ab_permission_view` (`id`),
  CONSTRAINT `ab_permission_view_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `ab_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_permission_view_role`
--

LOCK TABLES `ab_permission_view_role` WRITE;
/*!40000 ALTER TABLE `ab_permission_view_role` DISABLE KEYS */;
INSERT INTO `ab_permission_view_role` VALUES (1,1,1),(2,2,1),(3,3,1),(4,4,1),(5,5,1),(6,6,1),(7,7,1),(8,8,1),(9,9,1),(10,10,1),(11,11,1),(12,12,1),(13,13,1),(14,14,1),(15,15,1),(16,16,1),(17,17,1),(18,18,1),(19,19,1),(20,20,1),(21,21,1),(22,22,1),(23,23,1),(24,24,1),(25,25,1),(26,26,1),(27,27,1),(28,28,1),(29,29,1),(30,30,1),(31,31,1),(32,32,1),(33,33,1),(34,34,1),(35,35,1),(36,36,1),(37,37,1),(38,38,1),(39,39,1),(40,40,1),(41,41,1),(42,42,1),(43,43,1),(44,44,1),(45,45,1),(46,46,1),(47,47,1),(48,48,1),(49,49,1),(50,50,1),(51,51,1),(52,52,1),(53,53,1),(54,54,1),(55,55,1),(56,56,1),(57,57,1),(58,58,1),(59,59,1),(60,60,1),(61,61,1),(62,62,1),(63,63,1),(64,64,1),(65,65,1),(66,66,1),(67,67,1),(68,68,1),(69,69,1),(70,70,1),(71,71,1),(72,72,1),(73,73,1),(74,74,1),(75,75,1),(76,76,1),(77,77,1),(78,78,1),(79,79,1),(80,80,1),(81,81,1),(82,82,1),(83,83,1),(84,84,1),(85,85,1),(86,86,1),(87,87,1),(88,88,1),(89,89,1),(90,90,1),(91,91,1),(92,92,1),(93,93,1),(94,94,1),(95,95,1),(96,96,1),(97,97,1),(98,98,1),(99,99,1),(100,100,1),(101,101,1),(102,102,1),(103,103,1),(104,104,1),(105,105,1),(106,106,1),(107,107,1),(108,108,1),(109,109,1),(110,110,1),(111,111,1),(112,112,1),(113,113,1),(114,114,1),(115,115,1),(116,116,1),(117,117,1),(118,118,1),(119,119,1),(120,120,1);
/*!40000 ALTER TABLE `ab_permission_view_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_register_user`
--

DROP TABLE IF EXISTS `ab_register_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_register_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `email` varchar(64) NOT NULL,
  `registration_date` datetime DEFAULT NULL,
  `registration_hash` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_register_user`
--

LOCK TABLES `ab_register_user` WRITE;
/*!40000 ALTER TABLE `ab_register_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `ab_register_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_role`
--

DROP TABLE IF EXISTS `ab_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_role`
--

LOCK TABLES `ab_role` WRITE;
/*!40000 ALTER TABLE `ab_role` DISABLE KEYS */;
INSERT INTO `ab_role` VALUES (1,'Admin'),(2,'Public');
/*!40000 ALTER TABLE `ab_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_user`
--

DROP TABLE IF EXISTS `ab_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `email` varchar(64) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `login_count` int(11) DEFAULT NULL,
  `fail_login_count` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `changed_on` datetime DEFAULT NULL,
  `created_by_fk` int(11) DEFAULT NULL,
  `changed_by_fk` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `created_by_fk` (`created_by_fk`),
  KEY `changed_by_fk` (`changed_by_fk`),
  CONSTRAINT `ab_user_ibfk_1` FOREIGN KEY (`created_by_fk`) REFERENCES `ab_user` (`id`),
  CONSTRAINT `ab_user_ibfk_2` FOREIGN KEY (`changed_by_fk`) REFERENCES `ab_user` (`id`),
  CONSTRAINT `ab_user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_user`
--

LOCK TABLES `ab_user` WRITE;
/*!40000 ALTER TABLE `ab_user` DISABLE KEYS */;
INSERT INTO `ab_user` VALUES (1,'admin','user','admin','pbkdf2:sha256:150000$788djhRN$1be17959c96e4d635c34647d38131b9ca27914f786efa4d7fa8d4cc5f24f893a',1,'admin@fab.org','2020-09-26 11:29:14',3,0,'2020-09-24 17:14:31','2020-09-24 17:14:31',NULL,NULL);
/*!40000 ALTER TABLE `ab_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_user_role`
--

DROP TABLE IF EXISTS `ab_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`role_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `ab_user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `ab_user` (`id`),
  CONSTRAINT `ab_user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `ab_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_user_role`
--

LOCK TABLES `ab_user_role` WRITE;
/*!40000 ALTER TABLE `ab_user_role` DISABLE KEYS */;
INSERT INTO `ab_user_role` VALUES (1,1,1);
/*!40000 ALTER TABLE `ab_user_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ab_view_menu`
--

DROP TABLE IF EXISTS `ab_view_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ab_view_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ab_view_menu`
--

LOCK TABLES `ab_view_menu` WRITE;
/*!40000 ALTER TABLE `ab_view_menu` DISABLE KEYS */;
INSERT INTO `ab_view_menu` VALUES (33,'ALERT List'),(32,'ALERTModelView'),(8,'AuthDBView'),(17,'Base Permissions'),(29,'CHECKING List'),(27,'CHECKINGTRANS List'),(26,'CHECKING_TRANSModelView'),(28,'CHECKINGModelView'),(45,'CUSTOMER List'),(44,'CUSTOMERModelView'),(1,'IndexView'),(37,'LINE_OF_CREDIT List'),(36,'LINE_OF_CREDITModelView'),(13,'List Roles'),(10,'List Users'),(35,'LOC_TRANSACTIONS List'),(34,'LOC_TRANSACTIONSModelView'),(3,'LocaleView'),(25,'Menu'),(22,'MenuApi'),(21,'Permission on Views/Menus'),(16,'PermissionModelView'),(20,'PermissionViewModelView'),(6,'ResetMyPasswordView'),(5,'ResetPasswordView'),(12,'RoleModelView'),(41,'SAVINGS List'),(39,'SAVINGSTRANS List'),(38,'SAVINGS_TRANSModelView'),(40,'SAVINGSModelView'),(11,'Security'),(4,'SecurityApi'),(43,'TRANSFER_FUNDS List'),(42,'TRANSFER_FUNDSModelView'),(15,'User\'s Statistics'),(9,'UserDBModelView'),(7,'UserInfoEditView'),(14,'UserStatsChartView'),(2,'UtilView'),(24,'Valid_Acct_Type List'),(23,'Valid_Acct_TypeModelView'),(31,'valid_credit List'),(30,'valid_creditModelView'),(47,'valid_state List'),(46,'valid_stateModelView'),(18,'ViewMenuModelView'),(19,'Views/Menus');
/*!40000 ALTER TABLE `ab_view_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valid_credit`
--

DROP TABLE IF EXISTS `valid_credit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valid_credit` (
  `creditCode` smallint(6) NOT NULL,
  `displayValue` varchar(50) DEFAULT NULL,
  `MaxCreditLimit` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`creditCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valid_credit`
--

LOCK TABLES `valid_credit` WRITE;
/*!40000 ALTER TABLE `valid_credit` DISABLE KEYS */;
INSERT INTO `valid_credit` VALUES (1,'Excellent',5000.00),(2,'Good',1000.00),(3,'Fair',500.00),(4,'Poor',250.00),(5,'No Credit',0.00);
/*!40000 ALTER TABLE `valid_credit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `valid_state`
--

DROP TABLE IF EXISTS `valid_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `valid_state` (
  `stateCode` varchar(2) NOT NULL,
  `stateName` varchar(255) NOT NULL,
  PRIMARY KEY (`stateCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `valid_state`
--

LOCK TABLES `valid_state` WRITE;
/*!40000 ALTER TABLE `valid_state` DISABLE KEYS */;
INSERT INTO `valid_state` VALUES ('AK','Alaska'),('AL','Alabama'),('AR','Arkansas'),('AZ','Arizona'),('CA','California'),('CO','Colorado'),('CT','Connecticut'),('DE','Delaware'),('FL','Florida'),('GA','Georgia'),('HI','Hawaii'),('IA','Iowa'),('ID','Idaho'),('IL','Illinois'),('IN','Indiana'),('KS','Kansas'),('KY','Kentucky'),('LA','Louisiana'),('MA','Massachusetts'),('MD','Maryland'),('ME','Maine'),('MI','Michigan'),('MN','Minnesota'),('MO','Missouri'),('MS','Mississippi'),('MT','Montana'),('NC','North Carolina'),('ND','North Dakota'),('NE','Nebraska'),('NH','New Hampshire'),('NJ','New Jersey'),('NM','New Mexico'),('NV','Nevada'),('NY','NewYork'),('OH','Ohio'),('OK','Oklahoma'),('OR','Oregon'),('PA','Pennsylvania'),('RI','Rhode Island'),('SC','South Carolina'),('SD','South Dakota'),('TN','Tennessee'),('TX','Texas'),('UT','Utah'),('VA','Virginia'),('VT','Vermont'),('WA','Washington'),('WI','Wisconsin'),('WV','West Virginia'),('WY','Wyoming');
/*!40000 ALTER TABLE `valid_state` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-09-27 10:28:09
