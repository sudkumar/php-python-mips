<?php
// comparison operators: == === !=    !==  > < >= <=
$a = 5;
$b = 9;
$c = 4.67;
$d = 70E-1;
if($a==$b)
	print('a and b are same');
else if($a===$b)
	print('a and b are identical');
else if($a!=$b)
	print('a and b are not same');
else if($a!==$b)
	print('a and b are not identical');
else if($a>$b)
	print('a is greater than b');
else if($a < $b)
	print('b is greater than a');
else if($a>=$b)
	print('a is greater equal than b');
else if($a <= $b)
	print('b is greater equal than a');

?>