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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-03-18 16:13:45.864149'),(2,'contenttypes','0002_remove_content_type_name','2026-03-18 16:13:46.051733'),(3,'auth','0001_initial','2026-03-18 16:13:46.571215'),(4,'auth','0002_alter_permission_name_max_length','2026-03-18 16:13:46.696926'),(5,'auth','0003_alter_user_email_max_length','2026-03-18 16:13:46.706399'),(6,'auth','0004_alter_user_username_opts','2026-03-18 16:13:46.721260'),(7,'auth','0005_alter_user_last_login_null','2026-03-18 16:13:46.733302'),(8,'auth','0006_require_contenttypes_0002','2026-03-18 16:13:46.740650'),(9,'auth','0007_alter_validators_add_error_messages','2026-03-18 16:13:46.750514'),(10,'auth','0008_alter_user_username_max_length','2026-03-18 16:13:46.766827'),(11,'auth','0009_alter_user_last_name_max_length','2026-03-18 16:13:46.776676'),(12,'auth','0010_alter_group_name_max_length','2026-03-18 16:13:46.806326'),(13,'auth','0011_update_proxy_permissions','2026-03-18 16:13:46.817296'),(14,'auth','0012_alter_user_first_name_max_length','2026-03-18 16:13:46.826655'),(15,'core','0001_initial','2026-03-18 16:13:49.027865'),(16,'admin','0001_initial','2026-03-18 16:13:49.260472'),(17,'admin','0002_logentry_remove_auto_add','2026-03-18 16:13:49.278804'),(18,'admin','0003_logentry_add_action_flag_choices','2026-03-18 16:13:49.295507'),(19,'sessions','0001_initial','2026-03-18 16:13:49.352106'),(20,'authtoken','0001_initial','2026-03-18 16:17:17.615839'),(21,'authtoken','0002_auto_20160226_1747','2026-03-18 16:17:17.658442'),(22,'authtoken','0003_tokenproxy','2026-03-18 16:17:17.668062'),(23,'authtoken','0004_alter_tokenproxy_options','2026-03-18 16:17:17.679002'),(24,'core','0002_review','2026-03-19 02:15:43.902087'),(25,'core','0003_customuser_must_change_password_otpverification','2026-03-24 02:38:07.897791');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-26 20:48:28
