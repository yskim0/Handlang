
$(document).ready(function()  {

	$(document).keyup(function(event){  // keyup 이벤트 처리 enter, backspace
	  var keycode = (event.keyCode ? event.keyCode : event.which);
	  if(keycode == '13') regist();  
	  if(keycode == '8') erase();
	});

	$("#add").click(function() {
	  regist();
	});

	$("#erase").click(function() {
	  erase();
	});


	function regist() {

	  $.ajax({
	    url: "/getlabel",
	    method: "GET"
	  }).done(function(r) {
	    $('#label').empty();
	    var result = r.split('2020HANDLANG');

	    result.reverse();

	    result = get_unique(result);

	    for (var i in result) {
	      $('#label').append( '<input type="checkbox" name="result_check" value="label'+i+'">' + result[i] + '</input><br>');
	    }

	    console.log("ajax-getLabel-success");

	  }).fail(function() {
	    console.log("ajax-getLabel-fail");
	  });

	}

	function erase()  {

	  $.ajax({
	    url: "/eraselabel",
	    method: "GET"
	  }).done(function(r) {
	    $('#label').empty();
	    $('#label').append( '<p> ===초기화=== </p>');
	    console.log("ajax-erase-success");
	  }).fail(function() {
	    console.log("ajax-erase-fail");
	  });
	}

	//중복되지 않게 나오도록 한번씩만 출력
	function get_unique(array) {
	  var unique_array = [];
	  $.each(array, function(index, element)  {     // 배열의 원소수만큼 반복
	    if($.inArray(element, unique_array) == -1)  {   // unique_array 에서 값을 찾는다. 값이 없을경우 (-1)
	      if(element != "") {
	        unique_array.push(element); // unique_array  배열에 값을 넣는다.
	      }
	      
	    }
	  });

	  return unique_array;
	}

});
