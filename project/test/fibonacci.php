<?php

$n = 7;
function Fibonacci($n)
{
   if ( $n == 0 ){
      return 0;
   }
   else if ( $n == 1 ){
      return 1;
   }
   else{
      // $n = $n-1;
      // $a = Fibonacci($n);
      // $n = $n-1;
      // $b = Fibonacci($n);
      return Fibonacci($n-1) + Fibonacci($n-2);
   }
} 
$c = Fibonacci($n);
echo $c;
 
?>