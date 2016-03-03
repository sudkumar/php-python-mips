<?php

// For loop

/* example 1 */

for ($i = 1; $i <= 10; $i++) {
    echo $i;
}

/* example 2 */

for ($i = 1; ; $i++) {
    if ($i > 10) {
        break;
    }
    echo $i;
}

/* example 3 */

$i = 1;
for (; ; ) {
    if ($i > 10) {
        break;
    }
    echo $i;
    $i++;
}

/* example 4 */
for ($i = 1, $j = 0; $i <= 10; $j += $i, print $i, $i++);

// nested for loop

for ($i = 1; ; $i++) {
    if ($i > 10) {
        break;
    }
    for ($i = 1; ; $i++) {
	    if ($i > 10) {
	        break;
	    }
	    for ($i = 1; ; $i++) {
		    if ($i > 10) {
		        break;
		    }
		    echo $i;
		}
	    echo $i;
	}
    echo $i;
}
?>