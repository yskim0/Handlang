function regist(){
    $.ajax({
      url: '/getlabel',
      method: 'GET'
    }).done(function(r){
      // console.log(r);
      $('#label').text(r)
      console.log("ajax-success")
    }).fail(function(){
      console.log("ajax fail")
    });

}

function erase(){
  $.ajax({
    url: '/eraselabel',
    method: 'GET'
  }).done(function(r){
    // console.log(r);
    $('#label').text(r)
    console.log("ajax-success")
  }).fail(function(){
    console.log("ajax fail")
  });

}


// 키보드 엔터키 눌렀을 때 새로운 label 호출
function keyPress(e) {
if (e.keyCode == 13) {
  regist();
  return false;
}
}

//backspace : result 한글자 지움
function keyDown(e) {
if(e.keyCode == 8){
  erase();
  return false;
}

}
