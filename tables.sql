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
							 `phone` BIGINT(10), 
							 `address` MEDIUMTEXT,
							 `country` TINYTEXT,
							 `state` TINYTEXT,  
							 `pin` bigINT(6),						 
							 `dob` DATE,
							 `gender` TINYTEXT,
							 `linkedin` TINYTEXT,
							 `github` TINYTEXT, 
							  #`dp` LONGBLOB,
							 PRIMARY KEY (`emp_id`) );

ALTER TABLE `emp_personal` ADD CONSTRAINT `emp_id` FOREIGN KEY (`emp_id`) REFERENCES `emp_login_details`(`emp_id`) ON UPDATE CASCADE ON DELETE CASCADE; 
CREATE TABLE `institutes`( `inst_id` INT(4) NOT NULL AUTO_INCREMENT,
						   `inst_name` TEXT(40) NOT NULL,
						    PRIMARY KEY (`inst_id`) ) ENGINE=INNODB CHARSET=utf8;
ALTER TABLE `institutes` AUTO_INCREMENT=1001;
INSERT INTO `institutes` (`inst_name`) VALUES ('St. thomas` college of engineering and technology');

CREATE TABLE `education`( `emp_id` INT(4) NOT NULL, `inst_id` INT(4) NOT NULL,`level` SET('Doctorate/Phd','Master','Bachelor','High-School') NOT NULL,  `year_pass` INT(4) NOT NULL, `marks` FLOAT NOT NULL ) ENGINE=INNODB CHARSET=utf8; 
ALTER TABLE  `education` ADD PRIMARY KEY (`emp_id`, `inst_id`,`level`),
						 ADD CONSTRAINT `emp_id1` FOREIGN KEY (`emp_id`) REFERENCES `emp_login_details`(`emp_id`) ON UPDATE CASCADE ON DELETE CASCADE,
						 ADD CONSTRAINT `inst_id1` FOREIGN KEY (`inst_id`) REFERENCES `institutes`(`inst_id`) ON UPDATE CASCADE ON DELETE CASCADE;
CREATE TABLE `experience`( `emp_id` INT(4) NOT NULL, 
	                       `designation` TEXT, 
	                       `organisation` TEXT, 
	                       `start_date` DATE, 
	                       `end_date` DATE, 
	                       CONSTRAINT `emp_id3` FOREIGN KEY (`emp_id`) REFERENCES `emp_login_details`(`emp_id`) ) ENGINE=INNODB CHARSET=utf8; 
CREATE TABLE `skill`( `emp_id` INT(4) NOT NULL,
					  `skills` TEXT(20) NOT NULL,
					  `level` SET('beginner','intermediate','advanced') NOT NULL, 
					  CONSTRAINT `emp_id2` FOREIGN KEY (`emp_id`) REFERENCES `emp_login_details`(`emp_id`) ON UPDATE CASCADE ON DELETE CASCADE ) ENGINE=INNODB CHARSET=utf8; 						  