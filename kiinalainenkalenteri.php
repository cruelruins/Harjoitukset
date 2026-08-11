<form method="POST">
<h3>Kiinalainen Kalenteri</h3><br><br>
Kirjoita syntymävuotesi<br>
<input type="text" name="vuosi" size="4"><br>
<input type="submit" value="Testaa">
</form>

<?php

if (isset($_POST['vuosi'])) {

    $vuosi = $_POST['vuosi'];

    $elain = ($vuosi - 4) % 12;

    if ($elain == 0)
        echo "Olet syntynyt Rotan vuonna";

    elseif ($elain == 1)
        echo "Olet syntynyt Härän vuonna";

    elseif ($elain == 2)
        echo "Olet syntynyt Tiikerin vuonna";

    elseif ($elain == 3)
        echo "Olet syntynyt Jäniksen vuonna";

    elseif ($elain == 4)
        echo "Olet syntynyt Lohikäärmeen vuonna";

    elseif ($elain == 5)
        echo "Olet syntynyt Käärmeen vuonna";

    elseif ($elain == 6)
        echo "Olet syntynyt Hevosen vuonna";

    elseif ($elain == 7)
        echo "Olet syntynyt Vuohen vuonna";

    elseif ($elain == 8)
        echo "Olet syntynyt Apinan vuonna";

    elseif ($elain == 9)
        echo "Olet syntynyt Kukon vuonna";

    elseif ($elain == 10)
        echo "Olet syntynyt Koiran vuonna";

    elseif ($elain == 11)
        echo "Olet syntynyt Sian vuonna";
}
?>