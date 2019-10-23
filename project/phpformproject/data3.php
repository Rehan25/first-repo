<?php

session_start();

$con = mysqli_connect('localhost' , 'Rehan' , 'password', 'dbusers');
if($con){
	//echo"connection successful";
	}
	else{
	echo "no connection";
	}

//$s = "select * from RegisterationDetails where name = '$firstname'";


?>