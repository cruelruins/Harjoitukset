<!-- KERTOLASKU -->
<form method="post">
    Valitse kerroin: <input type="number" name="kerroin" value="<?= htmlspecialchars($_POST['kerroin'] ?? 5) ?>">
    <button type="submit" name="toiminto" value="kerro">Laske</button>
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && ($_POST['toiminto'] ?? '') === 'kerro') {
    $kerroin = (int)$_POST['kerroin'];
    $luku = 0;

    while (true) {
        $summa = $kerroin * $luku;
        if ($summa >= 100) {
            break; // Lopetetaan ennen tulostusta, jos 100 täyttyy tai ylittyy
        }
        echo "$kerroin * $luku = $summa <br>";
        $luku++;
    }
}
?>

<!-- JAKOLASKU -->
<form method="post">
    Valitse Jako: <input type="number" name="Jako" value="<?= htmlspecialchars($_POST['Jako'] ?? 5) ?>">
    <button type="submit" name="toiminto" value="jaat">Laske</button>
</form>

<?php
if ($_SERVER["REQUEST_METHOD"] == "POST" && ($_POST['toiminto'] ?? '') === 'jaat') {
    $jako = (int)$_POST['Jako']; // Huomioitu iso J-kirjain
    
    // Aloitetaan luvusta 1, jotta vältetään nollalla jakaminen
    $luku = 1; 

    // Huom: Jos $jako on esim. 5, $summa (5/1 = 5) on aina alle 100.
    // Silmukka loppuu heti, kun jaettava tulos laskee alle 100:n tai luku kasvaa liikaa.
    while ($luku <= 100) { 
        $summa = $jako / $luku;
        echo "$jako / $luku = " . round($summa, 2) . "<br>";
        $luku++;
    }
}
?>