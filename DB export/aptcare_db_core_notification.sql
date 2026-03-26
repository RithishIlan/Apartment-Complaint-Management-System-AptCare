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
-- Table structure for table `core_notification`
--

DROP TABLE IF EXISTS `core_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `complaint_id` bigint DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_notification_complaint_id_7d780829_fk_core_complaint_id` (`complaint_id`),
  KEY `core_notification_user_id_6e341aac_fk_core_customuser_id` (`user_id`),
  CONSTRAINT `core_notification_complaint_id_7d780829_fk_core_complaint_id` FOREIGN KEY (`complaint_id`) REFERENCES `core_complaint` (`id`),
  CONSTRAINT `core_notification_user_id_6e341aac_fk_core_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `core_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3247 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_notification`
--

LOCK TABLES `core_notification` WRITE;
/*!40000 ALTER TABLE `core_notification` DISABLE KEYS */;
INSERT INTO `core_notification` VALUES (3240,'Your complaint #2486 has been assigned to Arun Mehta. Status: In Progress.',0,'2026-03-26 07:08:42.878450',2486,1012),(3241,'Your complaint #2454 has been assigned to Dinesh Reddy. Status: In Progress.',0,'2026-03-26 07:18:29.444555',2454,951),(3242,'Your complaint #2454 has been assigned to Dinesh Reddy. Status: In Progress.',0,'2026-03-26 07:19:11.269732',2454,951),(3243,'Your complaint #2455 has been assigned to Vikram Singh. Status: In Progress.',0,'2026-03-26 07:26:59.618013',2455,1003),(3244,'Your complaint #2673 has been filed with HIGH priority.',0,'2026-03-26 14:20:48.240830',2673,866),(3245,'Your complaint #2674 has been filed with HIGH priority.',0,'2026-03-26 14:52:41.452269',2674,866),(3246,'Your complaint #2675 has been filed with HIGH priority.',0,'2026-03-26 14:53:10.129522',2675,866);
/*!40000 ALTER TABLE `core_notification` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 20:48:27
