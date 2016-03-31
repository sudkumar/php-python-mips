<?php

    var $y = 10;
    var $z = 1;
    $y = $y > 0 ? $y + 1 : $z + 2;
    if($y == 0){
        $y = 3;
        $y += 4;
    }elseif($y != 0){
        $y = 1;
        $y = 14;
    }

    $y = 10;

    switch ($y) {
        case 1 :
            $y = 1;
            break;

        default:
            $y = 2;
            break;
    }

    $y= -1;

    while($y > 0){
        $y -= 1;
        while($y > 10){
            $y += 1;
            if($y == 0){
                $y = 1;
                continue;
            }else{
                $y = -1;
                break;
            }
            $y = 10;
        }
        $y = 10;
        continue;
        $y = 2;
    }

    $y = 11;
 ?>
