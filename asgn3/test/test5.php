<?php
// DO while

do {
    if ($i < 5) {
        echo "i is not big enough";
        break;
    }

    do {
	    if ($i < 5) {
	        echo "i is not big enough";
	        break;
	    }
	    $i *= $factor;
	    if ($i < $minimum_limit) {
	        break;
	    }
	   echo "i is ok";

	    /* process i */

	} while (0);

    $i *= $factor;
    if ($i < $minimum_limit) {
        break;
    }
   echo "i is ok";

    /* process i */

} while (0);

?>
