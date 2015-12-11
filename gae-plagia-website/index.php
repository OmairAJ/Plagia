<?php
error_reporting(0);
//session_start();

//if ($_SESSION["login"] != "true"){
//	header("Location:index.php");
//}

include('dbConnection.php');
?>
<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!--> <html class="no-js" lang="en"> <!--<![endif]-->

<head>
<title>Plagia</title>
<!-- meta tags -->
<meta charset="utf-8">
<meta http-equiv="Content-Type" content="text/html">
<meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1">
<meta http-equiv="imagetoolbar" content="false">
<meta name="application-name" content="Plagia">
<meta name="msapplication-tap-highlight" content="no">
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, target-densitydpi=device-dpi, user-scalable=yes">
<meta name="author" content="Omair Jaswal">
<meta name="description" content="">
<meta name="keywords" content="">
<meta name="copyright" content="&copy; 2015 Plagia. All Rights Reserved.">
<!-- styles -->
<link rel="stylesheet" href="css/normalize.min.css">
<link rel="stylesheet" href="css/bootstrap.min.css">
<link rel="stylesheet" href="css/bootstrap-theme.min.css">
<link rel="stylesheet" href="css/main.css">
<!-- fonts -->
<link rel="stylesheet" href="css/font-awesome.min.css">
<!-- pre scripts -->
<script src="js/modernizr.min.js"></script>
<script src="js/ie10viewport-bugworkaround.js"></script>
<!--[if lt IE 9]>
<script src="js/html5shiv-printshiv.min.js"></script>
<script src="js/respond.min.js"></script>
<![endif]-->
<!-- icons -->
<link rel="shortcut icon" href="favicon.ico">
<link rel="apple-touch-icon-precomposed" href="apple-touch-icon-precomposed.png" />
<link rel="apple-touch-icon-precomposed" sizes="72x72" href="apple-touch-icon-72x72-precomposed.png" />
<link rel="apple-touch-icon-precomposed" sizes="114x114" href="apple-touch-icon-114x114-precomposed.png" />
<link rel="apple-touch-icon-precomposed" sizes="144x144" href="apple-touch-icon-144x144-precomposed.png" />
<link rel="apple-touch-icon-precomposed" sizes="1024x1024" href="apple-touch-icon-1024x1024-precomposed.png" />
<!-- seo -->
<meta name="robots" content="noindex">
<meta name="title" content="Plagia">
</head>

<body>
<!-- header -->
<div id="header">
  <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
    <div class="container-fluid">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#main-top-navbar">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </button>
        <a class="navbar-brand"><i class="fa fa-graduation-cap"></i> Plagia</a>
      </div>
      <div class="collapse navbar-collapse" id="main-top-navbar">
        <ul class="nav navbar-nav navbar-right">
          <li class="active"><a href="#"><i class="fa fa-home"></i></a></li>
          <li><a href="" data-toggle="modal" data-target="#sysSettings"><i class="fa fa-cog"></i></a></li>
          <!--li><a href="logout.php"><i class="fa fa-sign-out"></i></a></li-->
        </ul>
      </div>
    </div>
  </nav>
