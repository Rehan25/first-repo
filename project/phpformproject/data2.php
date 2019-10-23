<?php 

session_start();

$con = mysqli_connect('localhost','Rehan','password');

mysqli_select_db($con, 'dbusers');

$firstname = $_POST['firstname'];
$lastname = $_POST['lastname'];
$Username = $_POST['Username'];
$Password = $_POST['Password'];
$Gender = $_POST['Gender'];
$dateofbirth = $_POST['dateofbirth'];

$s = " select * from 'Registeration Details' where name = '$firstname'";

$result = mysqli_query($con ,$s);

$num = mysqli_num_rows($result);

if($num == 1){
	echo "Username already Taken";
	}
	else{
	$reg = "insert into 'Registeration Details'(firstname , lastname, Username , Password , Gender , dateofbirth) values ('$firstname' , '$lastname', '$Username' , '$Password' , '$Gender' , '$dateofbirth')";
	
	mysqli_query($con, $reg);

    echo"Registeration Succesful";

	}
?>
