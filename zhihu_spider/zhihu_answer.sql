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

 Date: 15/06/2021 16:10:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for zhihu_answer
-- ----------------------------
DROP TABLE IF EXISTS `zhihu_answer`;
CREATE TABLE `zhihu_answer`  (
  `answer_id` bigint NOT NULL,
  `url` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `question_id` bigint NOT NULL,
  `author_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `praise_num` int NOT NULL,
  `comments_num` int NOT NULL,
  `create_time` date NOT NULL,
  `update_time` date NOT NULL,
  `crawl_time` datetime NOT NULL,
  `crawl_update_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`answer_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
