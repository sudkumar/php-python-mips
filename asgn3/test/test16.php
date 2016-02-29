<?php
function factorial($number) { 


for ($x = 0; $x <= 10; $x++) {
    echo "The number is: $x <br>";
} 
    if ($number < 2) { 
        return 1; 
    } else { 
        return ($number * factorial($number-1)); 
    } 
}


         $array = array( 1, 2, 3, 4, 5);
         
         foreach( $array as $value ) {
            if( $value == 3 )continue;
            echo "Value is $value <br />";
         }

?>

