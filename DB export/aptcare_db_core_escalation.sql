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
-- Table structure for table `core_escalation`
--

DROP TABLE IF EXISTS `core_escalation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_escalation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sla_deadline` datetime(6) NOT NULL,
  `escalated_at` datetime(6) NOT NULL,
  `reason` longtext NOT NULL,
  `complaint_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `complaint_id` (`complaint_id`),
  CONSTRAINT `core_escalation_complaint_id_59eeef81_fk_core_complaint_id` FOREIGN KEY (`complaint_id`) REFERENCES `core_complaint` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_escalation`
--

LOCK TABLES `core_escalation` WRITE;
/*!40000 ALTER TABLE `core_escalation` DISABLE KEYS */;
INSERT INTO `core_escalation` VALUES (115,'2026-03-26 05:03:36.433926','2026-03-26 06:57:36.433926','SLA breached. Expected resolution within 24 hours.',2486),(116,'2026-03-25 20:03:36.433926','2026-03-25 22:02:36.433926','SLA breached. Expected resolution within 24 hours.',2487),(117,'2026-03-25 21:03:36.433926','2026-03-25 22:03:36.433926','SLA breached. Expected resolution within 24 hours.',2488),(118,'2026-03-25 03:03:36.433926','2026-03-25 04:57:36.433926','SLA breached. Expected resolution within 4 hours.',2489),(119,'2026-03-24 06:03:36.433926','2026-03-24 07:24:36.433926','SLA breached. Expected resolution within 4 hours.',2490),(120,'2026-03-24 04:03:36.433926','2026-03-24 04:27:36.433926','SLA breached. Expected resolution within 4 hours.',2491),(121,'2026-03-24 07:03:36.433926','2026-03-24 07:37:36.433926','SLA breached. Expected resolution within 4 hours.',2492);
/*!40000 ALTER TABLE `core_escalation` ENABLE KEYS */;
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
