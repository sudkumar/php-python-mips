<?php

// FOR EACH

$arr = array("one", "two", "three");
reset($arr);
while ($value = $arr) {
    echo "Value: $value<br />\n";
}

foreach ($arr as $value) {
    echo "Value: $value<br />\n";
}

$arr = array("one", "two", "three");
reset($arr);
while ($key = $arr) {
    echo "Key: $key; Value: $value<br />\n";
}

foreach ($arr as $key => $value) {
    echo "Key: $key; Value: $value<br />\n";
}

?>