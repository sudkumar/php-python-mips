<?php
// errors
$c = 10 + 20;
$b = 30;
$d = 's';
if($c == $b && $c){
    $c = 1 + 'c';
}else if($c + 0 ){
        $c = 1;
    }
while($c = 3){
	--$c;
}
for($c > 0;$c=10&&$b>0;$c++){
	$c += 2;
}
$c = $d;

function sum(){
    global $f;
    $c = $d + 2;
    return $c;
} 
$f = sum();  

?>