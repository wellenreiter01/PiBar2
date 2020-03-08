<?php
$db = mysqli_connect("localhost", "root", "<PASSWORD>", "pibar");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}
?>
