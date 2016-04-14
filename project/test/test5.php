<?php
	$y = 12;
    while($y > 0){
        $y -= 2;
        while($y > 10){
            $y += 1;
            if($y == 0){
                $y = 1;
                continue;
            }else{
                $y = -1;
                break;
            } 
        }
        continue;
        $y = 2;
    }
    echo $y;
?>