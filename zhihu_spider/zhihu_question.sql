/*
 Navicat Premium Data Transfer

 Source Server         : mysql-database
 Source Server Type    : MySQL
 Source Server Version : 80024
 Source Host           : localhost:3306
 Source Schema         : zhihu_spider_db

 Target Server Type    : MySQL
 Target Server Version : 80024
 File Encoding         : 65001

 Date: 15/06/2021 16:12:04
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zhihu_question
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_question`;
CREATE TABLE `zhihu_question`  (
  `question_id` bigint NOT NULL DEFAULT 0,
  `topics` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `url` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '',
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `create_time` datetime NULL DEFAULT NULL,
  `update_time` datetime NULL DEFAULT NULL,
  `answer_num` int NOT NULL DEFAULT 0,
  `comments_num` int NOT NULL DEFAULT 0,
  `watch_user_num` int NOT NULL DEFAULT 0,
  `click_num` int NOT NULL DEFAULT 0,
  `crawl_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `crawl_update_time` datetime NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`question_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
