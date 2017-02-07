# Plagia
A simple Plagiarism Detection System based on contextual n-grams of CoReMo with a number of simplifying variations to the approach implemented using various cloud technologies such as Google AppEngine &amp; Amazon Web Services.<br />
<br />
The system consists of three applications:<br />
<ol>
<li>The Web Application</li>
<li>The Controller Application</li>
<li>The MapReduce Applications for Indexing and Macthing</li>
</ol>
The Web Application is implemented on Google App Engine along with a Google Cloud SQL database for queuing and keeping track of various plagirism detection jobs.<br />
<br />
The Controller Application is implemented on a continuously running Amazon EC2 instance. Its only function is to query the Google Cloud SQL database and pickup jobs to launch Amazon EMR with the stored steps. These steps are either the Indexing stage or Matching stage of the job. Each of these stages have there own respective two applications for map and reduce processing using Hadoop. This is automatically handled by Amazon EMR.<br />
<br />
This was a coursework project meant to enable students to learn by trial and error about cloud computing concepts, tools and techniques using various technologies.<br />
<br />
The project was completed with a successful test of the system.<br />
<small>Unfortunatly, OpenStack could not be integrated or tested.</small><br />
<br />
<strong>Technologies Used</strong><br />
<ul>
<li>PHP</li>
<li>Bootstrap</li>
<li>Python</li>
<li>Boto</li>
<li>Amazon EC2</li>
<li>Amazon EMR</li>
<li>Google App Engine</li>
<li>Google Cloud SQL (MySQL)</li>
</ul>
<br />
