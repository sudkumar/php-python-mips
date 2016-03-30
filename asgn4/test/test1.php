<?php

    var $y = 10;

    if($y == 0){
        $y = 3;
        $y += 4;
    }

    switch ($y) {
        case 1 :
            $y = 1;
            break;

        default:
            $y = 2;
            break;
    }

    while($y > 0){
        $y -= 1;
        while($y > 10){
            $y += 1;
            if($y == 0){
                $y = 1;
                continue;
            }
            $y = 10;
        }
        $y = 2;
    }

    $y = 11;
 ?>
