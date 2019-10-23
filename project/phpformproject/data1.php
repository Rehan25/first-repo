<?php

    //session_start();

    // variable declaration
    $servername = 'localhost';
    $username = 'Rehan';
    $password = 'password';
    $database = 'dbusers';
// connect to database
        $db = mysqli_connect($servername, $username, $password, $database);
if (!$db) {
      die("Connection failed: " . mysqli_connect_error());
}

    // $errors = array();
    //$_SESSION['success'] = "";

    // if register button clicked receive all inputs from the form
    


//     $_SESSION['username'] = $username;
//     $_SESSION['success'] = "You are now logged in";
//     header('location: index.php');
//   }

// }

// // login user


?>