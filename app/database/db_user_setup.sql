-- Prepares a MySQL server for the project.
CREATE DATABASE IF NOT EXISTS birrwatch_db;
CREATE USER IF NOT EXISTS 'at_dev_usr'@'localhost' IDENTIFIED BY 'at_dev_pwd';
CREATE USER IF NOT EXISTS 'at_sys_usr'@'localhost' IDENTIFIED BY 'at_sys_pwd';
GRANT ALL PRIVILEGES ON at_dev_db. * TO 'at_dev_usr'@'localhost';
GRANT ALL PRIVILEGES ON at_dev_db. * TO 'at_sys_usr'@'localhost';
GRANT SELECT ON performance_schema. * TO 'at_dev_usr'@'localhost';
GRANT SELECT ON performance_schema. * TO 'at_sys_usr'@'localhost';