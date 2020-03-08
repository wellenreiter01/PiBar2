<?php
require('fpdf.php');
include("../.dbconnect.php");
?>
<?php
if(isset($_POST['paynopdf'])){
$update = "UPDATE orders SET isPaid='1' WHERE customerId='$_POST[customer]'";
mysqli_query($db, $update);
echo"<br>done<br>";
}

if(isset($_POST['paypdf'])){
$image1 = "../images/logo_dpsg_franziskus.png";
$sql="SELECT p.name AS Product, p.price AS Price, COUNT( o.id ) AS Total, SUM( p.price ) AS 'Money' FROM customers c LEFT JOIN orders o ON o.customerId = c.id LEFT JOIN products p ON p.ean = o.productId WHERE c.id ='$_POST[customer]' AND isPaid=0 GROUP BY p.name";
$pdf = new FPDF();
$pdf->AliasNbPages();
$pdf->AddPage();
$pdf->SetFont('Arial', '', 10);
$pdf->Cell( 40, 40, $pdf->Image($image1, $pdf->GetX(), $pdf->GetY(), 33.78), 0, 0, 'L', false );
$pdf->Ln(5);
#$pdf->Cell(150, 10, $_POST[firstname].' '.$_POST[lastname], 0);
$pdf->SetFont('Arial', '', 9);
$pdf->Cell(160, 8, '', 0);
$pdf->Cell(10, 8, 'Datum: '.date('d-m-Y').'', 0);
$pdf->Ln(5);
$pdf->Line(20, 45, 210-20, 45);
$pdf->Ln(5);
$pdf->SetFont('Arial', 'B', 11);
$pdf->Cell(70, 8, '', 0);
$pdf->Cell(100, 8, 'Rechnung' .' von ' .$_POST[firstname].' '.$_POST[lastname], 0);
$pdf->Ln(23);
$pdf->SetFont('Arial', 'B', 8);
$pdf->Cell(15, 8, 'Item', 0);
$pdf->Cell(80, 8, 'Produkt', 0);
$pdf->Cell(40, 8, 'Einzel Preis ', 0);
$pdf->Cell(25, 8, 'Anzahl', 0);
$pdf->Cell(25, 8, 'EUR', 0);
$pdf->Ln(8);
$pdf->SetFont('Arial', '', 8);
$money =0.00;
$total =0;
$ergebnis = mysqli_query($db, $sql);
while($row = mysqli_fetch_object($ergebnis))
{
$item = $item+1;
$pdf->Cell(15, 8, $item, 0);
$pdf->Cell(80, 8,$row->Product, 0);
$pdf->Cell(40, 8,$row->Price, 0);
$pdf->Cell(25, 8,$row->Total, 0);
$pdf->Cell(25, 8,$row->Money, 0);
$pdf->Ln(8);
$money = $money + $row->Money;
$total = $total + $row->Total;
}
$pdf->Ln(8);
$pdf->Cell(108, 8, ' ', 0);
$pdf->Cell(25, 8, ' Summe: ', 0);
$pdf->Cell(25, 8, $total , 1);
$pdf->Cell(25, 8, number_format($money,2) .' ' .'Euro', 1);
$update = "UPDATE orders SET isPaid='1' WHERE customerId='$_POST[customer]'";
mysqli_query($db, $update);
$pdf->Output(date('d-m-y').'_'.$_POST[firstname].'_'.$_POST[lastname].'.pdf',D);
}
?>
<html>
<head>
<meta name="Tom Erber" content="PiBar Webinterface">
<meta name="Wellenreiter" content="PiBar2 Webinterface">
<link href="admin_style.css" type="text/css" rel="stylesheet">

<title>PiBar Webinterface</title>
</head>
<body>
<span><image class=logo src='/images/logo_dpsg_franziskus.png'> </span>
<div align=center>
    <h1 align>Welcome to the PiBar</h1>
     <p>
        <input type=button type=button onClick="location.href='/'" value='Zur Startseite'>
      </p>
    <?php
    $sql= "SELECT * FROM customers where  userCard like 'CREDIT%'";
    $ergebnis = mysqli_query($db, $sql);
    echo "<div class=full><table>
    <tr>
    <th align=center colspan=3> Benutzer:</th>
    <tr>
    <th>Vorname:</th>
    <th>Nachname:  </th>
    <th>Wie soll bezahlt werden?</th>
    </tr>";

    while($row = mysqli_fetch_object($ergebnis))
    {
    echo "<form action=pay.php method=post>";
    echo "<tr>";
    echo "<td align='center'>" . $row->firstName ."</td>";
    echo "<td align='center'>" . $row->lastName ."</td>";
    echo "<td align='center'>" . "<input type=submit name=paypdf value='pay with PDF?'"."> <input type=submit name=paynopdf value='pay without PDF?'". "> </td>";
    echo "<td>" . "<input type=hidden name=firstname value=" . $row->firstName ."> </td>";
    echo "<td>" . "<input type=hidden name=lastname value=" . $row->lastName ."> </td>";
    echo "<td>" . "<input type=hidden name=customer value=" . $row->id ."> </td>";
    echo "</tr>";
    echo "</form>";
    }
    echo "</table></div>";
    echo "<br>";


    mysqli_close($db);
    ?>
</div> 
</body>
</html>
