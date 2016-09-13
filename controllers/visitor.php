<?php
	require_once('../bootstrap.inc.php');
	
	global $ndm;
	
	
	if($_GET['action'] != NULL)
    switch($_GET['action']) {
      case 'get':
        echo($ndm->getVisitorCount());
        break;
      case 'set':
        $ndm->addOneVisitor();
        break;
      case 'del':
        $ndm->removeOneVisitor();
        break;
      case 'getTotal':
        echo $ndm->getTotalCount();
        break;
      case 'getStats':
        echo $ndm->getJSONStats();
	break;
      case 'getCounters':
	echo $ndm->getCounters();
	break;
      default:
        echo('error');
        break;
      }
?>
