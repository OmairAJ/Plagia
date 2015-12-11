<?php
include ('dbConnection.php');

if (isset( $_SERVER['HTTP_X_REQUESTED_WITH'])) {
	if (isset($_POST['inputSetupSource']) AND isset($_POST['inputWindowSource']) AND isset($_POST['inputOverlapSource']) AND isset($_POST['inputPatternSource'])) {
		
		$jPath    =  'pan-plagiarism-corpus-2011/external-detection-corpus/source-document/part3/';
		$jSetup   =  filter_var($_POST['inputSetupSource'], FILTER_SANITIZE_STRING);
		$jWindow  =  filter_var($_POST['inputWindowSource'], FILTER_SANITIZE_STRING);
		$jOverlap =  filter_var($_POST['inputOverlapSource'], FILTER_SANITIZE_STRING);
		$jPattern =  filter_var($_POST['inputPatternSource'], FILTER_SANITIZE_STRING);
		$jStatus  =  'Starting';
			
		for($i = 1100; $i <= 1399; $i++) {
			$jDocument  =  'source-document0'.$i.'.txt';
			$jIdentifier  =  'source_' . uniqid();
			
			$sql = 'INSERT INTO jobs(jIdentifier, jDocumentPath, jDocument, jSetup, jWindow, jOverlap, jPattern, jStatus) VALUES("'.$jIdentifier.'", "'.$jPath.'", "'.$jDocument.'", "'.$jSetup.'", "'.$jWindow.'", "'.$jOverlap.'", "'.$jPattern.'", "'.$jStatus.'")';
			mysql_query($sql) or die(mysql_error());
		}
	}
	return;
}
?>
