<?php
require_once 'data.php';
echo "
<!DOCTYPE html>
<html>
<head>
  <title>Registration system </title>
  <link rel='stylesheet' href='style.css'>
</head>
<body>";
if (isset($_POST['login_user'])) {
  $username = $_POST['username'];
  $password = $_POST['password'];
if (count($errors) == 0) {
   // $password = ($password);
    $query = "SELECT * FROM membersdetails WHERE username='$username' AND password='$password'";
    $results = mysqli_query($db, $query);
    if (mysqli_num_rows($results) == 1) {
      $_SESSION['username'] = $username;
      $_SESSION['success'] = "You are now logged in";
      header('location: wel.php');
    }else {
        echo "Wrong username or Password. Please try again.";
    }
  }
}
echo "
  <div class='header'>
  	<h2>Login</h2>
  </div>
	 
  <form method='post' action=''>
  
  	<div class='input-group'>
  		Username:
  		<input type='text' name='username' placeholder='username'>
  	</div>
  	<div class='input-group'>
  		Password:
  		<input type='password' name='password' placeholder='password'>
  	</div>
  	<div class='input-group'>
  		<button type='submit' class='btn' name='login_user'>Login</button>
  	</div>
  	<p>
  		Not yet a member? <a href='registration.php'>Sign up</a>
  	</p>
</form>
</body>
</html>
";
?>