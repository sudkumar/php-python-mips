<?php
//  int main(void){
//     int i = 0,a[]={1,2,3};
//     if (i<=3)
//         a[i]++;
//     if (i>=2)
//         a[i]--;
//     else 
//         a[i] = 1;
// } 
$i=0;
$a =5;
// $a=array(1,2,3);
if($i<=3){
	$c = ++$a; // ++ pre-incr
}
if($i>=2){
	$c = $a++;
}
else{
	--$a;
}
?>