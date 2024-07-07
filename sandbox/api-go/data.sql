-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: kegwatch
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bac_log`
--

DROP TABLE IF EXISTS `bac_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bac_log` (
  `game` varchar(255) NOT NULL,
  `time` datetime NOT NULL,
  `consumer` varchar(255) NOT NULL,
  `bac` float DEFAULT '0',
  `team` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bac_log`
--

LOCK TABLES `bac_log` WRITE;
/*!40000 ALTER TABLE `bac_log` DISABLE KEYS */;
INSERT INTO `bac_log` VALUES ('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:26:46','Eli Harper',0.014,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:28:46','Eli Harper',0.011,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:30:46','Eli Harper',0.009,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:32:46','Eli Harper',0.006,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:34:46','Eli Harper',0.004,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:36:46','Eli Harper',0.003,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:38:46','Eli Harper',0.002,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:40:47','Eli Harper',0.001,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 15:42:47','Eli Harper',0,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:14:30','Eli Harper',0.019,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:16:30','Eli Harper',0.016,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:18:30','Eli Harper',0.017,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:20:31','Eli Harper',0.013,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:22:31','Eli Harper',0.009,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:24:31','Eli Harper',0.007,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:26:31','Eli Harper',0.005,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:28:31','Eli Harper',0.003,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:30:31','Eli Harper',0.002,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:32:31','Eli Harper',0.002,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:34:31','Eli Harper',0.001,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:36:31','Eli Harper',0.001,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 16:38:32','Eli Harper',0,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 20:52:59','Eli Harper',0.033,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 20:57:59','Eli Harper',0.021,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 21:02:59','Eli Harper',0.012,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 21:08:00','Eli Harper',0.005,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 21:13:00','Eli Harper',0.001,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:01:41','Eli Harper',0.018,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:06:42','Eli Harper',0.012,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:11:44','Eli Harper',0.007,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:15:16','Eli Harper',0.004,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:15:57','Eli Harper',0.004,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:17:13','Eli Harper',0.003,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:17:59','Eli Harper',0.003,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 20:22:59','Eli Harper',0,'Team 1');
/*!40000 ALTER TABLE `bac_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beer_log`
--

DROP TABLE IF EXISTS `beer_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beer_log` (
  `time` datetime NOT NULL,
  `tap_id` int DEFAULT NULL,
  `beer_id` varchar(100) DEFAULT NULL,
  `beer_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `consumer` varchar(255) DEFAULT NULL,
  `oz_poured` float DEFAULT NULL,
  PRIMARY KEY (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beer_log`
--

LOCK TABLES `beer_log` WRITE;
/*!40000 ALTER TABLE `beer_log` DISABLE KEYS */;
INSERT INTO `beer_log` VALUES ('2022-10-14 10:35:23',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Calibration',12),('2022-10-14 10:37:12',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Calibration',12),('2022-10-14 10:38:22',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Calibration',16),('2022-10-14 10:40:15',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Calibration',16),('2022-10-14 10:45:35',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Calibration',12),('2022-10-14 10:46:47',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Calibration',12),('2022-10-14 10:47:34',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Calibration',16),('2022-10-14 10:48:38',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Calibration',16),('2022-10-14 15:31:42',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',12.3294),('2022-10-14 16:36:29',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Joe Pecsi',12.2978),('2022-10-14 17:21:29',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Joe Pecsi',4.89499),('2022-10-14 19:13:10',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Nick Cotten',10.5977),('2022-10-14 19:21:09',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',12.6532),('2022-10-14 19:39:01',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',13.227),('2022-10-14 19:43:33',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kathryn Pecsi',12.622),('2022-10-14 19:50:27',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Anonymous',8.49948),('2022-10-14 19:51:57',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Rob Chiarelli',13.2454),('2022-10-14 20:31:41',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Andrew Mendez',11.6007),('2022-10-14 20:32:13',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kyra Mendez',13.0553),('2022-10-14 20:33:32',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',11.7008),('2022-10-14 20:58:24',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Rob Chiarelli',13.011),('2022-10-14 20:58:52',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',9.69937),('2022-10-14 21:00:17',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',11.34),('2022-10-14 21:10:14',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',14.2268),('2022-10-14 21:10:53',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Nick Cotten',12.2358),('2022-10-14 21:40:25',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',5.68389),('2022-10-14 21:40:39',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',5.54246),('2022-10-14 21:40:47',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',3.13855),('2022-10-14 21:41:00',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',2.71774),('2022-10-14 21:41:21',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',2.94225),('2022-10-14 21:44:56',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Andrew Mendez',6.34607),('2022-10-14 21:55:00',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kyra Mendez',7.33138),('2022-10-14 21:56:40',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Rob Chiarelli',15.6041),('2022-10-14 21:56:58',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Anonymous',0.589674),('2022-10-14 21:56:59',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Anonymous',1.68221),('2022-10-14 22:35:09',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Nick Cotten',9.46722),('2022-10-14 22:35:38',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Joe Pecsi',15.8247),('2022-10-14 22:37:06',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kathryn Pecsi',12.5176),('2022-10-14 22:37:41',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',14.7857),('2022-10-14 22:39:28',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Joe Pecsi',8.63792),('2022-10-14 22:41:36',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Rob Chiarelli',11.6964),('2022-10-14 22:42:48',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kyra Mendez',3.00359),('2022-10-14 22:43:15',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kyra Mendez',4.50469),('2022-10-14 22:43:57',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Kyra Mendez',6.20617),('2022-10-14 22:45:00',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Andrew Mendez',14.6237),('2022-10-14 22:54:26',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Jacquelyn Bell',4.86905),('2022-10-15 17:46:00',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',12),('2022-10-16 20:07:08',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',10.1571),('2022-10-16 21:00:48',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Joe Pecsi',11.8477),('2022-10-25 15:10:22',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',2.00091),('2022-10-25 15:10:35',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00305),('2022-10-25 15:12:05',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00097),('2022-10-25 15:12:09',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00002),('2022-11-07 08:55:57',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00318),('2022-11-07 08:56:01',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.99987),('2022-11-07 08:56:04',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00236),('2022-11-07 08:56:09',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00294),('2022-11-07 08:56:12',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00064),('2022-11-07 08:56:17',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',3.0029),('2022-11-07 10:18:57',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',2.00125),('2022-11-07 10:18:59',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00002),('2022-11-07 10:19:02',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',2.00157),('2022-11-07 10:19:06',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',3.00267),('2022-11-07 10:19:09',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00104),('2022-11-07 10:19:13',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00219),('2022-11-07 11:14:03',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.002),('2022-11-07 11:14:08',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3),('2022-11-07 11:14:10',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00181),('2022-11-07 11:14:13',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',2.00126),('2022-11-07 11:14:16',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00063),('2022-11-07 11:14:18',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00082),('2022-11-07 11:17:37',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00045),('2022-11-07 11:17:44',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00139),('2022-11-08 15:48:36',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00068),('2022-11-08 15:48:40',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00225),('2022-11-08 15:48:42',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00156),('2022-11-08 15:48:46',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',3.00186),('2022-11-08 15:48:50',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',2.00205),('2022-11-08 15:48:52',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00157),('2022-11-08 15:48:56',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00186),('2022-11-08 15:49:01',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00312),('2022-11-08 15:51:24',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',1.00021),('2022-11-08 15:51:27',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00145),('2022-11-08 15:51:30',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00185),('2022-11-09 14:58:44',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00064),('2022-11-09 14:58:47',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',1.00017),('2022-11-09 14:58:52',1,'125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit','Eli Harper',3.00281),('2022-11-09 14:58:57',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00232),('2022-11-09 14:59:01',2,'7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite','Eli Harper',2.00095);
/*!40000 ALTER TABLE `beer_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consumers`
--

DROP TABLE IF EXISTS `consumers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consumers` (
  `id` varchar(255) NOT NULL,
  `body_cat` int DEFAULT NULL,
  `grams` int DEFAULT '0',
  `is_female` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consumers`
--

LOCK TABLES `consumers` WRITE;
/*!40000 ALTER TABLE `consumers` DISABLE KEYS */;
INSERT INTO `consumers` VALUES ('Andrew Mendez',1,0,0),('Eli Harper',1,81647,0),('Jacquelyn Bell',0,0,1),('Joe Pecsi',1,0,0),('John Doe',2,0,0),('Kathryn Pecsi',0,0,1),('Kyra Mendez',1,0,1),('Lida Weinstock',1,0,1),('NEW USER',0,0,1),('Noob McBoob',0,0,1),('Rob Chiarelli',1,0,0);
/*!40000 ALTER TABLE `consumers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_log`
--

DROP TABLE IF EXISTS `game_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_log` (
  `game` varchar(255) NOT NULL,
  `time` datetime NOT NULL,
  `consumer` varchar(255) NOT NULL,
  `type_consumed` varchar(255) NOT NULL,
  `amount_consumed` float NOT NULL,
  `bev_abv` float DEFAULT NULL,
  `team` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_log`
--

LOCK TABLES `game_log` WRITE;
/*!40000 ALTER TABLE `game_log` DISABLE KEYS */;
INSERT INTO `game_log` VALUES ('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-10-25 15:10:22','Eli Harper','(Beer) Optimal Wit',2.00091,4.9,'None'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-10-25 15:10:35','Eli Harper','(Beer) Optimal Wit',3.00305,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-10-25 15:12:05','Eli Harper','(Beer) Miller Lite',1.00097,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-10-25 15:12:09','Eli Harper','(Beer) Miller Lite',2.00002,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:55:57','Eli Harper','(Beer) Optimal Wit',3.00318,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:56:01','Eli Harper','(Beer) Miller Lite',1.99987,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:56:04','Eli Harper','(Beer) Optimal Wit',1.00236,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:56:09','Eli Harper','(Beer) Optimal Wit',3.00294,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:56:12','Eli Harper','(Beer) Optimal Wit',1.00064,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 08:56:17','Eli Harper','(Beer) Miller Lite',3.0029,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:18:57','Eli Harper','(Beer) Optimal Wit',2.00125,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:18:59','Eli Harper','(Beer) Miller Lite',1.00002,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:19:02','Eli Harper','(Beer) Optimal Wit',2.00157,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:19:06','Eli Harper','(Beer) Miller Lite',3.00267,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:19:09','Eli Harper','(Beer) Miller Lite',2.00104,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 10:19:13','Eli Harper','(Beer) Optimal Wit',3.00219,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:03','Eli Harper','(Beer) Miller Lite',2.002,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:08','Eli Harper','(Beer) Optimal Wit',3,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:10','Eli Harper','(Beer) Optimal Wit',1.00181,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:13','Eli Harper','(Beer) Optimal Wit',2.00126,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:16','Eli Harper','(Beer) Miller Lite',1.00063,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:14:18','Eli Harper','(Beer) Optimal Wit',1.00082,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:17:37','Eli Harper','(Beer) Optimal Wit',1.00045,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-07 11:17:45','Eli Harper','(Beer) Optimal Wit',1.00139,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:36','Eli Harper','(Beer) Miller Lite',1.00068,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:40','Eli Harper','(Beer) Miller Lite',2.00225,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:42','Eli Harper','(Beer) Miller Lite',1.00156,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:46','Eli Harper','(Beer) Miller Lite',3.00186,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:50','Eli Harper','(Beer) Optimal Wit',2.00205,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:52','Eli Harper','(Beer) Optimal Wit',1.00157,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:48:57','Eli Harper','(Beer) Optimal Wit',3.00186,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:49:01','Eli Harper','(Beer) Optimal Wit',3.00312,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:51:24','Eli Harper','(Beer) Optimal Wit',1.00021,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:51:27','Eli Harper','(Beer) Miller Lite',2.00145,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-08 15:51:30','Eli Harper','(Beer) Optimal Wit',3.00185,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 14:58:44','Eli Harper','(Beer) Optimal Wit',3.00064,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 14:58:47','Eli Harper','(Beer) Miller Lite',1.00017,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 14:58:52','Eli Harper','(Beer) Optimal Wit',3.00281,4.9,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 14:58:57','Eli Harper','(Beer) Miller Lite',2.00232,4.2,'Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','2022-11-09 14:59:01','Eli Harper','(Beer) Miller Lite',2.00095,4.2,'Team 1');
/*!40000 ALTER TABLE `game_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `games`
--

DROP TABLE IF EXISTS `games`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `games` (
  `id` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `date` varchar(255) DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `games`
--

LOCK TABLES `games` WRITE;
/*!40000 ALTER TABLE `games` DISABLE KEYS */;
INSERT INTO `games` VALUES ('6b9c9724-dd8d-41fa-8611-d0027f84ddab','Test Game','2022-10-25','0');
/*!40000 ALTER TABLE `games` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keg_log`
--

DROP TABLE IF EXISTS `keg_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keg_log` (
  `id` varchar(255) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `tap` int DEFAULT NULL,
  `abv` float DEFAULT NULL,
  `capacity` float DEFAULT NULL,
  `remaining` float DEFAULT NULL,
  `date_tapped` varchar(100) DEFAULT NULL,
  `date_kicked` varchar(100) DEFAULT NULL,
  `days_to_consume` int DEFAULT NULL,
  `status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keg_log`
--

LOCK TABLES `keg_log` WRITE;
/*!40000 ALTER TABLE `keg_log` DISABLE KEYS */;
INSERT INTO `keg_log` VALUES ('125b44ac-5e0c-4be0-96da-01c70edfba71','Optimal Wit',1,4.9,661,353.35,'2022-10-14','',0,'1'),('7eef7d24-88fc-4946-a30d-c929c44ba6a0','Miller Lite',2,4.2,992,715.67,'2022-10-14',NULL,NULL,'1'),('cc823510-573c-4049-832c-f1f6482796ba','Ride the Tide',1,8.5,661,0,'2022-7-26','2022-9-26',62,'0');
/*!40000 ALTER TABLE `keg_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teams`
--

DROP TABLE IF EXISTS `teams`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teams` (
  `game` varchar(255) NOT NULL,
  `consumer` varchar(255) NOT NULL,
  `team` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teams`
--

LOCK TABLES `teams` WRITE;
/*!40000 ALTER TABLE `teams` DISABLE KEYS */;
INSERT INTO `teams` VALUES ('6b9c9724-dd8d-41fa-8611-d0027f84ddab','Eli Harper','Team 1'),('6b9c9724-dd8d-41fa-8611-d0027f84ddab','Joe Pecsi','Team 1');
/*!40000 ALTER TABLE `teams` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-09 20:44:42
