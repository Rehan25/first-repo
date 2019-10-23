<?php
require_once 'data3.php';
echo "
<!DOCTYPE html>
<html>
<link rel='stylesheet' href='mini.css'>
<body>";

if (isset($_POST['login_user'])) {
  $username = $_POST['username'];
  $password = $_POST['password'];

  if ($username==''){
  	echo 'Username is required';
  }
  if ($password==''){
  	echo 'Password is required';
  }
  else{

$query = "select * from RegisterationDetails where username='$username' and password='$password'";
    $results = mysqli_query($con, $query);
    if (mysqli_num_rows($results) == 1) {
      $_SESSION['username'] = $username;
      $_SESSION['password'] = $password;
      $_SESSION['success'] = "You are now logged in";
      header('location: welcome.php');
    }
    else {
        echo "Wrong username or Password. Please try again.";
    }
}
}
echo "
<form method='post' action=''>
Username: <input type='text' name='username' /><br></br>
Password: <input type='password' name='password' />
<input type='submit' name='login_user' value='Login'/>

</form>
</body>
</html>";
?>