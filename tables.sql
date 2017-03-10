CREATE DATABASE IF NOT EXISTS `employee`;
USE `employee`;
DROP TABLE IF EXISTS `emp_login_details`;
CREATE TABLE `emp_login_details`( `emp_id` INT(4) NOT NULL AUTO_INCREMENT,
                                  `emp_username` TINYTEXT NOT NULL,
                                  `emp_password` TINYTEXT NOT NULL, 
                                  `admin_perm` TINYINT(1) NOT NULL DEFAULT 0 COMMENT '0 for emp, 1 for admin',
                                  PRIMARY KEY (`emp_id`) ) ENGINE=INNODB CHARSET=utf8 COLLATE=utf8_general_ci;
ALTER TABLE `emp_login_details` AUTO_INCREMENT=1001;
INSERT INTO `emp_login_details` (`emp_username`, `emp_password`, `admin_perm`) VALUES ('tyrion', '12345', '1');
INSERT INTO `emp_login_details` (`emp_username`, `emp_password`) VALUES ('jon snow', '98765');

CREATE TABLE `emp_personal`( `emp_id` INT(4) NOT NULL AUTO_INCREMENT,
							 `emp_name` TINYTEXT NOT NULL,
							 `email` TINYTEXT,
							 `phone` TINYINT(10), 
							 `address` MEDIUMTEXT, 
							 `pin` SMALLINT(6), 
							 `state` TINYTEXT,
							 `country` TINYTEXT, 
							 `dob` DATE, `sex` CHAR,
							 `religion` TINYTEXT, 
							 `linkedin` TINYTEXT,
							  `github` TINYTEXT, 
							  `dp` LONGBLOB, PRIMARY KEY (`emp_id`) ); 

ALTER TABLE `emp_personal` ADD CONSTRAINT `emp_id` FOREIGN KEY (`emp_id`) REFERENCES `employee`.`emp_login_details`(`emp_id`) ON UPDATE CASCADE ON DELETE CASCADE; 
