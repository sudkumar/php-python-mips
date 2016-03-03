<?php 
// While loop

// Type 1
$i=1;
while($i<=5)
{
    $j=1;
    while($j<=$i)
    {
      echo"*&nbsp&nbsp";
      $j++;
      if ($a == 1){
        continue;
      }      
      else{
        break;
      }
    }
    echo"<br>";
    $i++;
    exit;
}

// Type 2
$i=1;
while($i<=5):

    $j=1;
    while($j<=$i):
      echo"*&nbsp&nbsp";
      $j++;      
    endwhile;
    
    echo"<br>";
    $i++;
endwhile;

?>