<?php
$a = 5;
$n = 2;
function power($a, $n)
{
    if ($n == 0){
    	return 1;
    }
    if ($n % 2 == 0) {
    	$n = $n/2;
        $m = power($a, $n);
        return $m * $m;
    }
    else{
    	$n = $n-1;
        $x = power($a, $n);
    	return $a * $x; 
    }
}
$p = power($a, $n);
echo $p;
?>