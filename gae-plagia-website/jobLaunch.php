<?php
include ('dbConnection.php');

if (isset( $_SERVER['HTTP_X_REQUESTED_WITH'])) {
	if (isset($_POST['inputDocument']) AND isset($_POST['inputSetup']) AND isset($_POST['inputWindow']) AND isset($_POST['inputOverlap']) AND isset($_POST['inputPattern'])) {
		
		$jPath      =  'pan-plagiarism-corpus-2011/external-detection-corpus/suspicious-document/part1/';
		$jDocument  =  filter_var($_POST['inputDocument'], FILTER_SANITIZE_STRING);
		$jSetup     =  filter_var($_POST['inputSetup'], FILTER_SANITIZE_STRING);
		$jWindow    =  filter_var($_POST['inputWindow'], FILTER_SANITIZE_STRING);
		$jOverlap   =  filter_var($_POST['inputOverlap'], FILTER_SANITIZE_STRING);
		$jPattern   =  filter_var($_POST['inputPattern'], FILTER_SANITIZE_STRING);
		$jStatus    =  'Starting';
		$jIdentifier  =  $jDocument . '_' . uniqid();
		
		$sql = 'INSERT INTO jobs(jIdentifier, jDocumentPath, jDocument, jSetup, jWindow, jOverlap, jPattern, jStatus) VALUES("'.$jIdentifier.'", "'.$jPath.'", "'.$jDocument.'", "'.$jSetup.'", "'.$jWindow.'", "'.$jOverlap.'", "'.$jPattern.'", "'.$jStatus.'")';
		mysql_query($sql) or die(mysql_error());
	}
	return;
}
?>