</div>
<!-- content -->
<div class="container">
  
  <p class="lead text-justify">A simple Plagiarism Detection System based on contextual n-grams of CoReMo with a number of simplifying variations to the approach implemented using various cloud technologies such as Google AppEngine, Amazon Web Services &amp; OpenStack.</p>
  
  <div class="row">
    <div class="col-sm-12">
    <div class="panel panel-primary">
      <div class="panel-heading">
        <h3 class="panel-title">Start a job</h3>
      </div>
      
      <div class="panel-body">
        <form action="" method="post" class="form-horizontal" id="jobForm">
          <div class="row">
            <div class="col-sm-6">
              <div class="form-group">
                <label for="inputDocument" class="col-sm-3 control-label">Document</label>
                <div class="col-sm-9">
                  <select name="inputDocument" size="4" class="form-control">
                  <?php for($i = 10; $i <= 49; $i++) {
					  $jobDocument = 'suspicious-document000'.$i.'.txt'; ?>
                    <option><?php echo $jobDocument; ?></option>
                  <?php } ?>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label for="inputSetup" class="col-sm-3 control-label">Cloud Setup</label>
                <div class="col-sm-9">
                  <label class="radio-inline"><input type="radio" name="inputSetup" id="inputSetup1" value="ee" checked> E-E </label>
                  <label class="radio-inline disabled"><input type="radio" name="inputSetup" id="inputSetup2" value="eo" disabled> E-O </label>
                  <label class="radio-inline disabled"><input type="radio" name="inputSetup" id="inputSetup3" value="oe" disabled> O-E </label>
                  <label class="radio-inline disabled"><input type="radio" name="inputSetup" id="inputSetup4" value="oo" disabled> O-O </label>
                </div>
              </div>
            </div>
            <div class="col-sm-6">
              <div class="form-group">
                <label for="inputWindow" class="col-sm-3 control-label">Window Size</label>
                <div class="col-sm-9">
                  <input type="number" class="form-control" name="inputWindow" id="inputWindow" min="2" value="5" placeholder="5">
                </div>
              </div>
              <div class="form-group">
                <label for="inputOverlap" class="col-sm-3 control-label">Overlap Size</label>
                <div class="col-sm-9">
                  <input type="number" class="form-control" name="inputOverlap" id="inputOverlap" min="1" value="4" placeholder="4">
                </div>
              </div>
              <div class="form-group">
                <label for="inputPattern" class="col-sm-3 control-label">Pattern Size</label>
                <div class="col-sm-9">
                  <input type="number" class="form-control disabled" name="inputPattern" id="inputPattern" min="1" value="3" placeholder="3" disabled>
                </div>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-sm-12">
              <div class="form-group">
                <div class="col-sm-offset-3 col-sm-6">
                  <button type="submit" class="btn btn-primary btn-block btn-lg" id="jobSubmit">Launch!</button>
                </div>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
    </div>
  </div>
  
  <div class="row">
    <div class="col-sm-12">
      <div class="panel panel-default">
        <div class="panel-heading">
          <h3 class="panel-title">Jobs in progress</h3>
        </div>
        <table class="table table-striped table-hover">
          <thead>
            <tr>
              <th class="text-center">#</th>
              <th>Documents</th>
              <th class="text-center">Setup</th>
              <th>Parameters</th>
              <th class="text-center">Time Started</th>
              <th class="text-center">Status</th>
            </tr>
          </thead>
          <tbody id="tasks">
          </tbody>
        </table>
      </div>
    </div>
    
  </div>
</div>
<!-- footer -->
<div id="footer">
  <nav class="navbar navbar-default navbar-fixed-bottom navbar-inverse">
    <div class="container-fluid">
      <div class="col-sm-12">
        <small class="navbar-text navbar-right">&copy; 2015 Plagia. All Rights Reserved.</small>
      </div>
    </div>
  </nav>
</div>
<!-- Modal -->
<div class="modal fade" id="sysSettings" tabindex="-1" role="dialog" aria-labelledby="sysSettingsLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title lead" id="sysSettingsLabel">(re)Generate indexes of source documents</h4>
      </div>
      <form action="" method="post" class="form-horizontal" id="jobFormSources">
        <div class="modal-body">
          <h4>Parameters</h4>
          <div class="col-sm-12">
            <div class="form-group">
              <label for="inputSetup" class="col-sm-4 control-label">Cloud Setup</label>
              <div class="col-sm-8">
                <label class="radio-inline"><input type="radio" name="inputSetupSource" id="inputSetupSource1" value="ee" checked> Amazon </label>
                <label class="radio-inline disabled"><input type="radio" name="inputSetupSource" id="inputSetupSource2" value="oo" disabled> OpenStack </label>
              </div>
            </div>
            <div class="form-group">
              <label for="inputWindowSource" class="col-sm-4 control-label">Window Size</label>
              <div class="col-sm-8">
                <input type="number" class="form-control" name="inputWindowSource" id="inputWindowSource" min="2" value="5" placeholder="5">
              </div>
            </div>
            <div class="form-group">
              <label for="inputOverlapSource" class="col-sm-4 control-label">Overlap Size</label>
              <div class="col-sm-8">
                <input type="number" class="form-control" name="inputOverlapSource" id="inputOverlapSource" min="1" value="4" placeholder="4">
              </div>
            </div>
            <div class="form-group">
              <label for="inputPatternSource" class="col-sm-4 control-label">Pattern Size</label>
              <div class="col-sm-8">
                <input type="number" class="form-control" name="inputPatternSource" id="inputPatternSource" min="1" value="3" placeholder="3">
              </div>
            </div>
          </div>
          <div class="row">
            <div class="col-sm-12">
              <p class="text-danger small"><strong>Warning:</strong> This is both a time consuming and resource intensive (costly) process.</p>
            </div>
          </div>
          <div class="row">
            <div class="col-sm-12">
              <div class="form-group">
                <div class="col-sm-3">
                  <button type="submit" class="btn btn-primary btn-block" id="jobSubmitSources">Start</button>
                </div>
                <div class="col-sm-3 pull-right">
                  <button type="button" class="btn btn-default btn-block" data-dismiss="modal">Cancle</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>
  </div>
