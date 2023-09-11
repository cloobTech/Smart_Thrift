-- Prepare a MYSQL database for the application

-- Create the database
CREATE DATABASE IF NOT EXISTS `smart_drift_DB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;

-- Create the user
CREATE USER IF NOT EXISTS 'smart_drift_user'@'localhost' IDENTIFIED BY 'smart_drift_pwd';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON `smart_drift_DB`.* TO 'smart_drift_user'@'localhost';

-- Grant SELECT privileges to the user
GRANT SELECT ON `performance_schema`.* TO 'smart_drift_user'@'localhost';

-- Flush privileges
FLUSH PRIVILEGES;