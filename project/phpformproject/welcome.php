<?php

$username=" ";
$password=" ";

session_start();

if(isset($_SESSION['username'])){

  echo"<h1>Welcome ".$_SESSION['username']."</h1>";

  echo "<a href ='Login.php'>Login</a><br>";


  echo" <br><a href='Logout.php'><input type=button value=logout name=Logout></a>";
}
else{
  if($_POST['username']==$username && $_POST['password']==$password){
    $_SESSION['username']=$" ";
  }
  echo "<script>location.href='welcome.php'</script>";
}
else
{
  echo"<script>alert('username or password incorrect')</script>";

  echo"<script>location.href='Login.php'</script>";
}
?>