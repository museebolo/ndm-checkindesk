<?php

   $CONFIG['DB_USER']   = '';
   $CONFIG['DB_PWD']    = '';
   $CONFIG['DB_PORT']   = '27017';
   $CONFIG['DB_HOST']   = 'localhost';
   $CONFIG['DB_NAME']   = "Ndm";
   $CONFIG['COL_NAME']  = "Ndm15";  
   
   $CONFIG['PATH']['ROOT']          = getcwd().'/';
   $CONFIG['PATH']['LIB']           = $CONFIG['PATH']['ROOT'].'lib/';
   $CONFIG['PATH']['CONTROLLERS']   = $CONFIG['PATH']['ROOT'].'controllers/';
   $CONFIG['PATH']['MODELS']        = $CONFIG['PATH']['ROOT'].'models/';
   $CONFIG['PATH']['JQUERY']        = $CONFIG['PATH']['LIB'].'flot/jquery.js';
   $CONFIG['PATH']['FLOT']          = $CONFIG['PATH']['LIB'].'flot/jquery.flot.js';
   
   $CONFIG['INFOS']['DATE'] = '2015-09-26';
   
   $PAGE['TITLE']       = 'Bolo Museum - '.$CONFIG['COL_NAME'].' - Check-In Desk';
   $PAGE['HEADER_TITLE'] = 'NDM 2015 CheckIn Desk';
   $PAGE['FOOTER']      = 'Copyright aBCM 2015 - Guillaume Camenzind';
   $PAGE['TIMER']       = '2000';
?>