</div>
<!-- post scripts -->
<?php //<script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script> ?>
<script>window.jQuery || document.write('<script src="js/jquery.min.js"><\/script>')</script>
<script src="js/bootstrap.min.js"></script>
<script src="js/retina.min.js"></script>
<script src="js/holder.js"></script>
<script src="js/plugins.js"></script>
<script src="js/main.js"></script>
<script>
setInterval(function(){
	$.ajax({
		type: 'POST', 
		url: 'jobCurrent.php', 
		data: {}, 
		dataType: 'json', 
		success: function(data) {
			$('#tasks').html('');
			$.each(data, function(key, value) {
				$jColor = '';
				$jStatus = '';
				
				if (value.jSetup == 'ee') {
					$jSetup = 'E-E';
				} else if (value.jStatus == 'eo') {
					$jSetup = 'E-O';
				} else if (value.jStatus == 'oe') {
					$jSetup = 'O-E';
				} else if (value.jStatus == 'oo') {
					$jSetup = 'O-O';
				}
				
				if (value.jStatus == 'Starting') {
					$jColor = 'primary';
				} else if (value.jStatus == 'Terminated') {
					$jColor = 'danger';
				} else if (value.jStatus == 'Completed') {
					$jColor = 'success';
				} else if (value.jStatus == 'Waiting') {
					$jColor = 'warning';
				} else if (value.jStatus == 'Indexing') {
					$jColor = 'info';
				} else if (value.jStatus == 'Index Mapped') {
					$jColor = 'warning';
				} else if (value.jStatus == 'Index Reducing') {
					$jColor = 'info';
				} else if (value.jStatus == 'Indexed') {
					$jColor = 'warning';
				} else if (value.jStatus == 'Matching') {
					$jColor = 'info';
				} else if (value.jStatus == 'Match Mapped') {
					$jColor = 'warning';
				} else if (value.jStatus == 'Match Reducing') {
					$jColor = 'info';
				} else if (value.jStatus == 'Matched') {
					$jColor = 'warning';
				}
				
				$('#tasks').append('<tr id="' + value.jID + '">' +
				'<td class="text-center"><strong>' + value.jID + '</strong></td>' +
				'<td class="text-info"><a href="' + value.jDocumentResult + '"></a>' + value.jDocument + '</td>' +
				'<td class="text-center">' + $jSetup + '</td>' +
				'<td>Window: ' + value.jWindow + '; Overlap: ' + value.jOverlap + '; Pattern: ' + value.jPattern + '</td>' +
				'<td class="text-center">' + value.jTimestamp + '</td>' +
				'<td class="text-center"><span class="label label-' + $jColor + '">' + value.jStatus + '</span></td>' +
				'</tr>');
			});
		}
	});
}, 3000);
</script>
<script type="text/javascript">
$(document).ready(function() {
	var form = $('#jobForm');
	var submit = $('#jobSubmit');
	
	form.on('submit', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: 'jobLaunch.php', 
			type: 'POST', 
			dataType: 'html', 
			data: form.serialize(),
			beforeSend: function() {
				submit.html('Launching...');
			},
			success: function(data) {
				form.trigger('reset');
				submit.html('Launch!');
			},
			error: function(e) {
				console.log(e)
			}
		});
	});

	var formSource = $('#jobFormSources');
	var submitSource = $('#jobSubmitSources');
	
	formSource.on('submit', function(e) {
		e.preventDefault();
		
		$.ajax({
			url: 'jobSources.php', 
			type: 'POST', 
			dataType: 'html', 
			data: formSource.serialize(),
			beforeSend: function() {
				submitSource.html('Starting...');
			},
			success: function(data) {
				formSource.trigger('reset');
				submitSource.html('Start');
				$('#sysSettings').modal('hide')
			},
			error: function(e) {
				console.log(e)
			}
		});
	});
});
</script>
</body>
</html>