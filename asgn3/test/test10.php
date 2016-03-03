<?php
// Mix of all
function addFunction($num1, $num2) {
    $sum = $num1 + $num2;
    switch ($i) {
	    case 0:
	        echo "i equals 0";
	        break;
	    case 1:
	        echo "i equals 1";
	        break;
	    case 2:
	        echo "i equals 2";
	        break;
	    default:
	       echo "i is not equal to 0, 1 or 2";
	}
	while ($key = $arr) {
    	echo "Key: $key; Value: $value<br />\n";
	}

	foreach ($arr as $key => $value) {
	    echo "Key: $key; Value: $value<br />\n";
	}

	if($a > $b):
	    echo $a." is greater than ".$b;
	elseif($a == $b): // Note the combination of the words.
	    echo $a." equals ".$b;
	else:
	    echo $a." is neither greater than or equal to ".$b;
	endif;

    return $sum;
 }
 $return_value = addFunction(10, 20);
 
 echo "Returned value from the function : $return_value";
?>
