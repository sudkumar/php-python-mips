<?php
$a = 10;
$n = 5;
function power($a, $n)
{
    if ($n == 0){
    	return 1;
    }
    if ($n % 2 == 0) { 
        $m = power($a, $n/2);
        return $m * $m;
    }
    else{ 
        $x = power($a, $n-1);
    	return $a * $x; 
    }
    $x = 10;
    return;
}
$p = power($a, $n);
echo $p;
?>