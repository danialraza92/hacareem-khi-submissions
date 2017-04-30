DROP TABLE trips;
CREATE TABLE trips (user_id varchar(255), ride_id varchar(255), pick_up_time varchar(255), pick_up varchar(255), pick_up_lat varchar(255), pick_up_lng varchar(255), pick_up_geohash varchar(255), drop_off varchar(255), drop_off_lat varchar(255), drop_off_lng varchar(255), drop_off_geohash varchar(255), readFlag tinyint(1) DEFAULT 0 NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;
DROP PROCEDURE getPredictions;
--/
CREATE DEFINER=`root`@`localhost` PROCEDURE getPredictions()
    READS SQL DATA
BEGIN
  DECLARE v CHAR(10) DEFAULT 'Hello';
  SELECT CONCAT(v, ', ', current_user, '!');
END
/
