<?php

/**
 * Class for db connection and methods
 *
 * @author Guillaume Camenzind <guillaume.camenzind@gmail.com>
 */
class Ndm {

  private $con = '';
  private $db = '';
  private $col = '';

  public function __construct() {
    global $CONFIG;

    // $this->con = new MongoClient('mongodb://'.$CONFIG['DB_USER'].':'.$CONFIG['DB_PWD'].'@'.$CONFIG['DB_HOST'].":".$CONFIG['DB_PORT']);

    $this->con = new MongoClient('mongodb://'.$CONFIG['DB_HOST'].":".$CONFIG['DB_PORT']);

    $this->db = $this->con->$CONFIG['DB_NAME'];
    $this->col = $this->db->$CONFIG['COL_NAME'];
    $this->initDbAttr();
  }

  public function addOneVisitor() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'visitors'),array('count'));

    $count = $obj["count"];
    $newdata = array('$set' => array("count" => $count+1, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'visitors'), $newdata);

    //log
    $obj = array("attr" => "visitors_log",
               "date" => new MongoDate(),
               "count" => $count+1,
               "action" => 'add',
                 );
    $this->col->insert($obj);
  }

  public function removeOneVisitor() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'visitors'),array('count'));
    $count = $obj["count"];

    $newdata = array('$set' => array("count" => $count-1, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'visitors'), $newdata);

    //log
    $obj = array("attr" => "visitors_log",
               "date" => new MongoDate(),
               "count" => $count-1,
               "action" => 'del',
                 );
    $this->col->insert($obj);
  }

  public function addOneTicket() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'tickets'),array('count'));
    $count = $obj["count"];

    $newdata = array('$set' => array("count" => $count+1, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'tickets'), $newdata);

    //log
    $obj = array("attr" => "tickets_log",
               "date" => new MongoDate(),
               "count" => $count+1,
               "action" => "add"
                 );
    $this->col->insert($obj);
  }

  public function removeOneTicket() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'tickets'),array('count'));
    $count = $obj["count"];

    $newdata = array('$set' => array("count" => $count-1, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'tickets'), $newdata);

    //log
    $obj = array("attr" => "tickets_log",
             "date" => new MongoDate(),
             "count" => $count-1,
             "action" => "del"
               );
    $this->col->insert($obj);
  }

  private function initDbAttr() {
    if($this->col->findOne(array("attr" => "visitors")) == NULL){
      $obj = array("attr" => "visitors",
                  "date" => new MongoDate(),
                  "count" => 0
                  );
      $this->col->insert($obj);
    }

    //log all actions
    if($this->col->findOne(array("attr" => "visitors_log")) == NULL){
      $obj = array("attr" => "visitors_log",
                  "date" => new MongoDate(),
                  "count" => 0
                 );
      $this->col->insert($obj);
    }

    if($this->col->findOne(array("attr" => "tickets")) == NULL){
      $obj = array("attr" => "tickets",
               "date" => new MongoDate(),
               "count" => 0
                 );
      $this->col->insert($obj);
    }

    //log all actions
    if($this->col->findOne(array("attr" => "tickets_log")) == NULL){
      $obj = array("attr" => "tickets_log",
               "date" => new MongoDate(),
               "count" => 0
                 );
      $this->col->insert($obj);
    }
  }

  public function getVisitorCount() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'visitors'),array('count'));
    $count = $obj["count"];

    return $count;
  }

  public function getTicketCount() {
    $count = -1;

    $obj = $this->col->findOne(array('attr'=>'tickets'),array('count'));
    $count = $obj["count"];

    return $count;
  }

  public function getHourlyCount($hour) {
    global $CONFIG;

    $start = new MongoDate(strtotime($CONFIG['INFOS']['DATE']." ".$hour.":00:00"));
    $end = new MongoDate(strtotime($CONFIG['INFOS']['DATE']." ".($hour+1).":00:00"));
    $cadd = $this->col->count(array('$or'=>array(array('attr'=>'visitors_log'),
                            array('attr'=>'tickets_log')), array("date" =>
                            array('$gt' => $start, '$lte' => $end, 'action' => 'add'))));
    $cdel = $this->col->count(array('$or'=>array(array('attr'=>'visitors_log'),
                            array('attr'=>'tickets_log')), array("date" =>
                            array('$gt' => $start, '$lte' => $end, 'action' => 'del'))));
    return $cadd-$cdel;
  }
  public function getJSONStats() {
    $res = array();
    for($i = 0; $i < 10;++$i)
      $res[] = $this->getHourlyCount(14+$i);

    return json_encode($res);
  }

  public function getCounters() {
    $res=array();
    $res[]=$this->getVisitorCount()+$this->getTicketCount();
    $res[]=$this->getTicketCount();
    return json_encode($res);
  }

  public function closeCon() {
    $this->con->close();
  }

  public function resetCounters() {
    $this->resetTicketCounter();
    $this->resetVisitorCounter();
  }
  public function resetTicketCounter() {
    $newdata = array('$set' => array("count" => 0, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'tickets'), $newdata);
  }
  public function resetVisitorCounter() {
    $newdata = array('$set' => array("count" => 0, "date" => new MongoDate()));

    $this->col->update(array('attr' => 'visitors'), $newdata);
  }
  public function getTotalCount() {
    return $this->getVisitorCount() + $this->getTicketCount();
  }
}
