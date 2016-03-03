<?php
// IF ELSE, Nested IF ELSE

	if ($a > $b) {
	    echo "a is bigger than b";
	} elseif ($a == $b) {
	    echo "a is equal to b";
		if($a > $b):
		    echo $a." is greater than ".$b;
		elseif($a == $b): // Note the combination of the words.
		    echo $a." equals ".$b;
			if ($a > $b) {
			    echo "a is bigger than b";
			} elseif ($a == $b) {
			    echo "a is equal to b";
				if($a > $b):
				    echo $a." is greater than ".$b;
				elseif($a == $b): // Note the combination of the words.
				    echo $a." equals ".$b;
				else:
				    echo $a." is neither greater than or equal to ".$b;
				endif;
			} else {
			    echo "a is smaller than b";
			}
		else:
		    echo $a." is neither greater than or equal to ".$b;
		endif;
	} else {
	    echo "a is smaller than b";
	}

	if($a > $b):
	    echo $a." is greater than ".$b;
	elseif($a == $b): // Note the combination of the words.
	    echo $a." equals ".$b;
	else:
	    echo $a." is neither greater than or equal to ".$b;
	endif;
?>
