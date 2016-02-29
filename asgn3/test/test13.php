<?php
function hello() {
    print "<h1>HELLO!</h1>";
    print "<p>Welcome to my web site</p>";
}

function printBreak($text) {

for ($x = 0; $x <= 10; $x++) {
    echo "The number is: $x <br>";
} 
    print "$text<br>";
}

function addNumbers($num1, $num2) {
     return $num1 + $num2;
}

hello();
printBreak("This is a line");
print addNumbers(3.75, 5.645);

?>
