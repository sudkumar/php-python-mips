<?php

    // var $y;
    // var $z;
    $c = 10 + 20;
    $d = $c + 12342340;
    $a = 112;
    $b = $a + 1;
    $a = $a + 1; 
    $a = $b + 1;
    $c = $a > 25 ? $a - 10 : $b + 5;
    if($c == 3 || $c == 9){
        $c = 1;
    }
    else if($c > 0  ){
        $c = 1;
    }
    while($c > 0){
        --$c;
    }
    for($c=0;$c<10;$c++){
        $c += 1;
    }
    $d = 10;
    $e = $d + 100;
    $f = $d;
    function sum($c, $e){
        return $c + $e;
    }
    function foo($d){
        if($d == 0){
            return 0;
        }
        else{
            $d--;
            return  $d + foo($d); 
        }
    }
    $d = 10;
    $e = foo($d);
    echo $e;
    $f = 10;
    $f = sum($f, $e);
    echo $f;
    exit;
 ?>
