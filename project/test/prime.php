<?php
$n = 10; 
$count;
$c;
  
if ( $n >= 1 )
{
   echo "2   " ;
}

for ( $count = 2,$i=3 ; $count <= $n ;  )
{
   for ( $c = 2 ; $c <= $i - 1 ; $c++ )
   {
      if ( $i%$c == 0 ){
         break;
      }
   }
   if ( $c == $i )
   {
      echo $i;
      echo "    ";
      $count++;
   }
   $i++;
}
echo "\n\n";
?>