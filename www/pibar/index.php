<?php
    include(".dbconnect.php"); #<-- Hier steht alles zur verbindung zur Datenbank
?>
<html>
<head>
    <meta charset="UTF-8">
    <link href="index-files/style.css" type="text/css" rel="stylesheet">
    <title>PiBar Webinterface</title>
    <link rel="shortcut icon" href="index-files/favicon.ico" type="image/x-icon">
    <link rel="icon" href="index-files/favicon.ico" type="image/x-icon">
</head>

<body>
    
    <div class="inhalt">
        
        <div class="header">
            <img src="logo/Raspi-PGB001.png" style="height: 150px;">
            <div class="ueberschrift-box">
                <p class="ueberschrift-header">PiBar Webinterface</p>
                <p class="menu">
                    <a href="#">Home</a>
                    <a href="Highscore.php">Highscores</a>
                    <a href="admin/pay.php">Bezahlen</a>
                    <a href="admin/users.php">Benutzer</a>
                    <a href="admin/product.php">Produkte</a>
                </p>
            </div>
        </div>
            
        <div class="spalte">
            
            <div class="weisser-kasten text-mitte">
                
                <?php
                    # Abfrage für Anzahl an Getränken (unbezahlt):
                    $abfrage = "SELECT COUNT( orders.id ) AS NumberOfOrders,orderDate FROM orders where DATE(orderDate) = CURDATE()";
                    $ergebnis = mysqli_query($db, $abfrage);
                    $ergebnis= mysqli_fetch_object($ergebnis);
                    $aktuelle_drinks = $ergebnis->NumberOfOrders;

                    #Abfrage Wann wurde das letzte getränk getrunken:
                    $abfrage = "SELECT orderDate FROM orders where DATE(orderDate) = CURDATE() ORDER by orderDate desc limit 1";
                    $ergebnis = mysqli_query($db, $abfrage);
                    $ergebnis= mysqli_fetch_object($ergebnis);
                    $Zeitstempel = $ergebnis->orderDate;
                ?>
                
                <p class="tabellen-ueberschrift">Heute wurden</p>
                <p class="anzahl-getraenke"><?php echo $aktuelle_drinks ?></p>
                <p class="tabellen-ueberschrift">Getränke getrunken. Das letzte um:</p>
                <p class="uhrzeit-letztes-getraenk"><?php echo $Zeitstempel ?></p>
                
            </div>
            <div class="weisser-kasten">

                <p class="tabellen-ueberschrift">Wer hatte wie viele Drinks?</p>
                
                <table class="kleine-tabelle">
                    <?php
                        $abfrage = "SELECT CONCAT( customers.firstName, ' ', customers.lastName ) AS Name, COUNT( orders.id ) AS NumberOfOrders FROM orders LEFT JOIN customers ON orders.customerId = customers.id  WHERE DATE(orders.orderDate) = CURDATE() GROUP BY firstName ORDER BY `NumberOfOrders` DESC ";
                        $ergebnis = mysqli_query($db, $abfrage);
                        while($row = mysqli_fetch_object($ergebnis))
                        {
                          echo "<tr>";
                          echo "<td>" . $row->Name . "</td>";
                          echo "<td>" . $row->NumberOfOrders . "</td>";
                          echo "</tr>";
                        }
                    ?>
                </table>                

            </div>
            
        </div>
        
        <div class="spalte">
            
            <div class="weisser-kasten">
                <p class="tabellen-ueberschrift">Beliebte Getränke</p>

                <table class="kleine-tabelle">
                    
                    <?php
                        $abfrage = "SELECT products.name AS Name, COUNT( orders.id ) AS NumberOfOrders FROM orders LEFT JOIN products ON products.ean = orders.productId  GROUP BY Name ORDER BY `NumberOfOrders` DESC LIMIT 0,5";
                        $ergebnis = mysqli_query($db, $abfrage);
                        while($row = mysqli_fetch_object($ergebnis))
                        {
                          echo "<tr>";
                          echo "<td>" . $row->Name . "</td>";
                          echo "<td>" . $row->NumberOfOrders . "</td>";
                          echo "</tr>";
                        }
                    ?>
                </table>
            </div>
            <div class="weisser-kasten">
                <p class="tabellen-ueberschrift">
                    Wer hat offene Rechnungen auf der Karte?<br><center>(Nur Rechnungskarten)</center>
                </p>

                <table class="kleine-tabelle">
                    <?php
                        $abfrage = "SELECT CONCAT(c.firstName,' ', c.lastName ) AS 'Name', SUM( p.price ) AS 'Money' FROM customers c LEFT JOIN orders o ON o.customerId = c.id LEFT JOIN products p ON p.ean = o.productId WHERE o.isPaid =0 GROUP BY c.id ORDER BY Money DESC";
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
            
        </div>

        
    </div>

</body>
</html>
