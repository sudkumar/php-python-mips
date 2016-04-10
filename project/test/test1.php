<?php

    // var $y;
    // var $z;
    $a = 30;
    $b = 10;
    $c = $a > 25 ? $a - 10 : $b + 5;
    
    function sum($a,$b){
        $c = $a + 1;
        return $a;
        $c = $a + $b;
        return $c;
    }
    $c = sum($a,$b);
    echo $c;
 ?>
