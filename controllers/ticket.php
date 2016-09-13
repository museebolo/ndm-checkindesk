<?php
	require_once('../bootstrap.inc.php');
	
	global $ndm;
	
	
	if($_GET['action'] != NULL)
    switch($_GET['action']) {
      case 'get':
        echo($ndm->getTicketCount());
        break;
      case 'set':
        $ndm->addOneTicket();
        break;
      case 'del':
        $ndm->removeOneTicket();
        break;	 
      case 'resetCounters':
        $ndm->resetCounters();
        break;
      default:
        echo('error');
        break;
      }