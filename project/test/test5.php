<?php
	$y = 10;
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
    $y = 10;
?>