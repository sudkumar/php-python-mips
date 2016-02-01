<?
$a = 4;
$b = 7;
$c = $b | $a;
$d = ~($c ^( $b & $a)) ;
$e = ($c >> ($b << $a));
$result = ($a < $b ) ? $a :$b;

if($_GET["name"] || $_GET["age"])
	print_r('name or age is set');

$color = "red";
switch ($color) {
    case "red":
        echo "color is red!";
        break;
    case "blue":
        echo "color is blue!";
        break;
    default:
        echo "color is neither red nor blue!";
}

?>