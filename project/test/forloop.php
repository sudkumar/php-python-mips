<?php
$y = 1; 
$a = $y;
for($y = 0, $z = 2; $y < 10 && $z < 10; $y += 1){
     $a += $z ;
     if($a==17){
        break;        
     }
}
echo $a;
$y = 10;
?>