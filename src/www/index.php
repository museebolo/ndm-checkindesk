<?php

  require_once('bootstrap.inc.php');

  global $ndm,$PAGE, $CONFIG;  
?>

<html>
   <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title><? echo($PAGE['TITLE']); ?></title>
    <link rel='stylesheet' type='text/css' href='css/style.css' />
	  <script type="text/javascript" src="lib/jquery.js"></script>	  
   </head>
   <body>
    <div id="content">
      <div id="header">
        <h1><? echo($PAGE['HEADER_TITLE']); ?></h1>
      </div>
      <div id="ticketsdiv">
        <h2>Tickets sold</h2>
        <input class="button" type="button" value="-" onclick="removeTicket();"/>
        <input class="button" type="button" value="+" onclick="addTicket();" />
      </div>
      <div id="visitorsdiv">
        <h2>Visitors with tickets</h2>
        <input class="button" type="button" value="-" onclick="removeVisitor();"/>
        <input class="button" type="button" value="+" onclick="addVisitor();" />
      </div>    
      <div id="vcounter">
        <h3>Visitors counter: <span id="vcount">#</span></h3>
        <p>(with + without tickets)</p>        
      </div>
      <div id="tcounter">
        <h3>Ticket sold: <span id="tcount">#</span></h3>
      </div>
      <div id="stats" onclick="$(this).find('ul').toggle()">
        <h3>Stats</h3>
        <ul>
          <li>1st Hour: <span id="hour1"></span></li>
          <li>2nd Hour: <span id="hour2"></span></li>
          <li>3rd Hour: <span id="hour3"></span></li>
          <li>4th Hour: <span id="hour4"></span></li>
          <li>5th Hour: <span id="hour5"></span></li>
          <li>6th Hour: <span id="hour6"></span></li>
          <li>7th Hour: <span id="hour7"></span></li>
          <li>8th Hour: <span id="hour8"></span></li>
          <li>9th Hour: <span id="hour9"></span></li>
          <li>10th Hour: <span id="hour10"></span></li>
        </ul>
      </div>
      <div id="footer">
        <small><? echo $PAGE['FOOTER'];?><span style="color:black;" href="#" onclick="reset();">reset</span></small>
      </div>
    </div>
  <script>  
    function majCounter(){
			$.ajax({
				url: "controllers/visitor.php?action=getTotal"
			}).done(function(data){
				$('#vcount').html(data);
			});
		}
    
		function timer() {
			setTimeout(function(){
				majCounters();
			        getStats();
				setTimeout(timer, <? echo $PAGE['TIMER'];?>);
			}, <? echo $PAGE['TIMER'];?>);
		}

		function addVisitor() {
			$.ajax({
				url: "controllers/visitor.php?action=set"
			});

			$('#vcount').html(parseInt($('#vcount').html())+1);
		}

		function addTicket() {
			$.ajax({
				url: "controllers/ticket.php?action=set"
			});

			$('#vcount').html(parseInt($('#vcount').html())+1);
			$('#tcount').html(parseInt($('#tcount').html())+1);
		}

		function removeVisitor() {
			$.ajax({
				url: "controllers/visitor.php?action=del"
			});

			$('#vcount').html(parseInt($('#vcount').html())-1);
		}

		function removeTicket() {
			$.ajax({
				url: "controllers/ticket.php?action=del"
			});

			$('#vcount').html(parseInt($('#vcount').html())-1);
		}
    
    function reset() {
      if ( confirm("Reset app counters?") )
        $.ajax({				
        	url: "controllers/ticket.php?action=resetCounters"
        });
    }
    
    function majCounters() {
	$.ajax({
  	  url: "controllers/visitor.php?action=getCounters",
	  dataType: "json",
	}).done(function(data){
	  console.log(data);
  	  $('#vcount').html(data[0]);
	  $('#tcount').html(data[1]);
	});
    }
    function getStats() {
      $.ajax({				
	url: "controllers/visitor.php?action=getStats"
      }).done(function(data){
        //console.log(data);
	var datas=eval(data);
        var i = 0;
        $('#stats ul li').each(function(){
	  
          $(this).find('span').html(datas[i++]);
        });
      });
    }

		$(document).ready(function(){
			timer();     
      			$('#stats').find('ul').toggle()
		});
	</script>
  </body>
</html>
