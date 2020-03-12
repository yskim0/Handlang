function change2(){

    //1초마다 intervalLoad() 호출
    var interverID = setInterval("intervalLoad()", 1000);

    $.ajax({
      url: '/return_label',
      method: 'GET'
    }).done(function(r){
      console.log(r);
      $('#predict-in').text(r)
      console.log("ajax-success")
    }).fail(function(){
      console.log("ajax fail")
    });

}

function intervalLoad() {
    $("#predict-in").load("/return_label");
}

//
// function erase(){
//   $.ajax({
//     url: '/eraselabel',
//     method: 'GET'
//   }).done(function(r){
//     // console.log(r);
//     $('#label').text(r)
//     console.log("ajax-success")
//   }).fail(function(){
//     console.log("ajax fail")
//   });
//
// }
//

// 라벨 측정 시작
function keyPress(e) {
if (e.keyCode == 13) {
  change2();
  return false;
}
}
//
// //backspace : result 한글자 지움
// function keyDown(e) {
// if(e.keyCode == 8){
//   erase();
//   return false;
// }
//
// }