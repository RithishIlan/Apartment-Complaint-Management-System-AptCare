-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: aptcare_db
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add complaint category',8,'add_complaintcategory'),(22,'Can change complaint category',8,'change_complaintcategory'),(23,'Can delete complaint category',8,'delete_complaintcategory'),(24,'Can view complaint category',8,'view_complaintcategory'),(25,'Can add department',10,'add_department'),(26,'Can change department',10,'change_department'),(27,'Can delete department',10,'delete_department'),(28,'Can view department',10,'view_department'),(29,'Can add user',9,'add_customuser'),(30,'Can change user',9,'change_customuser'),(31,'Can delete user',9,'delete_customuser'),(32,'Can view user',9,'view_customuser'),(33,'Can add complaint',7,'add_complaint'),(34,'Can change complaint',7,'change_complaint'),(35,'Can delete complaint',7,'delete_complaint'),(36,'Can view complaint',7,'view_complaint'),(37,'Can add attachment',6,'add_attachment'),(38,'Can change attachment',6,'change_attachment'),(39,'Can delete attachment',6,'delete_attachment'),(40,'Can view attachment',6,'view_attachment'),(41,'Can add escalation',11,'add_escalation'),(42,'Can change escalation',11,'change_escalation'),(43,'Can delete escalation',11,'delete_escalation'),(44,'Can view escalation',11,'view_escalation'),(45,'Can add notification',12,'add_notification'),(46,'Can change notification',12,'change_notification'),(47,'Can delete notification',12,'delete_notification'),(48,'Can view notification',12,'view_notification'),(49,'Can add staff',13,'add_staff'),(50,'Can change staff',13,'change_staff'),(51,'Can delete staff',13,'delete_staff'),(52,'Can view staff',13,'view_staff'),(53,'Can add staff performance log',14,'add_staffperformancelog'),(54,'Can change staff performance log',14,'change_staffperformancelog'),(55,'Can delete staff performance log',14,'delete_staffperformancelog'),(56,'Can view staff performance log',14,'view_staffperformancelog'),(57,'Can add Token',15,'add_token'),(58,'Can change Token',15,'change_token'),(59,'Can delete Token',15,'delete_token'),(60,'Can view Token',15,'view_token'),(61,'Can add Token',16,'add_tokenproxy'),(62,'Can change Token',16,'change_tokenproxy'),(63,'Can delete Token',16,'delete_tokenproxy'),(64,'Can view Token',16,'view_tokenproxy'),(65,'Can add review',17,'add_review'),(66,'Can change review',17,'change_review'),(67,'Can delete review',17,'delete_review'),(68,'Can view review',17,'view_review'),(69,'Can add otp verification',18,'add_otpverification'),(70,'Can change otp verification',18,'change_otpverification'),(71,'Can delete otp verification',18,'delete_otpverification'),(72,'Can view otp verification',18,'view_otpverification');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 20:48:29
