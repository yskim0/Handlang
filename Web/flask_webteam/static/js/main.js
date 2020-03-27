var timer;
var alphabet = $("#topic").text();
var correct = 0;
var total_correct = 0;

$(document).ready(function()  {
	// 라벨 측정 시작
	$(document).keypress(function(event){  // keyup 이벤트 처리 enter, backspace
		var keycode = (event.keyCode ? event.keyCode : event.which);
		if(keycode === 13) {
			console.log('엔터!');
			timer = setInterval(function(){
				ajax_prediction();
			}, 1000);
			// setInterval(ajax_prediction(), 1000);
			$("#predict_status").text("🔆 예측중... 🔆");
		}

	});


});

function en(){
	console.log('en!');
    $.ajax({
      url: '/en',
      type: 'get', 
      data: {
		"lang_code": "en"
	},
	  dataType: 'JSON',
	  success:function(){
		console.log('success!');
	}
    });

}
function ko(){
	console.log('ko!');
    $.ajax({
      url: '/ko',
      type: 'get', 
      data: {
		"lang_code": "ko"
	},
	  dataType: 'JSON',
	  success:function(){
		console.log('success!');
	}
    });

}
function ajax_prediction(){
	console.log('ajax!');
    $.ajax({
      url: '/return_label',
      type: 'POST', 
      data: {
      	target: alphabet
      },
      dataType: 'JSON',
      success: function(result){
      	console.log(result);
      	$("#predict-in").text(result.info + result.label);
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
		$("#check_table_"+total_correct).attr("src", "../static/img/smile.png");
		clearInterval(timer);
		$("#predict_status").text("✅ 연습완료! 예측을 중지합니다. ✅");    //js도 언어 바꾸기 1. jinja 내부에 넣기 or 2. session에서 가져와서 하는 방법
	}
	else $("#check_table_"+total_correct).attr("src", "../static/img/smile.png");
}

$("#btn_previous").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );

$("#btn_next").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );

$("#btn_practice_asl").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );


$("#btn_previous").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );

$("#btn_next").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );

$("#btn_practice_asl").click( function() {
	if(timer === true) {
		clearInterval(timer);
	}
} );


// var total_q=10;
// var q_num=0;

$(document).ready(function(){
	var q_num=0;
	var total_q=10;

	$("#next").click(function(){
	  $("#before").show();

	  $("#"+q_num).hide();
	  q_num+=1;
	  if(q_num==total_q-1){
		$('#next').hide();
		$('#submit').show();
	  }
	  $("#"+q_num).show();
	  
	});


	$("#before").click(function(){
	  $("#submit").hide();
	  $("#next").show();
	  $("#"+q_num).hide();
	  q_num=q_num-1;
	  if(q_num==0){
		$('#before').hide();
	  }
	  $("#"+q_num).show()
	  



	});

});
