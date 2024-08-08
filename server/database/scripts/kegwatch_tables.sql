CREATE DATABASE IF NOT EXISTS `kegwatch` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
GO
USE `kegwatch`;
GO

CREATE TABLE tbl_keg (
    keg_id varchar(255) NOT NULL, 
    keg_name varchar(255) NOT NULL, 
    keg_size decimal(8,4) NOT NULL, 
    keg_abv decimal(3,1) NOT NULL, 
    keg_tap tinyint NOT NULL, 
    keg_start datetime NOT NULL, 
    keg_end datetime, 
    keg_remain decimal(8,4) NOT NULL, 
    keg_status tinyint NOT NULL,
    PRIMARY KEY (keg_id)
);
GO

CREATE TABLE tbl_pour (
    keg_id varchar(255) NOT NULL,
    keg_tap tinyint NOT NULL,
    pour_time datetime NOT NULL,
    pour_size decimal(8,4) NOT NULL,
    pour_user varchar(255) NOT NULL,
    FOREIGN KEY (keg_id) REFERENCES tbl_keg(keg_id)
);
GO