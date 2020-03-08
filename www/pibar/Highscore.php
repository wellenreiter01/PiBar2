<?php
include(".dbconnect.php"); #<-- Hier steht alles zur verbindung zur Datenbank
?>
<html>
<head>
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
<link rel="icon" href="/favicon.ico" type="image/x-icon">
<meta name="Tom Erber" content="PiBar Webinterface">
<meta name="Wellenreiter" content="PiBar2 Webinterface">
<link href="admin/admin_style.css" type="text/css" rel="stylesheet">
<title>PiBar Webinterface</title>
</head>

<body>
<div><image class=logo src='images/logo_dpsg_franziskus.png'> </div>
<div align=center class=overlap>
    <h1>Die PiBar Weboberfl&auml;che</h1>
    <p>
        <input type=button type=button onClick="location.href='/'" value='Zur Startseite'>
    </p>
    <h3 > Aktuelle &Uuml;bersicht von Heute</h3>
</div>

<!-- Highscore drinkers Tabelle -->
<br><br>
<div class=float-right>
<table  >
<tr colspan=2>
    <th><h4>Highscore Trinker:</h4></th>
</tr>
<tr>
<th>Name:</th>
<th>Anzahl Drinks: </th>
</tr>

<!-- PHP teil der Highscore drinkers Tabelle -->
<?php
$abfrage = "SELECT CONCAT( customers.firstName, ' ', customers.lastName ) AS Name, COUNT( orders.id ) AS NumberOfOrders,orderDate FROM orders LEFT JOIN customers ON orders.customerId = customers.id GROUP BY firstName ORDER BY `NumberOfOrders` DESC ";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{
  echo "<tr>";
  echo "<td align='center' width='150'>" . $row->Name . "</td>";
  echo "<td align='center'>" . $row->NumberOfOrders . "</td>";
  echo "</tr>";
}
?>
</table>
</div>

<!-- Highscore on Account drinkers Tabelle -->
<div class=float-right>

<table>
<tr colspan: 2>
    <th><h4>Highscore Kosten:</h4></th>
</tr>
<tr>
<th>Name: </th>
<th>vertrunken: </th>
</tr>

<!-- php teil von Highscore on Account drinkers Tabelle -->
<?php
$abfrage = "SELECT CONCAT(c.firstName,' ', c.lastName ) AS 'Name', SUM( p.price ) AS 'Money' FROM customers c LEFT JOIN orders o ON o.customerId = c.id LEFT JOIN products p ON p.ean  = o.productId where  GROUP BY c.id ORDER BY Money DESC";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{

if ($row->Money != ""){
echo "<tr>";
echo "<td align='center' width='150'>" . $row->Name . "</td>";
echo "<td align='center' width='150'>" . $row->Money ." Euro" . "</td>";
echo "</tr>";}
}
?>
</table>
</div>

<!-- Highscore Drinks Tabelle -->
<div class=float-right>

<table>
<tr colspan= 2>
    <th><h4>Highscore Getränke:</h4></th>
<tr>
<th>Name: </th>
<th>Bestellt: </th>
</tr>

<!-- php teil vonHighscore Drinks Tabelle -->
<?php
$abfrage = "SELECT products.name AS Name, COUNT( orders.id ) AS NumberOfOrders FROM orders LEFT JOIN products ON products.ean = orders.productId WHERE GROUP BY Name ORDER BY `NumberOfOrders` DESC LIMIT 0,5";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{
  echo "<tr>";
  echo "<td align='left'>" . $row->Name . "</td>";
  echo "<td align='center'width='100'>" . $row->NumberOfOrders . "</td>";
  echo "</tr>";
}
?>
</table>
</div>

