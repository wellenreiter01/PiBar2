<?php
include("../.dbconnect.php");
?>
<html>
<head>
<meta name="Wellenreiter" content="PiBar2 Webinterface">
<link href="admin_style.css" type="text/css" rel="stylesheet">
<title>PiBar Webinterface</title>
</head>
  <body>
    <span><image class=logo src='/images/logo_dpsg_franziskus.png'> </span>
    <h1 align="center">Willkommen in der PiBar</h1>
    <div align=center>
      <p>
        <input type=button type=button onClick="location.href='/'" value='Zur Startseite'>
      </p>
        <?php


        if(isset($_POST['update'])){
        $update = "UPDATE customers SET firstName='$_POST[firstname]', lastName='$_POST[lastname]',userCard='$_POST[usercard]', usergroup='$_POST[usergroup]', admin='$_POST[admin]', balance='$_POST[balance]'  WHERE id='$_POST[hidden]'";
        mysqli_query($db, $update);
        };

        if(isset($_POST['delete'])){
        # Aus der datenbank alle bestellungen rauslöschen von dem User
        $update = "DELETE FROM orders WHERE customerId ='$_POST[hidden]'";
        mysqli_query($db, $update);
        #Dann den User an sich löschen
        $update = "DELETE FROM customers WHERE id='$_POST[hidden]'";
        mysqli_query($db, $update);
        echo "Done!";
        echo "<br>";
        };

        $sql= "SELECT * FROM customers WHERE admin=0 and usergroup > 0 Order by id";
        $ergebnis = mysqli_query($db, $sql);
        
        echo "<table >
        <tr>
        <th colspan=9 align=center>User: </th>
        <tr>
        <th width= 10>Nr: </th>
        <th>RFID:</th>
        <th>Name:</th>
        <th>Hausname:</th>
        <th>Karte:</th>
        <th width=20> Gruppe</th>
        <th width=20> Admin</th>
        <th width=20> Guthaben</th>
        <th>Aktion</th>
        </tr>";

        while($row = mysqli_fetch_object($ergebnis))
        {
        echo "<form action=users.php method=post>";
        echo "<tr>";
        echo "<td align='left'>".  $row->id." </td>";
        echo "<td align='left'>".$row->tagid." </td>";  
        echo "<td align='left'>" . "<input type=text name=firstname required value='$row->firstName'>" ." </td>";
        echo "<td align='left'>" . "<input type=text name=lastname value='$row->lastName'>" . " </td>";
        echo "<td align='left'>" . "<input title= 'CREDIT <Nummer> für Rechnungskarte eingeben
                    sonst CHIP <Nummer> eingeben' type=text name=usercard value='$row->userCard'>" . " </td>";
        echo "<td align='right'>" . "<input type=number min=0 max =3 step=1 title= '0: Freie Karte
        1: Alkoholfreie Getänke\n2: Alkoholhlatige Getränke' name=usergroup value=" . $row->usergroup . "> </td>";
        echo "<td align='right'>" . "<input type=number min=0 max =3 step=1 name=admin value=" . $row->admin . "> </td>";
        echo "<td align='right'>" . "<input type=number min=0 max=999 step=.1 name=balance value=" . $row->balance  . "> </td>";
        echo "<td>" . "<input type=submit name=update value=Update>" . " " . "<input type=submit name=delete value=delete>"."</td>";
        echo "<td>" . "<input type=hidden name=hidden value=" . $row->id ."> </td>";
        echo "</tr>";
        echo "</form>";
        }

        echo "</table>";
        echo "<br>";
        $sql= "SELECT * FROM customers WHERE admin=1 and usergroup > 0 order by id ";
        $ergebnis = mysqli_query($db, $sql);
        
        echo "<table >
        <tr>
            <th colspan=9>Admins:</th>
        </tr>
        <tr>
        <th width= 10>Nr: </th>
        <th>RFID:</th>
        <th>Name:</th>
        <th>Hausname:</th>
        <th>Karte:</th>
        <th width=20> Gruppe</th>
        <th width=20> Admin</th>
        <th width=20> Guthaben</th>
        <th>Aktion</th>
        </tr>";

        while($row = mysqli_fetch_object($ergebnis))
        {
        echo "<form action=users.php method=post>";
        echo "<tr>";
        echo "<td align='left'>".  $row->id." </td>";
        echo "<td align='left'>".$row->tagid." </td>";  
        echo "<td align='left'>" . "<input type=text name=firstname required value='$row->firstName'>" ." </td>";
        echo "<td align='left'>" . "<input type=text name=lastname value='$row->lastName'>" . " </td>";
        echo "<td align='left'>" . "<input title= 'CREDIT <Nummer> für Rechnungskarte eingeben
                    sonst CHIP <Nummer> eingeben' type=text name=usercard value='$row->userCard'>" . " </td>";
        echo "<td align='right'>" . "<input type=number min=0 max =3 step=1 title= '0: Freie Karte
        1: Alkoholfreie Getänke\n2: Alkoholhlatige Getränke' name=usergroup value=" . $row->usergroup . "> </td>";
        echo "<td align='right'>" . "<input type=number min=0 max =3 step=1 name=admin value=" . $row->admin . "> </td>";
        echo "<td align='right'>" . "<input type=number min=0 max=999 step=.1 name=balance value=" . $row->balance  . "> </td>";
        echo "<td>" . "<input type=submit name=update value=Update>" . " " . "<input type=submit name=delete value=delete>"."</td>";
        echo "<td>" . "<input type=hidden name=hidden value=" . $row->id ."> </td>";
        echo "</tr>";
        echo "</form>";
        }

        echo "</table>";
        echo "<br>";
        $sql= "SELECT * FROM customers WHERE usergroup = '0' Order by id";
        $ergebnis = mysqli_query($db, $sql);
        echo "<table>
        <tr>
            <th colspan=7> Freie RFID: </th>
        </tr>
        <tr>
        <th width= 10>Nr: </th>
        <th>RFID:</th>
        <th>Name:</th>
        <th>Hausname:</th>
        <th>Karte:</th>
        <th width=20> Gruppe</th>
        <th>Aktion</th>
        </tr>";

        while($row = mysqli_fetch_object($ergebnis))
        {
        echo "<form action=users.php method=post>";
        echo "<tr>";
        echo "<td align='left'>".  $row->id." </td>";
        echo "<td align='left'>".$row->tagid." </td>";  
        echo "<td align='left'>" . "<input type=text name=firstname required value='$row->firstName'>" ." </td>";
        echo "<td align='left'>" . "<input type=text name=lastname value='$row->lastName'>" . " </td>";
        echo "<td align='left'>" . "<input title= 'CREDIT <Nummer> für Rechnungskarte eingeben
                    sonst CHIP <Nummer> eingeben' type=text name=usercard value='$row->userCard'>" . " </td>";
        echo "<td align='right'>" . "<input type=number min=0 max =3 step=1 title= '0: Freie Karte
        1: Alkoholfreie Getänke\n2: Alkoholhlatige Getränke' name=usergroup value=" . $row->usergroup . "> </td>";
        echo "<td>" . "<input type=submit name=update value=Update>" . " " . "<input type=submit name=delete value=delete>"."</td>";
        echo "<td>" . "<input type=hidden name=hidden value=" . $row->id ."> </td>";
        echo "</tr>";
        echo "</form>";
        }
        echo "</table>";
        mysqli_close($db);

        ?>
        <br>

        <input type=button type=button onClick="location.href='/'" value='Zur Startseite'>
    </div>
  </body>
</html>



