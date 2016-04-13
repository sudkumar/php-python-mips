<?php

    // var $y;
    // var $z;
    $a = 4;
    $b = 10;
    if($a<$b){
    	$tmp = $a;
    	$a = $b;
    	$b = $tmp;
    }
    while($b!=0){
    	$tmp = $a % $b;
    	$a = $b;
    	$b = $tmp;
    }

 ?>
