<?php
require_once 'data.php';
echo "
<!DOCTYPE html>
<html>
<head>
  <title>Registration Form</title>
  <link rel='stylesheet' href='style.css'>
</head>
<body>";
if (isset($_POST['submit'])) 
{
//  echo "Form submitted";
    $name = $_POST['name'];
    $username =$_POST['username'];
    $password = $_POST['password'];
    $gender = $_POST['gender'];
    $dateofbirth = $_POST['dateofbirth'];

  
      // ensure that form fields are filled properly

    if ($name == '') {
      echo "Name is Required" . "<br>";
    }

    if ($username == '') {
      echo "Username is Required";
    }

  
  
    //if (count($errors) == 0) {
    else{ 
  
    $query = "INSERT INTO membersdetails (name, username, password, gender, dateofbirth) 
    VALUES('$name', '$username', '$password', '$gender', '$dateofbirth')";

    mysqli_query($db, $query);
    $_SESSION['username'] = $username;
    $_SESSION['success'] = "You are now logged in";
    //header('location: index.php');
  }
  echo $_POST['name'].'<br>'; 
  echo $_POST['username'].'<br>';
  echo $_POST['gender'].'<br>';
  echo $_POST['dateofbirth'].'<br>';

}

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



