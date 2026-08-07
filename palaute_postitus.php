<?php
foreach($_POST as $rivi => $arvo) {
	$sviesti .= $rivi.": ".$arvo."\n";
}
$mail = mail("maili@osoite.net", "viesti", $sviesti);
header("Location: ok.php");
?>