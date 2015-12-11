<?php
session_start();

if(session_destroy()) {
	$_SESSION["login"] = "false";
	header("Location:login.php");
}
?>