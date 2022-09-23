<?php
//The $_REQUEST["n"] and $_REQUEST["c"] will serve as python arguments
$str = "sudo python /var/www/html/test.py   ".$_REQUEST['pos']." ".$_REQUEST['raf'];

exec($str);
