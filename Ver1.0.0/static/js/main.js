var timer;
var alphabet = $("#topic").text();
var number = $("#topic").text();

var correct = 0;
var total_correct = 0;

$(document).ready(function()  {
	// 라벨 측정 시작
	$(document).keypress(function(event){  // keyup 이벤트 처리 enter, backspace
		var keycode = (event.keyCode ? event.keyCode : event.which);
		if(keycode === 13) {
			console.log('엔터!');

			timer = setInterval(function(){
				if($('#category').hasClass('alphabet')) {
					// console.log(windowLoc)

					ajax_prediction(function (lang_code) {
						if (lang_code == "en") {
							$("#predict_status").text("🔆 Predicting... 🔆");

						} else if (lang_code == "ko") {
							$("#predict_status").text("🔆 예측중... 🔆");

						}

					});
				}
				else if($('#category').hasClass('number')){

					ajax_prediction2(function (lang_code) {
						if (lang_code == "en") {
							$("#predict_status").text("🔆 Predicting... 🔆");

						} else if (lang_code == "ko") {
							$("#predict_status").text("🔆 예측중... 🔆");

						}

					});
				}

			}, 1000);

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
function ajax_prediction(save_langcode){
	console.log('ajax!');
    $.ajax({
      url: '/return_label',
      type: 'POST', 
      data: {
      	target: alphabet
      },
      dataType: 'JSON',
      success: function(result){
		save_langcode(result.lang_code);
      	console.log(result);
		  $("#predict-in").text(result.info + result.label);
      	if(result.status === 0) {
      		correct = 0;
      	}
      	else	{
      		correct++;
      		console.log("플러스");
      		if(correct === 3)	{
      			check_correct(result.lang_code);
      			correct = 0;
      		}
		}
 
	  
	},
      error: function(xtr, status, error){
      	console.log(xtr+":"+status+":"+error);
      }
    });

}

function ajax_prediction2(save_langcode){
	console.log('ajax!');
    $.ajax({
      url: '/return_label2',
      type: 'POST', 
      data: {
      	target: number
      },
      dataType: 'JSON',
      success: function(result){
		save_langcode(result.lang_code);
      	console.log(result);
		  $("#predict-in").text(result.info + result.label);
      	if(result.status === 0) {
      		correct = 0;
      	}
      	else	{
      		correct++;
      		console.log("플러스");
      		if(correct === 3)	{
      			check_correct(result.lang_code);
      			correct = 0;
      		}
		}
 
	  
	},
      error: function(xtr, status, error){
      	console.log(xtr+":"+status+":"+error);
      }
    });

}

function check_correct(lang_code)	{
	total_correct++;
	
	if (total_correct === 8)	{
		$("#check_table_"+total_correct).attr("src", "../static/img/smile.png");
		clearInterval(timer);
		if(lang_code=="en"){
			$("#predict_status").text("✅ done ✅");    //js도 언어 바꾸기 1. jinja 내부에 넣기 or 2. session에서 가져와서 하는 방법

		}
		else if(lang_code=="ko"){
			$("#predict_status").text("✅ 연습완료! 예측을 중지합니다. ✅");    //js도 언어 바꾸기 1. jinja 내부에 넣기 or 2. session에서 가져와서 하는 방법
		}
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
	var total_q=5;
	//$("#"+q_num).show();

	$("#next").click(function(){
	  $("#before").show();

	  $("#"+q_num).hide();
	  
	  q_num+=1;
	  console.log(q_num);
	//   location.href = "#"+q_num;
	  

	  if(q_num==total_q-1){
		$('#next').hide();
		$('#submit').show();
	  }
	   $("#"+q_num).toggle();
	

	});


	$("#before").click(function(){

	  $("#submit").hide();
	  $("#next").show();
	 $("#"+q_num).hide();
	  q_num=q_num-1;
	  console.log(q_num);

	  if(q_num==0){
		$('#before').hide();
	  }
	  $("#"+q_num).toggle()
	
	// location.href = "#"+q_num;




	});

});

