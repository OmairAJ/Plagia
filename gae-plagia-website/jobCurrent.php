<?php 
include('dbConnection.php');

$sql   = 'SELECT * FROM jobs';
$query = mysql_query($sql) or die(mysql_error());

$return_array = array();

while ($row = mysql_fetch_array($query)) {
	$row_array['jID']         =  $row['jID'];
	//$row_array['jIdentifier'] =  $row['jIdentifier'];
	$row_array['jDocumentResult']   =  $row['jDocumentResult'];
	$row_array['jDocument']   =  $row['jDocument'];
	$row_array['jSetup']      =  $row['jSetup'];
	$row_array['jWindow']     =  $row['jWindow'];
	$row_array['jOverlap']    =  $row['jOverlap'];
	$row_array['jPattern']    =  $row['jPattern'];
	$row_array['jStatus']     =  $row['jStatus'];
	$row_array['jTimestamp']  =  $row['jTimestamp'];
	
	if ($row['jStatus'] == 'Matched') {
		$sql = 'UPDATE jobs SET jStatus="Completed" WHERE jID='.$row['jID'];
		mysql_query($sql) or die(mysql_error());
	}
	
    array_push($return_array, $row_array);
}

echo json_encode($return_array);

?>