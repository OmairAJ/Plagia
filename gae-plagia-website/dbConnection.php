<?php
$host     =  ':/cloudsql/plagia-2015:plagiadb';
$username =  'root';
$password =  '';
$database =  'plagiaDB';

$connection  =  mysql_connect($host, $username, $password) or die('Unable to establish connection to the database server.');

mysql_select_db($database) or die('No database of such name found.');

$sql    =  '';
$query  =  '';
$row    =  '';
?>