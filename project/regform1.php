<?php
echo"
<!DOCTYPE HTML>
<html>
<head><title>HTML Form</title>
<body style="background-image:url('Registeration.jpg');">
<link rel="stylesheet" href="mini.css">
<style>
.error {color: red;}
</style>
</head>
<body>";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  if (empty($_POST["name"])) {
    $nameErr = "Name is required";
  } else {
    $name = test_input($_POST["name"]);
  }
  
  if (empty($_POST["gender"])) {
    $genderErr = "Gender is required";
  } else {
    $gender = test_input($_POST["gender"]);
  }

  if (empty($_POST["name"])) {
    $nameErr = "Date of Birth is required";
  } else {
    $name = test_input($_POST["Date of Birth"]);
  }
}

function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}
}

echo"
<h1>Registration Form</h1>
<form target="_self" method="post">

Firstname :<br>
<input type="text" name="firstname" placeholder="firstname"><br>
<p style="text-align:left;"></p>
Lastname :<br>
<input type="text" name="lastname" placeholder="lastname"><br>
<p style="text-align:left;"></p>
Gender :<br>
<input type="radio" name="gender" value="Male">Male<br>
<input type="radio" name="gender" value="Female">Female<br>
<input type="radio" name="gender" value="Other" >Other<br>
<p style="text-align: center;"></p>
Date of Birth :<br>
<input type="date" name="DOB"><br>
<p style="text-align: center;"></p>
<input type="submit" value="Submit"><br>
</form><br><br>

<?php echo "Data inserted Successfully"; ?><br>
<?php echo $_POST["firstname"]; ?><br>
<?php echo $_POST["lastname"]; ?><br>
<?php echo $_POST["gender"]; ?><br>
<?php echo $_POST["dateofbirth"]; ?><br>
<?php echo "THANK YOU";?>

</body>
</html>";
?>
