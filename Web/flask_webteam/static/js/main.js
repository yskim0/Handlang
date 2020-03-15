var timer;
var alphabet = $("#topic").text();
var correct = 0;
var total_correct = 0;

$(document).ready(function()  {
	// 라벨 측정 시작

	$(document).keyup(function(event){  // keyup 이벤트 처리 enter, backspace
		var keycode = (event.keyCode ? event.keyCode : event.which);
		if(keycode == '13') {
			timer = setInterval(function(){
				ajax_prediction();
			}, 1000);
			// setInterval(ajax_prediction(), 1000);
		}
	});


});

function ajax_prediction(){
	console.log('ajax!')
    $.ajax({
      url: '/return_label',
      type: 'POST', 
      data: {
      	target: alphabet
      },
      dataType: 'JSON',
      success: function(result){
      	console.log(result);
      	$('#predict-in').text(result.info + result.label)
      	if(result.status === 0) {
      		correct = 0;
      	}
      	else	{
      		correct++;
      		console.log("플러스");
      		if(correct === 3)	{
      			check_correct();
      			correct = 0;
      		}
      	}
      },
      error: function(xtr, status, error){
      	console.log(xtr+":"+status+":"+error);
      }
    });

}

function check_correct()	{
	total_correct++;
	
	if (total_correct === 8)	{
		$("#check_table_"+total_correct).text("✅");
		clearInterval(timer);
		alert("다음 문자 공부");
	}
	else $("#check_table_"+total_correct).text("✅");
}
