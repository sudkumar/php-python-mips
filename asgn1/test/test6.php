<?php
class Foo { 
    public $aMemberVar = 'aMemberVar Member Variable'; 
    public $aFuncName = 'aMemberFunc'; 
    
    
    function aMemberFunc() { 
        print 'Inside `aMemberFunc()`'; 
    } 
} 
$foo = new Foo; 
$element = 'aMemberVar'; 
print $foo->$element; // prints "aMemberVar Member Variable" 

?>