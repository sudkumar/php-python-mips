<?php
// int main(int na, char* argv[])
// {
//     int wflg = 0, tflg = 0;
//     int dflg = 0;
//     char c;
//     switch(c)
//     {
//         case 'w':
//         case 'W':
//             wflg = 1;
//             break;
//         case 't':
//         case 'T':
//             tflg = 1;
//             break;
//         case 'd':
//             dflg = 1;
//             break;
//     }
//     return 0;
// }

$wflag = 0;
$tflg = 0;
$dflg = 0;
$c;
switch ($c) {
	case 'w': 
	case 'W':
		$wflg = 1;		
		break;
	case 't':
	case 'T':
		$tflg=1;		
		break;
	case 'd':
		$dflg = 1;
		break;
}
return 0;

?>