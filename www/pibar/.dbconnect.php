<?php
$db = mysqli_connect("localhost", "pibaruser", "DPSG-Franziskus", "pibar");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}
?>
