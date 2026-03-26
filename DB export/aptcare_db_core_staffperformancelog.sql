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
-- Table structure for table `core_staffperformancelog`
--

DROP TABLE IF EXISTS `core_staffperformancelog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_staffperformancelog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `complaints_resolved` int NOT NULL,
  `avg_resolution_time` double NOT NULL,
  `date` date NOT NULL,
  `staff_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `core_staffperformancelog_staff_id_0e4d2a32_fk_core_staff_id` (`staff_id`),
  CONSTRAINT `core_staffperformancelog_staff_id_0e4d2a32_fk_core_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `core_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_staffperformancelog`
--

LOCK TABLES `core_staffperformancelog` WRITE;
/*!40000 ALTER TABLE `core_staffperformancelog` DISABLE KEYS */;
INSERT INTO `core_staffperformancelog` VALUES (61,33,4.3,'2026-03-26',49),(62,42,3.2,'2026-03-26',49),(63,53,4.2,'2026-03-26',49),(64,27,5.2,'2026-03-26',50),(65,51,4.6,'2026-03-26',50),(66,43,4.5,'2026-03-26',50),(67,35,2.8,'2026-03-26',51),(68,39,3.1,'2026-03-26',51),(69,28,1.9,'2026-03-26',51),(70,55,4.7,'2026-03-26',52),(71,39,3.7,'2026-03-26',52),(72,26,1.9,'2026-03-26',52),(73,29,5.7,'2026-03-26',53),(74,45,2.6,'2026-03-26',53),(75,55,4.3,'2026-03-26',53),(76,52,2.8,'2026-03-26',54),(77,43,5.7,'2026-03-26',54),(78,36,4,'2026-03-26',54),(79,41,2.9,'2026-03-26',55),(80,26,5.3,'2026-03-26',55),(81,16,2.9,'2026-03-26',55),(82,40,2,'2026-03-26',56),(83,35,2.5,'2026-03-26',56),(84,46,5.6,'2026-03-26',56),(85,25,1.9,'2026-03-26',57),(86,33,3.7,'2026-03-26',57),(87,43,5.1,'2026-03-26',57),(88,35,1.9,'2026-03-26',58),(89,19,4.7,'2026-03-26',58),(90,47,5.5,'2026-03-26',58),(91,20,1.6,'2026-03-26',59),(92,54,5.5,'2026-03-26',59),(93,20,4.2,'2026-03-26',59),(94,37,2.1,'2026-03-26',60),(95,45,4,'2026-03-26',60),(96,34,2.7,'2026-03-26',60);
/*!40000 ALTER TABLE `core_staffperformancelog` ENABLE KEYS */;
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
