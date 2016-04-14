<?php

    $a = 2016;
    $isLeap = 0;
    if ($a % 400 == 0):
        $isLeap = 1;
    elseif ($a % 100 == 0):
        $isLeap = 0;
    elseif($a % 4 == 0):
        $isLeap = 1;
    else:
        $isLeap = 0;
    endif;

    
    // if($isLeap == 0){
    //     echo "No..";
    // }else{
	   //      echo "Yes.";
    // }
    
    $c = $isLeap == 0 ? "No.." : "Yes.";
    echo $c;
    echo "\n\n";

 ?>
