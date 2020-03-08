<?php
include("../.dbconnect.php");
?>
<html>
<head>
<meta name="Tom Erber" content="PiBar Webinterface">
<meta name="Wellenreiter" content="PiBar2 Webinterface">
<link href="admin_style.css" type="text/css" rel="stylesheet">

<title>PiBar Product view</title>
</head>
<body>
<span><image class=logo src='/images/logo_dpsg_franziskus.png'> </span>
<h1 align="center">Product overview</h1>

<div align=center>
<p>
<input type=button type=button onClick="location.href='/'" value='Zur Startseite'>
</p>

    <table border=1>
        <tr>
        <th colspan= 6> Produkt anlegen: </th>
        </tr>
        <form action="product.php" method="post">
        <tr>
        <td align='left'>Name:</td>
        <td align='left'><input type="text" name="name" required></td>
        </tr>
        <tr> 
        <td align='left'>EAN:</td>
        <td align='left'><input type="text" name="ean" required></td>
        </tr>
        <tr> 
        <td align='left'>Getränkegruppe:</td>
        <td colspan=2 ='left'><input type="number" min="0" max = "5" step="1" name="Getränkegruppe" required>
        0 = alkoholfrei, 1 = Alkoholhaltig, 2 = Hochprozentig</td>
        </tr>
        <TR><td align='left'>Preis in Euro:</td>
        <td align='left'><input type="number" min="0.10" step="0.1" name="price" required></td>
        </tr>
        <tr> 
        <td align='left'>an Lager:</td>
        <td align='left'><input type="number" min="1" name="stock" required></td>
        </tr>
        <tr>
        <td colspan = 2 align='center'><input type="submit" name="add" value="Produkt anlegen!"></td>
        </tr>
    </table>

</form>
<?php

if(isset($_POST['add'])){
$update = "INSERT INTO products SET ean='$_POST[ean]', name='$_POST[name]',  drinktype='$_POST[Getränkegruppe]', price='$_POST[price]', stock='$_POST[stock]'";
mysqli_query($db, $update);
echo "Done!";
echo "<br>";
};

if(isset($_POST['update'])){
$update = "UPDATE products SET ean='$_POST[ean]', name='$_POST[name]',drinktype= '$_POST[Getränkegruppe]', price='$_POST[price]', stock='$_POST[stock]' WHERE id='$_POST[hidden]'";
mysqli_query($db, $update);
echo "Done!";
echo "<br>";
};

if(isset($_POST['delete'])){
$update = "DELETE FROM orders WHERE productId='$_POST[hidden]'";
mysqli_query($db, $update);
$update = "DELETE FROM products WHERE id='$_POST[hidden]'";
mysqli_query($db, $update);
echo "Done!";
echo "<br>";
};

$sql= "SELECT * FROM products ORDER BY name";
$ergebnis = mysqli_query($db, $sql);

echo "<br><table border=1>
<tr>
    <th colspan = 6> Produkte: </th>
</tr>
<tr>
<th>EAN:</th>
<th>Produkt:</th>
<th width=60px> Gruppe: </th>
<th>Preis:</th>
<th>an Lager:</th>
<th>Aktion?</th>
</tr>";

while($row = mysqli_fetch_object($ergebnis))
{
echo "<form action=product.php method=post>";
echo "<tr>";
echo "<td align='left'>" . "<input type=text size=13 name=ean required value='$row->ean'>"."</td>"; 
echo "<td align='left'>" . "<input type=text name=name required value='$row->name'>"."</td>";
echo "<td align='left'>" . "<input type=number size=3 setp='1' min='0' max = '3' name=Getränkegruppe required value=" . $row->drinktype ."> </td>";
echo "<td align='left'>" . "<input type=number  step='0.1' max=100 name=price required value=" . $row->price ."> </td>";
echo "<td align='left'>" . "<input type=number setp='1' min='0'  name=stock required value=" . $row->stock ."> </td>";
echo "<td>" . "<input type=submit name=update value=change" . ">" . " " . "<input type=submit name=delete value=delete" . "> </td>";
echo "<td>" . "<input type=hidden name=hidden value=" . $row->id ."> </td>";
echo "</tr>";
echo "</form>";
}
echo "</table>";
echo "<br>";
mysqli_close($db);
?>

<input type=button type=button onClick="location.href='/'" value='Zur Startseite'>

</div>
</body>
</html>

