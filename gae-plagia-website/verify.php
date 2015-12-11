<?php
session_start();

$sUsername = 'superman';
$sPassword = 'kryptonite';

if (($_POST["username"] == $sUsername) and ($_POST["password"] == $sPassword)){
	$_SESSION["login"] = "true";
	header("Location:index.php");
} else {
	header("Location:login.php");
}
?>