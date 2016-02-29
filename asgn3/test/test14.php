<?php
    function ourFunction($x)
    {
          echo $x . ".<br />";

for ($x = 0; $x <= 10; $x++) {
    echo "The number is: $x <br>";
} 
    }

    $y = "black";
    echo "My car color is ";
    ourFunction("white");

    echo "My car color is ";
    ourFunction ("$y");

    $fruits[0] = "pineapple";
    $fruits[1] = "pomegranate";
    $fruits[2] = "tangerine";
    print_r($fruits);


     function addValues($x,$y)
     {
          $total=$x+$y;
          return $total;
     }

     echo "2 + 2 = " . addValues(2,2);

?>


