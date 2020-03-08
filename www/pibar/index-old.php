<?php
include("dbconnect.php"); #<-- Hier steht alles zur verbindung zur Datenbank
?>
<html>
<head>
<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
<link rel="icon" href="/favicon.ico" type="image/x-icon">
<meta name="Tom Erber" content="PiBar Webinterface">
<title>PiBar Webinterface</title>
</head>
<body bgcolor="#
CFFFF">
<h1 align="center">Die PiBar Weboberfl&auml;che</h1>
<h3 align="center"> Aktuelle &uuml;bersicht</h3>
<br>

<?php
# Abfrage für Anzahl an Getränken (unbezahlt):
$abfrage = "SELECT COUNT( orders.id ) AS NumberOfOrders FROM orders WHERE isPaid=0";
$ergebnis = mysqli_query($db, $abfrage);
$ergebnis= mysqli_fetch_object($ergebnis);
$aktuelle_drinks = $ergebnis->NumberOfOrders;

#Abfrage Wann wurde das letzte getränk getrunken:
$abfrage = "SELECT orderDate FROM orders LIMIT 1";
$ergebnis = mysqli_query($db, $abfrage);
$ergebnis= mysqli_fetch_object($ergebnis);
$Zeitstempel = $ergebnis->orderDate;

#Ausgabe von Anzahl und Zeit
echo "Leztes Getr&auml;nk am ". $Zeitstempel . "<br>";
echo "Es wurdern ". $aktuelle_drinks ." Getr&auml;nke getrunken" ;
?>

<!-- Current score drinkers Tabelle -->
<div style='width: 40%;'>
<h4>Wer hatte wieviele Drinks?</h4>
<table border='1' rules='all'>
<tr>
<th>Name: </th>
<th>Drinks: </th>
</tr>

<!-- PHP teil der Current score drinkers Tabelle -->
<?php
$abfrage = "SELECT CONCAT( customers.firstName, ' ', customers.lastName ) AS Name, COUNT( orders.id ) AS NumberOfOrders FROM orders LEFT JOIN customers ON orders.customerId = customers.id WHERE isPaid=0 GROUP BY firstName ORDER BY `NumberOfOrders` DESC ";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{
  echo "<tr>";
  echo "<td align='center' width='150'>" . $row->Name . "</td>";
  echo "<td align='right'>" . $row->NumberOfOrders . "</td>";
  echo "</tr>";
}
?>
</table>
</div>

<!-- Current on Account Tabelle -->
<div style='width: 40%;'>
<h4>Wie viel auf der Karte?</h4>
<table border='1' rules='all'>
<tr>
<th>Name: </th>
<th>Zu bezahlen: </th>
</tr>

<!-- Php Teil von Account Tabelle -->
<?php
$abfrage = "SELECT CONCAT(c.firstName,' ', c.lastName ) AS 'Name', SUM( p.price ) AS 'Money' FROM customers c LEFT JOIN orders o ON o.customerId = c.id LEFT JOIN products p ON p.id = o.productId WHERE o.isPaid =0 GROUP BY c.id ORDER BY Money DESC";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{
  echo "<tr>";
  echo "<td align='center' width='150'>" . $row->Name . "</td>";
  echo "<td align='center' width='167'>" . $row->Money ." Euro" . "</td>";
  echo "</tr>";
}
?>
</table>
</div>

<!-- Current drinks Tabelle -->
<div style='width: 40%;'>
<h4>Aktuelle Getr&auml;nke:</h4>
<table border='1' rules='all'>
<tr>
<th>Name: </th>
<th>Anzahl: </th>
</tr>

<!-- PHP teil von Current drinks -->
<?php
$abfrage = "SELECT products.name AS Name, COUNT( orders.id ) AS NumberOfOrders FROM orders LEFT JOIN products ON products.id = orders.productId WHERE isPaid=0 GROUP BY Name ORDER BY `NumberOfOrders` DESC LIMIT 0,5";
$ergebnis = mysqli_query($db, $abfrage);
while($row = mysqli_fetch_object($ergebnis))
{
  echo "<tr>";
  echo "<td align='left'>" . $row->Name . "</td>";
  echo "<td align='right'width='90'>" . $row->NumberOfOrders . "</td>";
  echo "</tr>";
}
?>
</table>
</div>

<?php mysqli_close($db);?> <!-- Datenbank verbindung schließen-->

<script>
#Hier macht Markus sein Zeugs
</script>

</body>
</html>
