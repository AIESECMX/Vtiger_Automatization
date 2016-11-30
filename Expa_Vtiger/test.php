<?php

if ( ini_get( "suhosin.get.max_value_length" ) ) { 
	echo 'si esta';
   // yes, suhosin is active ...
   // do something meaningful with the value of ini_get( "suhosin.get.max_value_length" )
 }else{
 	echo 'no esta';
 }


 ?>