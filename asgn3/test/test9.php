<?php
// function
 function addFive($num) {
    $num += 5;
 }
 
 function addSix(&$num) {
    $num += 6;
 }
 
 $orignum = 10;
 addFive( $orignum );
 
 echo "Original Value is $orignum<br />";
 
 addSix( $orignum );
 echo "Original Value is $orignum<br />";

function addFunction($num1, $num2) {
    $sum = $num1 + $num2;
    return $sum;
 }
 $return_value = addFunction(10, 20);
 
 echo "Returned value from the function : $return_value";
?>

