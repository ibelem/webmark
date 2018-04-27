-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: localhost    Database: webmark
-- ------------------------------------------------------
-- Server version	5.7.21

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('55f7b537eb76');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8_unicode_ci,
  `body_html` text COLLATE utf8_unicode_ci,
  `timestamp` datetime DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `webmark_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_comments_timestamp` (`timestamp`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `comments_ibfk_3` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
INSERT INTO `comments` VALUES (35,'什么是Generic Sensor API？\r\nGeneric Sensor API提供了一套接口把传感器设备暴露到Web平台。该API由基础Sensor接口和一组构建于上方的具体传感器类组成。拥有基础接口可以简化具体传感器类的实现和规范流程。比如你可以看一下Gyroscope类，它非常的简短！核心功能由基础Sensor接口提供，Gyroscope类仅用了三个代表角速度的属性扩展它。\r\n通常，具体的传感器类代表平台上的实际传感器，例如加速计或陀螺仪。但是，在某些情况下，传感器类的实现会融合来自多个平台传感器的数据，并以便捷的方式向用户展示结果。例如，AbsoluteOrientation传感器基于从加速度计，陀螺仪和磁力计获得的数据提供即用型4x4旋转矩阵。\r\n您可能认为Web平台已经提供了一些传感器数据接口，例如，DeviceMotion和DeviceOrientation事件暴露运动传感器数据，还有一些其他实验性API提供来自环境传感器的数据。那么，为什么我们需要这个新的API呢？','什么是Generic Sensor API？\nGeneric Sensor API提供了一套接口把传感器设备暴露到Web平台。该API由基础Sensor接口和一组构建于上方的具体传感器类组成。拥有基础接口可以简化具体传感器类的实现和规范流程。比如你可以看一下Gyroscope类，它非常的简短！核心功能由基础Sensor接口提供，Gyroscope类仅用了三个代表角速度的属性扩展它。\n通常，具体的传感器类代表平台上的实际传感器，例如加速计或陀螺仪。但是，在某些情况下，传感器类的实现会融合来自多个平台传感器的数据，并以便捷的方式向用户展示结果。例如，AbsoluteOrientation传感器基于从加速度计，陀螺仪和磁力计获得的数据提供即用型4x4旋转矩阵。\n您可能认为Web平台已经提供了一些传感器数据接口，例如，DeviceMotion和DeviceOrientation事件暴露运动传感器数据，还有一些其他实验性API提供来自环境传感器的数据。那么，为什么我们需要这个新的API呢？','2018-03-28 02:50:24',NULL,2,41),(38,'Good','Good','2018-03-28 03:22:26',NULL,1,41),(42,'运动传感器：\r\nAccelerometer（加速度计）\r\nGyroscope（陀螺仪）\r\nLinearAccelerationSensor（线性加速度传感器）\r\nAbsoluteOrientationSensor（绝对方向传感器）\r\nRelativeOrientationSensor（相对方向传感器）\r\n','运动传感器：\nAccelerometer（加速度计）\nGyroscope（陀螺仪）\nLinearAccelerationSensor（线性加速度传感器）\nAbsoluteOrientationSensor（绝对方向传感器）\nRelativeOrientationSensor（相对方向传感器）','2018-03-28 03:33:43',NULL,2,11),(43,'I don\'t think it\'s good','I don\'t think it\'s good','2018-03-28 05:16:56',NULL,1,11),(47,'what;s?','what;s?','2018-03-29 06:19:27',NULL,1,40),(49,'What is this','What is this','2018-03-29 07:46:22',NULL,1,39),(51,'几个评论呢','几个评论呢','2018-03-30 01:04:19',NULL,3,41),(52,'几个评论呢','几个评论呢','2018-03-30 01:04:40',NULL,3,41),(53,'重复提交的 bug 啊','重复提交的 bug 啊','2018-03-30 01:04:55',NULL,3,41),(54,'这边的采用','这边的采用','2018-03-30 01:05:26',NULL,3,41),(65,'Test','Test','2018-04-10 04:37:47',NULL,1,41),(67,'这个　Benchmark 还可以，就是现在不火了。','这个　Benchmark 还可以，就是现在不火了。','2018-04-10 04:44:16',NULL,1,41),(69,'我也不清楚他的意义是什么','我也不清楚他的意义是什么','2018-04-10 04:50:12',NULL,1,41),(70,'这个Benchmark还是很不错的','这个Benchmark还是很不错的','2018-04-10 04:52:28',NULL,2,11),(71,'我挺这个Benchmark!!! ','我挺这个Benchmark!!! ','2018-04-10 07:43:21',NULL,2,39),(72,'Good to know the timezone','Good to know the timezone','2018-04-24 05:26:14',NULL,2,11),(73,'什么啊','什么啊','2018-04-25 08:30:39',NULL,1,41);
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_browser`
--

DROP TABLE IF EXISTS `e_browser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_browser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `major` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `language` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `engine_name` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `channel` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ua` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `engine_version` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `version` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_e_browser_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_browser`
--

LOCK TABLES `e_browser` WRITE;
/*!40000 ALTER TABLE `e_browser` DISABLE KEYS */;
INSERT INTO `e_browser` VALUES (1,'2018-04-11 07:09:52','64','en-US','WebKit','','Chrome','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36','537.36','64.0.3282.140'),(2,'2018-04-12 05:00:29','65','zh-CN','WebKit','','Chrome','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','537.36','65.0.3325.181'),(3,'2018-04-12 05:10:41','1','en-US','WebKit','','Vivaldi','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.189 Safari/537.36 Vivaldi/1.95.1077.60','537.36','1.95.1077.60'),(4,'2018-04-16 05:31:47','68','en-US','WebKit','','Chrome','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3397.0 Safari/537.36','537.36','68.0.3397.0'),(5,'2018-04-16 05:33:39','16','en-US','EdgeHTML','','Edge','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299','16.16299','16.16299'),(6,'2018-04-16 05:35:27','61','en-US','Gecko','','Firefox','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','61.0','61.0'),(7,'2018-04-16 05:40:08','64','en-US','WebKit','','Chromium','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/64.0.3282.167 Chrome/64.0.3282.167 Safari/537.36','537.36','64.0.3282.167');
/*!40000 ALTER TABLE `e_browser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_cpu`
--

DROP TABLE IF EXISTS `e_cpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_cpu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `architecture` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hardware_concurrency` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_e_cpu_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_cpu`
--

LOCK TABLES `e_cpu` WRITE;
/*!40000 ALTER TABLE `e_cpu` DISABLE KEYS */;
INSERT INTO `e_cpu` VALUES (4,'2018-04-11 07:01:46','','amd64','8'),(5,'2018-04-12 05:00:29','','amd64','4'),(6,'2018-04-12 08:52:44','i7-7700K','amd64','8'),(7,'2018-04-16 05:31:46','i7-8700K','amd64','12'),(8,'2018-04-16 05:40:08','i7-7700','amd64','8');
/*!40000 ALTER TABLE `e_cpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_environment`
--

DROP TABLE IF EXISTS `e_environment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_environment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `hardware_id` int(11) DEFAULT NULL,
  `software_id` int(11) DEFAULT NULL,
  `browser_id` int(11) DEFAULT NULL,
  `cpu_id` int(11) DEFAULT NULL,
  `gpu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `browser_id` (`browser_id`),
  KEY `hardware_id` (`hardware_id`),
  KEY `software_id` (`software_id`),
  KEY `ix_e_environment_timestamp` (`timestamp`),
  KEY `cpu_id` (`cpu_id`),
  KEY `gpu_id` (`gpu_id`),
  CONSTRAINT `e_environment_ibfk_1` FOREIGN KEY (`browser_id`) REFERENCES `e_browser` (`id`),
  CONSTRAINT `e_environment_ibfk_2` FOREIGN KEY (`hardware_id`) REFERENCES `e_hardware` (`id`),
  CONSTRAINT `e_environment_ibfk_3` FOREIGN KEY (`software_id`) REFERENCES `e_software` (`id`),
  CONSTRAINT `e_environment_ibfk_4` FOREIGN KEY (`cpu_id`) REFERENCES `e_cpu` (`id`),
  CONSTRAINT `e_environment_ibfk_5` FOREIGN KEY (`gpu_id`) REFERENCES `e_gpu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_environment`
--

LOCK TABLES `e_environment` WRITE;
/*!40000 ALTER TABLE `e_environment` DISABLE KEYS */;
INSERT INTO `e_environment` VALUES (7,'2018-04-12 03:29:06',2,1,1,4,1),(8,'2018-04-12 05:08:41',3,2,2,5,2),(9,'2018-04-12 05:10:41',3,2,3,5,2),(10,'2018-04-12 08:52:45',2,1,1,6,1),(11,'2018-04-16 05:31:47',3,2,4,7,3),(12,'2018-04-16 05:33:39',3,2,5,7,4),(13,'2018-04-16 05:35:28',3,3,6,7,3);
/*!40000 ALTER TABLE `e_environment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_gpu`
--

DROP TABLE IF EXISTS `e_gpu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_gpu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `vender` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_e_gpu_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_gpu`
--

LOCK TABLES `e_gpu` WRITE;
/*!40000 ALTER TABLE `e_gpu` DISABLE KEYS */;
INSERT INTO `e_gpu` VALUES (1,'2018-04-11 07:04:53','Mesa DRI yourmail(R) HD Graphics 530 (Skylake GT2)','yourmail Open Source Technology Center'),(2,'2018-04-12 05:00:29','ANGLE (yourmail(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0)','Google Inc.'),(3,'2018-04-16 05:31:47','ANGLE (yourmail(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)','Google Inc.'),(4,'2018-04-16 05:33:39','yourmail(R) UHD Graphics 630','Microsoft'),(5,'2018-04-16 05:40:08','Mesa DRI yourmail(R) Kabylake GT2','yourmail Open Source Technology Center');
/*!40000 ALTER TABLE `e_gpu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_hardware`
--

DROP TABLE IF EXISTS `e_hardware`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_hardware` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `device_vendor` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_model` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `screen_width` int(11) DEFAULT NULL,
  `screen_height` int(11) DEFAULT NULL,
  `device_memory` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_e_hardware_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_hardware`
--

LOCK TABLES `e_hardware` WRITE;
/*!40000 ALTER TABLE `e_hardware` DISABLE KEYS */;
INSERT INTO `e_hardware` VALUES (2,'2018-04-11 08:08:03','None','None','None',1920,1080,'8'),(3,'2018-04-12 05:08:41','None','None','None',1920,1080,'None');
/*!40000 ALTER TABLE `e_hardware` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_software`
--

DROP TABLE IF EXISTS `e_software`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_software` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `os` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os_version` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `platform` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timezone` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_e_software_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_software`
--

LOCK TABLES `e_software` WRITE;
/*!40000 ALTER TABLE `e_software` DISABLE KEYS */;
INSERT INTO `e_software` VALUES (1,'2018-04-11 07:15:10','Linux','x86_64','Linux x86_64','+8'),(2,'2018-04-12 05:00:29','Windows','10','Win32','+8'),(3,'2018-04-16 05:35:27','Windows','10','Win64','+8');
/*!40000 ALTER TABLE `e_software` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `title` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `details` text COLLATE utf8_unicode_ci,
  `reviewed` tinyint(1) DEFAULT NULL,
  `replied` tinyint(1) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_feedback_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback`
--

LOCK TABLES `feedback` WRITE;
/*!40000 ALTER TABLE `feedback` DISABLE KEYS */;
INSERT INTO `feedback` VALUES (1,'belem.zhang@yourmail.com','什么鬼','好吧　这是什么网站　完全没看懂',1,0,'2018-04-25 06:23:14'),(4,'belem.zhang@yourmail.com','什么贵！','什么贵！什么贵！什么贵！什么贵！什么贵！什么贵！什么贵！',0,0,'2018-04-25 06:30:53'),(7,'sys_otc.cip@yourmail.com','What is this ','i don\'t know',NULL,NULL,'2018-04-25 07:16:30');
/*!40000 ALTER TABLE `feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follows`
--

DROP TABLE IF EXISTS `follows`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `follows` (
  `follower_id` int(11) NOT NULL,
  `followed_id` int(11) NOT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`follower_id`,`followed_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follows_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `users` (`id`),
  CONSTRAINT `follows_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follows`
--

LOCK TABLES `follows` WRITE;
/*!40000 ALTER TABLE `follows` DISABLE KEYS */;
INSERT INTO `follows` VALUES (1,1,'2018-03-22 02:20:56'),(2,2,'2018-03-28 01:42:25'),(3,3,'2018-03-29 08:39:32'),(4,4,'2018-04-10 04:54:07'),(5,5,'2018-04-16 05:29:08'),(6,6,'2018-04-25 07:17:56'),(7,7,'2018-04-25 07:45:15'),(8,8,'2018-04-25 07:53:12'),(9,9,'2018-04-25 08:04:08');
/*!40000 ALTER TABLE `follows` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `news` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `summary` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `details` text COLLATE utf8_unicode_ci,
  `timestamp` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `webmark_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_news_timestamp` (`timestamp`),
  CONSTRAINT `news_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `news_ibfk_2` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news`
--

LOCK TABLES `news` WRITE;
/*!40000 ALTER TABLE `news` DISABLE KEYS */;
INSERT INTO `news` VALUES (2,'Speedometer 2.0:  A Benchmark for Modern Web App Responsiveness','https://webkit.org/blog/8063/speedometer-2-0-a-benchmark-for-modern-web-app-responsiveness/','webkit.org','Apple was pleased to announce the Speedometer 2.0 benchmark. Apple hoped this new version of Speedometer helps browser vendors optimize their browser engines for the modern Web.','2018-04-02 08:18:04',1,38),(5,'yourmail contributes VR mode feature for Aquarium','https://github.com/WebGLSamples/WebGLSamples.github.io/pull/16','yourmail OTC','This PR contains two part:\r\n\r\nI. it rebase aquarium-vr to latest version.\r\nII. Add UI for aquarium vr mode. It has features below :\r\n\r\nShow fps in front of users. User could see current fps in HMD. This feature could be turn off by user in VR menu.\r\nVR Menu. It is a mirror of control panel of aquarium. User could call out menu by pressing any key on keyboard or clicking any button on their VR controller or gamepad. Menu is a mirror of control panel without \"Advanced\" label in aquarium. When menu present, user could control cursor(a point in front of user view) by their head. When a label is selected, it will close to user. User stares at a label for 1.5 seconds means click and corresponding operation will be adopted.\r\nWith the UI part, I think aquarium-vr has most feature of aquarium and it maybe possible to accepted aquarium-vr as vr mode of aquarium and merge two folders into one.','2018-04-02 08:34:05',1,11),(6,'Increase fish number and make its change easier','https://github.com/WebGLSamples/WebGLSamples.github.io/pull/13','yourmail OTC','To cater the powerful desktops, fish number is creased so that FPS won\'t hit the roof 60 and an algorithm is introduced to decide the numbers among small, medium and big fishes. Also to make future change of fish number easier, the relevant logic is moved from html to js.','2018-04-02 08:37:32',1,11),(16,'又有XR模式更新','','','这个很 Cool 吧','2018-04-10 04:58:54',1,11),(17,'Gordon Peak','http://mathieuancelin.github.io/js-repaint-perfs/','yourmail','Gordon Peak is Good','2018-04-10 05:24:13',1,40),(20,'A JavaScript benchmark suite focused on the most advanced web applications.','http://www.browserbench.org/JetStream/','Oversea','A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.','2018-04-10 08:49:08',1,41),(21,'A JavaScript benchmark suite focused on the most advanced web applications.','https://url.com','webkit.org','A JavaScript benchmark suite focused on the most advanced web applications.','2018-04-10 08:53:44',1,41),(22,'WebGL Aquarium is credited as being the first Chrome Experiment.','https://url.com','d','                    {% else %}\r\n                     <div class=\"{{ loop.cycle(\'odd\', \'even\') }} col-md-4\">\r\n                      {% if n.url %}\r\n                        {% if n.source %}\r\n                        <h6 class=\"mt-2 pix13\"><a href=\"{{n.url}}\">{{n.summary}}</a><br> by {{ n.source }}</h6>\r\n                          {{ n.details }}\r\n                        {% else %}\r\n                          <h6 class=\"mt-2 pix13\"><a href=\"{{n.url}}\">{{n.summary}}</a></h6>\r\n                          {{ n.details }}\r\n                        {% endif %}\r\n                      {% else %}\r\n                        {% if n.source %}\r\n                          <h6 class=\"mt-2 pix13\">{{n.summary}} by {{ n.source }}</h6>\r\n                          {{ n.details }}\r\n                        {% else %}\r\n                          <h6 class=\"mt-2 pix13\">{{n.summary}}</h6>\r\n                          {{ n.details }}\r\n                        {% endif %}','2018-04-10 08:54:04',1,41),(23,'Speedometer 2.0:  A Benchmark for Modern Web App Responsiveness','','','A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.A JavaScript benchmark suite focused on the most advanced web applications.','2018-04-10 08:54:22',1,41),(24,'A JavaScript benchmark suite focused on the most advanced web applications.','','','A JavaScript benchmark suite focused on the most advanced web applications.','2018-04-11 00:53:57',1,41),(25,'avatar','','','avatar','2018-04-11 01:30:32',1,11);
/*!40000 ALTER TABLE `news` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `posts`
--

DROP TABLE IF EXISTS `posts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `posts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `body` text COLLATE utf8_unicode_ci,
  `body_html` text COLLATE utf8_unicode_ci,
  `timestamp` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `ix_posts_timestamp` (`timestamp`),
  CONSTRAINT `posts_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posts`
--

LOCK TABLES `posts` WRITE;
/*!40000 ALTER TABLE `posts` DISABLE KEYS */;
/*!40000 ALTER TABLE `posts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `default` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_roles_default` (`default`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'User',1,7),(3,'Administrator',0,31);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `score` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `webmark_id` int(11) DEFAULT NULL,
  `score` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `environment_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_score_timestamp` (`timestamp`),
  KEY `environment_id` (`environment_id`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`),
  CONSTRAINT `score_ibfk_3` FOREIGN KEY (`environment_id`) REFERENCES `e_environment` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (65,11,'17',1,'2018-04-13 06:06:43',7),(67,11,'19',2,'2018-04-13 06:54:41',8),(68,11,'18',2,'2018-04-13 06:55:27',8),(69,41,'18',1,'2018-04-13 06:58:57',7),(70,41,'19',3,'2018-04-13 07:04:00',9),(71,11,'19',2,'2018-04-13 07:05:20',8),(72,41,'22',3,'2018-04-13 08:05:08',9),(73,41,'8',3,'2018-04-16 01:42:22',9),(74,41,'19',3,'2018-04-16 01:43:45',9),(75,41,'18',1,'2018-04-16 01:54:30',7),(76,11,'36',5,'2018-04-16 05:32:04',11),(77,11,'35',5,'2018-04-16 05:33:50',12),(78,11,'22',5,'2018-04-16 05:35:37',13),(79,11,'23',1,'2018-04-18 02:05:25',7);
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scores`
--

DROP TABLE IF EXISTS `scores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `webmark_id` int(11) DEFAULT NULL,
  `score` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_vendor` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_model` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `device_memory` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `screen_width` int(11) DEFAULT NULL,
  `screen_height` int(11) DEFAULT NULL,
  `cpu_name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cpu_architecture` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `cpu_hardware_concurrency` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gpu_name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `gpu_vender` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os_version` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `platform` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `timezone` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_version` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_major` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_language` varchar(8) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_engine_name` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_engine_version` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_ua` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser_channel` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_scores_timestamp` (`timestamp`),
  CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `scores_ibfk_2` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scores`
--

LOCK TABLES `scores` WRITE;
/*!40000 ALTER TABLE `scores` DISABLE KEYS */;
INSERT INTO `scores` VALUES (17,11,'1','None','None','None','None',1600,900,'i5-3320M','amd64','4','Google SwiftShader','Google Inc.','Windows','10','Win32','+8','Chrome','65.0.3325.181','65','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',5,'2018-04-18 07:51:26'),(18,11,'1','None','None','None','None',1600,900,'i5-3320M','amd64',NULL,'Microsoft Basic Render Driver','Microsoft','Windows','10','Win32','+8','Edge','14.14393','14','en-US','EdgeHTML','14.14393','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393','',5,'2018-04-18 07:52:50'),(19,11,'9','None','None','None','None',1920,1080,'i5-5300U','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','65.0.3325.181','65','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',5,'2018-04-18 07:58:20'),(20,11,'6','None','None','None','None',1920,1080,'i5-5300U','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win64','+8','Firefox','59.0','59','en-US','Gecko','59.0','Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0','',5,'2018-04-18 08:03:25'),(21,11,'22','None','None','None','None',1920,1080,'i7-8700K','amd64','12','ANGLE (yourmail(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win64','+8','Firefox','61.0','61','en-US','Gecko','61.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','',5,'2018-04-19 04:31:57'),(23,11,'36','None','None','None','None',1920,1080,'i7-8700K','amd64','12','yourmail(R) UHD Graphics 630','Microsoft','Windows','10','Win32','+8','Edge','16.16299','16','en-US','EdgeHTML','16.16299','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299','',5,'2018-04-15 04:34:14'),(24,11,'22','None','None','None','None',1920,1080,'i7-7700','amd64','8','ANGLE (yourmail(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win64','+8','Firefox','60.0','60','en-US','Gecko','60.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0','',5,'2018-04-19 05:11:27'),(43,41,'558','None','None','None','8',1920,1080,'i7-6700','amd64','8','Mesa DRI yourmail(R) HD Graphics 530 (Skylake GT2)','yourmail Open Source Technology Center','Linux','x86_64','Linux x86_64','+8','Chrome','64.0.3282.140','64','en-US','WebKit','537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36','',1,'2018-04-20 07:09:42'),(45,37,'6','None','None','None','8',1920,1080,'i7-6700','amd64','8','Mesa DRI yourmail(R) HD Graphics 530 (Skylake GT2)','yourmail Open Source Technology Center','Linux','x86_64','Linux x86_64','+8','Chrome','64.0.3282.140','64','en-US','WebKit','537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36','',1,'2018-04-20 07:17:50'),(48,41,'548','None','None','None','None',1920,1080,'i5-6440HQ','amd64','4','ANGLE (yourmail(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','65.0.3325.181','65','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',1,'2018-04-20 07:29:59'),(49,11,'19','None','None','None','None',1920,1080,'i5-6440HQ','amd64','4','ANGLE (yourmail(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','65.0.3325.181','65','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',1,'2018-04-20 07:49:26'),(50,37,'9','None','None','None','None',1920,1080,'i5-6440HQ','amd64','4','ANGLE (yourmail(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','65.0.3325.181','65','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',1,'2018-04-20 07:50:46'),(53,11,'37','None','None','None','None',1920,1080,'i7-8700K','amd64','12','ANGLE (yourmail(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','68.0.3405.0','68','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3405.0 Safari/537.36','',5,'2018-04-25 07:07:05'),(54,11,'38','None','None','None','None',1920,1080,'i7-8700K','amd64','12','NVIDIA GeForce GTX 1080','Microsoft','Windows','10','Win32','+8','Edge','16.16299','16','en-US','EdgeHTML','16.16299','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299','',5,'2018-04-25 07:12:04'),(55,11,'55','None','None','None','None',1920,1080,'i7-8700K','amd64','12','ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','68.0.3405.0','68','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3405.0 Safari/537.36','',5,'2018-04-25 07:13:11'),(56,11,'27','None','None','None','None',1920,1080,'i7-8700K','amd64','12','ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win64','+8','Firefox','61.0','61','en-US','Gecko','61.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','',5,'2018-04-25 07:14:27'),(57,37,'1','None','None','None','None',2880,1620,'i5-5300U','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','67.0.3396.10','67','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.10 Safari/537.36','',6,'2018-04-25 07:22:09'),(58,11,'11','None','None','None','None',2880,1620,'i5-5300U','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','67.0.3396.10','67','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.10 Safari/537.36','',6,'2018-04-25 07:24:20'),(59,41,'533','None','None','None','None',2880,1620,'i5-5300U','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','67.0.3396.10','67','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.10 Safari/537.36','',6,'2018-04-25 07:25:11'),(60,11,'34','None','None','None','None',1920,1080,'Ryzen 7 1800X','amd64','16','ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','68.0.3406.0','68','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3406.0 Safari/537.36','',5,'2018-04-25 07:27:20'),(61,11,'21','None','None','None','None',1920,1080,'Ryzen 7 1800X','amd64','16','ANGLE (NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win64','+8','Firefox','61.0','61','en-US','Gecko','61.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','',5,'2018-04-25 07:28:16'),(62,11,'25','None','None','None','None',1920,1080,'Ryzen 7 1800X','amd64','16','NVIDIA GeForce GTX 1080','Microsoft','Windows','10','Win32','+8','Edge','16.16299','16','en-US','EdgeHTML','16.16299','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299','',5,'2018-04-25 07:31:32'),(64,41,'543','None','None','None','None',1920,1080,'i5-8600K','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','67.0.3396.18','67','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.18 Safari/537.36','',8,'2018-04-25 07:57:02'),(66,37,'4','None','None','None','None',1920,1080,'i5-8600K','amd64','4','ANGLE (yourmail(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','8.1','Win32','+8','Chrome','67.0.3396.18','67','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.18 Safari/537.36','',8,'2018-04-25 08:01:55'),(67,11,'7','None','None','None','None',1366,768,'i5-6200U','amd64','4','ANGLE (yourmail(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','66.0.3359.117','66','zh-CN','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36','',7,'2018-04-25 08:01:58'),(68,11,'9','None','None','None','None',1920,1080,'i5-6300U','amd64','4','ANGLE (yourmail(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)','Google Inc.','Windows','10','Win32','+8','Chrome','65.0.3325.181','65','en-US','WebKit','537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36','',9,'2018-04-25 08:10:58');
/*!40000 ALTER TABLE `scores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `star`
--

DROP TABLE IF EXISTS `star`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `star` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `star` int(11) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `webmark_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `author_id` (`author_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_star_timestamp` (`timestamp`),
  CONSTRAINT `star_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`),
  CONSTRAINT `star_ibfk_2` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `star`
--

LOCK TABLES `star` WRITE;
/*!40000 ALTER TABLE `star` DISABLE KEYS */;
INSERT INTO `star` VALUES (1,5,'2018-03-29 06:11:24',1,41),(2,2,'2018-03-29 06:12:29',1,11),(3,3,'2018-03-29 06:13:37',1,40),(4,3,'2018-03-29 06:18:23',2,41),(5,5,'2018-03-29 07:39:42',2,11),(6,4,'2018-03-29 07:46:37',1,39),(7,5,'2018-03-29 08:40:24',3,41),(8,1,'2018-03-29 08:41:17',3,37),(9,5,'2018-03-29 08:44:31',3,11),(10,4,'2018-03-29 08:44:38',3,40),(11,3,'2018-03-29 08:44:47',3,39),(12,4,'2018-03-29 08:44:57',3,38),(13,3,'2018-03-29 08:45:12',3,36),(14,3,'2018-04-03 01:00:26',1,37),(15,5,'2018-04-10 07:43:28',2,39),(16,1,'2018-04-13 07:22:33',2,40);
/*!40000 ALTER TABLE `star` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscription`
--

DROP TABLE IF EXISTS `subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subscription` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `webmark_id` int(11) DEFAULT NULL,
  `global_subscribe` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `ix_subscription_timestamp` (`timestamp`),
  CONSTRAINT `subscription_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `subscription_ibfk_2` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscription`
--

LOCK TABLES `subscription` WRITE;
/*!40000 ALTER TABLE `subscription` DISABLE KEYS */;
/*!40000 ALTER TABLE `subscription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (20,'WebGL'),(21,'Graphics'),(22,'WebXR'),(23,'JavaScript'),(25,'CPU-Intensive'),(28,'DOM'),(29,'MVC'),(30,'CSS'),(32,'SVG'),(33,'Canvas'),(34,'GPU-Intensive'),(36,'HTML');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_webmark`
--

DROP TABLE IF EXISTS `tag_webmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_webmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `webmark_id` int(11) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `webmark_id` (`webmark_id`),
  KEY `tag_id` (`tag_id`),
  CONSTRAINT `tag_webmark_ibfk_1` FOREIGN KEY (`webmark_id`) REFERENCES `webmark` (`id`),
  CONSTRAINT `tag_webmark_ibfk_2` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=142 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_webmark`
--

LOCK TABLES `tag_webmark` WRITE;
/*!40000 ALTER TABLE `tag_webmark` DISABLE KEYS */;
INSERT INTO `tag_webmark` VALUES (77,38,28),(78,38,29),(109,11,20),(110,11,21),(111,11,22),(112,11,34),(113,11,33),(114,36,23),(115,36,25),(123,39,23),(124,40,30),(125,40,32),(126,40,33),(127,40,21),(141,41,36);
/*!40000 ALTER TABLE `tag_webmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `username` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `password_hash` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `location` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `about_me` text COLLATE utf8_unicode_ci,
  `member_since` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_username` (`username`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'belem.zhang@yourmail.com','belem',3,'pbkdf2:sha256:50000$EMG3o2Ig$b671cb407007c34ec8e2253c6742ce205533777c023bddfc395bba84ba10d98b',1,'张敏','CHINA','LLAPA','2018-03-22 02:20:56','2018-04-25 08:43:19'),(2,'sys_otc.cip@yourmail.com','cip',1,'pbkdf2:sha256:50000$QGzZTDX9$717de82cd93073a385055d1ca0b6004234296e5eed105d0deb8b6c3fc5888209',1,'CIP','CHINA','NNAPI','2018-03-28 01:42:24','2018-04-25 02:36:27'),(3,'webvrqa@yourmail.com','webvrqachinai122',1,'pbkdf2:sha256:50000$WsT5CrVA$e1de2ab7539b66fa3a6656ae8c0c9ca6d333b04739513b1d43a1bb71e3b0236c',1,NULL,NULL,NULL,'2018-03-29 08:39:32','2018-04-02 01:31:54'),(4,'test@yourmail.com','test',1,'pbkdf2:sha256:50000$ZsTwt6UD$439aaf28d7245ea899b2e0db5152db6ec388e6607c7b53ffbb32946ebc20e360',0,NULL,NULL,NULL,'2018-04-10 04:54:07','2018-04-10 04:54:07'),(5,'canx.cao@yourmail.com','cancaox',3,'pbkdf2:sha256:50000$hOAFlffZ$c6a7554352ea1851a06dc247d8f25c62efb51d6ee22d0f56fe3ad828821ca1cf',1,NULL,NULL,NULL,'2018-04-16 05:29:08','2018-04-25 07:28:25'),(6,'yunfei.hao@yourmail.com','yunfei',3,'pbkdf2:sha256:50000$TNoBOaij$f7db1415693f0d68553069c52d534b3e4619c7060b5d337356274bc2c262df36',1,NULL,NULL,NULL,'2018-04-25 07:17:56','2018-04-25 07:20:13'),(7,'leix1.wang@yourmail.com','wangle5x',3,'pbkdf2:sha256:50000$ORC1asOr$f3661d03da22511fbbe336b0aabde4536bc37969b6dee1db524bc55b26d0de6f',1,NULL,NULL,NULL,'2018-04-25 07:45:15','2018-04-25 07:45:49'),(8,'hao.x.li@yourmail.com','haoxli',3,'pbkdf2:sha256:50000$tShFseIv$5f51ab725df433abfd2d857cc65661ffc6353da10f2aaff07ed7acd50a689eb2',1,NULL,NULL,NULL,'2018-04-25 07:53:12','2018-04-25 07:58:30'),(9,'wanming.lin@yourmail.com','wmlin',3,'pbkdf2:sha256:50000$ekHeTJH4$7344bfe38621d1f2b7723a4670d4cfe24d18c2166d603ebb98ec9e1fe6bf25fa',1,NULL,NULL,NULL,'2018-04-25 08:04:08','2018-04-25 08:10:59');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webmark`
--

DROP TABLE IF EXISTS `webmark`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webmark` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `version` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `license` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `developed_by` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `screenshot_path` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `repo_url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `summary` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `details` text COLLATE utf8_unicode_ci,
  `pros` text COLLATE utf8_unicode_ci,
  `cons` text COLLATE utf8_unicode_ci,
  `timestamp` datetime DEFAULT NULL,
  `author_id` int(11) DEFAULT NULL,
  `rating_avg` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `comments_count` int(11) DEFAULT NULL,
  `click_count` int(11) DEFAULT NULL,
  `news_count` int(11) DEFAULT NULL,
  `metrics` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `duration` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ready` tinyint(1) DEFAULT NULL,
  `config` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `test_path` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `score_measurement_unit` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_webmark_name` (`name`),
  KEY `author_id` (`author_id`),
  KEY `ix_webmark_timestamp` (`timestamp`),
  CONSTRAINT `webmark_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webmark`
--

LOCK TABLES `webmark` WRITE;
/*!40000 ALTER TABLE `webmark` DISABLE KEYS */;
INSERT INTO `webmark` VALUES (11,'WebGL Aquarium','','BSD-3-Clause','Google Inc.','WebGL_Aquarium.jpg','https://webglsamples.org/aquarium/aquarium.html','https://github.com/WebGLSamples/WebGLSamples.github.io','The aquarium simulates an underwater environment by using WebGL. ','WebGL Aquarium is credited as being the first Chrome Experiment.','','','2018-03-23 05:07:44',1,'4.0000',4,130,4,'Bigger FPS are better','12',1,'15000 Fishes','/t/aquarium/aquarium.html','FPS'),(36,'JetStream','1.1','BSD-2-Clause','Apple Inc.','JetStream.jpg','http://www.browserbench.org/JetStream/','https://github.com/WebKit/webkit/tree/master/PerformanceTests/JetStream','JavaScript performance on advanced web applications.','A JavaScript benchmark suite focused on the most advanced web applications.\r\n\r\nJetStream combines a variety of JavaScript benchmarks, covering a variety of advanced workloads and programming techniques, and reports a single score that balances them using geometric mean.\r\n\r\nEach benchmark measures a distinct workload, and no single optimization technique is sufficient to speed up all benchmarks. Latency tests measure that a web application can start up quickly, ramp up to peak performance quickly, and run smoothly without interruptions. Throughput tests measure the sustained peak performance of a web application, ignoring ramp-up time and spikes in smoothness. Some benchmarks demonstrate tradeoffs, and aggressive or specialized optimization for one benchmark might make another benchmark slower.\r\n\r\nJetStream includes benchmarks from the SunSpider 1.0.2 and Octane 2 JavaScript benchmark suites. It also includes benchmarks from the LLVM compiler open source project, compiled to JavaScript using Emscripten 1.13. It also includes a benchmark based on the Apache Harmony open source project\'s HashMap and a port of the CDx benchmark, hand-translated to JavaScript.\r\n\r\nThese benchmarks cover both classical performance measurements — like Martin Richards\'s machine and language independent benchmark (richards) and the Dhrystone synthetic computing benchmark (dry.c) — and real-world examples — like the Mozilla open source project\'s PDF renderer (pdfjs), the Box2D JavaScript physics engine (box2d), and the jQuery and Closure JavaScript libraries (code- first-load, code-multi-load).\r\n\r\nNote that scores from JetStream 1.1 are not comparable to scores from other versions of JetStream.','JetStrean wants to minimize the opportunities for system noise to throw off measurements, to represent a high-fidelity approximation of the workloads that WebKit users are likely to care about.\r\n\r\nJetStream combines a variety of JavaScript benchmarks, covering a variety of advanced workloads and programming techniques, and reports a single score that balances them using a geometric mean.  \r\n\r\nJetStream includes benchmarks from the SunSpider 1.0.2 and Octane 2 JavaScript benchmark suites. It also includes benchmarks from the LLVM compiler open source project, compiled to JavaScript using Emscripten 1.13. It also includes a benchmark based on the Apache Harmony open source project’s HashMap, hand-translated to JavaScript.  ','','2018-03-20 08:17:59',1,'3.0000',NULL,14,NULL,'Bigger scores are better','',0,'','',''),(37,'FishIE Tank','','CC BY 2.5','Microsoft Corporation','FishIE_Tank2.jpg','https://testdrive-archive.azurewebsites.net/Performance/FishIETank/','https://github.com/MicrosoftEdge/Demos/tree/master/fishietank','This demo uses the canvas element to draw fish swimming in a fish tank.','Canvas is an important part of HTML5 to test because it creates all the nifty 2D images and shapes that can move across your screen.\r\n\r\nThe FPS count tells you how many frames per second the browser is able to draw. If you add or remove fish, the frames per second will go up or down depending on how much work the browser is able to do each frame.  \r\n\r\nThe UI is primarliy driven through Javascript and Canvas. The purpose of these demos is to convey a concept and not intended to be used as a best practice for web development.','','','2018-03-21 04:51:19',1,'2.0000',1,14,NULL,'Bigger FPS are better','12',1,'9000 Fishes','/t/FishIETank/DefaultMod.html','FPS'),(38,'Speedometer','2.0','LGPL and BSD','Apple Inc.','Speedometer.jpg','http://browserbench.org/Speedometer2.0/','https://github.com/WebKit/webkit/blob/master/PerformanceTests/Speedometer/index.html','A Benchmark for Modern Web App Responsiveness.','This benchmark simulates user actions for adding, completing, and removing to-do items using multiple examples in TodoMVC. Each example in TodoMVC implements the same todo application using DOM APIs in different ways. Some call DOM APIs directly from ECMAScript 5 (ES5), ECMASCript 2015 (ES6), ES6 transpiled to ES5, and Elm transpiled to ES5. Others use one of eleven popular JavaScript frameworks: React, React with Redux, Ember.js, Backbone.js, AngularJS, (new) Angular, Vue.js, jQuery, Preact, Inferno, and Flight.\r\n\r\nMany of these frameworks are used on the most popular websites in the world, such as Facebook and Twitter. The performance of these types of operations depends on the speed of the DOM APIs, the JavaScript engine, CSS style resolution, layout, and other technologies.','Speedometer is not meant to compare the performance of different JavaScript frameworks. The mechanism we use to simulate user actions is different for each framework, and we’re forcing frameworks to do more work synchronously than needed in some cases to ensure run time can be measured.','Speedometer should not be used as a way to compare the performance of different JavaScript frameworks as work load differs greatly in each framework.','2018-03-21 04:59:52',1,'4.0000',1,18,NULL,'Bigger scores are better','',0,'','',''),(39,'ARES-6','1.0.1','LGPL and BSD','Apple Inc.','ARES-6.jpg','http://browserbench.org/ARES-6/','https://github.com/WebKit/webkit/tree/master/PerformanceTests/ARES-6','JavaScript performance using modern ECMAScript 6 syntax.','A benchmark measures the execution time of JavaScript\'s newest features.\r\n\r\nARES-6 measures the execution time of JavaScript’s newest features, including symbols, for-of, arrow functions, Map/Set/WeakMap, let/const, classes, proxies, string interpolation, destructuring, default arguments, spread, tail calls, and generators. ARES-6 is comprised of four sub-tests: Air, Basic, Babylon, and ML.','','','2018-03-21 05:14:05',1,'4.0000',2,11,1,'Bigger scores are better','',0,'','',''),(40,'MotionMark','','BSD-2-Clause','Apple Inc.','MotionMark.jpg','http://browserbench.org/MotionMark/','https://github.com/WebKit/webkit/tree/master/PerformanceTests/MotionMark','Rendering performance of animated content.','A graphics benchmark measures a browser’s capability to animate complex scenes.\r\n\r\nMotionMark is a graphics benchmark that measures a browser’s capability to animate complex scenes at a target frame rate.\r\n\r\nMotionMark’s test suite covers a wide wariety of graphics techniques available to web authors:\r\n\r\nMultiply: CSS border radius, transforms, opacity\r\nArcs and Fills: Canvas path fills and arcs\r\nLeaves: CSS-transformed <img> elements\r\nPaths: Canvas line, quadratic, and Bezier paths\r\nLines: Canvas line segments\r\nFocus: CSS blur filter, opacity\r\nImages: Canvas getImageData() and putImageData()\r\nDesign: HTML text rendering\r\nSuits: SVG clip paths, gradients and transforms\r\nWe hope to expand and update this suite with more tests as the benchmark matures and graphics performance improves.','','','2018-03-21 05:26:21',1,'2.6667',NULL,7,1,'Bigger scores are better','',0,'','',''),(41,'HTML5test','9.0','MIT','Niels Leenheer','HTML5test.jpg','http://html5test.com/','https://github.com/WebPlatformTest/HTML5test','How well does your browser support HTML5?','This is a website for testing web standards in the browser. The HTML5 test score is an indication of how well your browser supports the HTML5 standard and related specifications. Find out which parts of HTML5 are supported by your browser today and compare the results with other browsers.','','The HTML5 test does not try to test all of the new features offered by HTML5, nor does it try to test the functionality of each feature it does detect. Despite these shortcomings we hope that by quantifying the level of support users and web developers will get an idea of how hard the browser manufacturers work on improving their browsers and the web as a development platform. The score is calculated by testing for the many new features of HTML5. Each feature is worth one or more points. Apart from the main HTML5 specification and other specifications created the W3C HTML Working Group or WHATWG, this test also awards points for supporting related drafts and specifications. Please be aware that although the HTML5 specification is now an official recommendation, other specifications that are being tested are still in development and could change before receiving an official status. In the future new tests will be added for new specifications and existing tests will be updated when the specifications change.','2018-03-23 06:16:08',1,'4.3333',10,101,5,'Bigger scores are better','10',1,'Version 9.0','/t/HTML5test-version-9.0/index.html','Points');
/*!40000 ALTER TABLE `webmark` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webmarkproposal`
--

DROP TABLE IF EXISTS `webmarkproposal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webmarkproposal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `details` text COLLATE utf8_unicode_ci,
  `timestamp` datetime DEFAULT NULL,
  `email` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `name` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `added` tinyint(1) DEFAULT NULL,
  `reviewed` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_webmarkproposal_name` (`name`),
  KEY `ix_webmarkproposal_timestamp` (`timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webmarkproposal`
--

LOCK TABLES `webmarkproposal` WRITE;
/*!40000 ALTER TABLE `webmarkproposal` DISABLE KEYS */;
INSERT INTO `webmarkproposal` VALUES (9,'https://localvoid.github.io/uibench/','Github: https://github.com/localvoid/uibench \r\n\r\nBenchmark is implemented as close as possible to React/Preact etc., implementation','2018-03-27 06:11:59','belem@163.com','UI Benchmark',0,0),(10,'https://github.com/krausest/js-framework-benchmark','A comparison of the perfomance of a few popular javascript frameworks. The benchmarks creates a large table with randomized entries and measures the time for various operations including rendering duration.','2018-03-27 06:13:07','belem@163.com','JS Framework Benchmark',0,0),(11,'http://mathieuancelin.github.io/js-repaint-perfs/','Playground to test repaint rates of JS libs.','2018-03-27 06:14:16','belem@163.com','JS Repaint Perfs',0,0);
/*!40000 ALTER TABLE `webmarkproposal` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-26 12:58:18
