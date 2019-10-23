<?php
echo "
<!DOCTYPE html>
<html>
<head>
  <title>Registration Form</title>
  <link rel='stylesheet' href='style.css'>
</head>
<body>";
echo " 

  <div class='header'>
  	<h2>Register</h2>
  </div>
	
  <form target='_self' method='post' action=''>
  
  	<div class='input-group'>
  	  Name:
  	  <input type='text' name='name' placeholder='name'>
  	</div>
  	<div class='input-group'>
  	  Username:
  	  <input type='text' name='username' placeholder='username'>
  	</div>
  	<div class='input-group'>
  	  Password:
  	  <input type='password' name='password' placeholder='******'>
  	</div>
  
 	<div> 	
	Gender:
	<input type='radio' name='gender' value='Male' checked>Male
	<input type='radio' name='gender' value='Female' >Female
	<input type='radio' name='gender' value='Others' >Others
	</div>	
	<div class='input-group'>	
	Date of Birth:
	<input type='date' name='dateofbirth'>
	</div>
	<div>
  	  <button type='submit' class='btn' name='submit'>Register</button>
  </div>
  	<p>
  		Already a member? <a href='login.php'>Sign in</a>
  	</p>
</form>
</body>
</html>
";
?>