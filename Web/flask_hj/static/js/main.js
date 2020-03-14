$(document).on('click', '.alphabet', function(){
  var id = $(this).text();
  edit_data(id);
  function edit_data(id) {
      $.ajax({
          url:'/question',
          method:"POST",
          data:JSON.stringify($(this).attr("id")),
          dataType:"text",
          success:function(data){
              alert(data);
          }
      });
  }
});


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

function keyPress(e) {
    if (e.keyCode == 13) {
        // regist();
        setInterval(regist , 1000);
        return false;
    }
}

// $(function() {
//     timer = setInterval( function () {
//         //----------------------------------------------------------------------------------
//         $.ajax ({
//             "url" : "[받아올 내용이 있는 URL]",  // ----- (1)
//             cache : false,
//             success : function (html) { // ----- (2)
//                 [받아온 내용을 처리할 부분] // ----- (3)
//                 [받아온 내용은 변수 html로 전달]
//             }
//         });
//         //----------------------------------------------------------------------------------
//     }, 30000); // 30초에 한번씩 받아온다.
// });





// 순서 1. button을 누른다.
// 2. button 의 아이디(알파벳)가 ajax를 통해 서버로 보내지고 이걸 저장한다.
// 3. html의 question이 해당 알파벳으로 바꾼다. & 이미지도 해당 알파벳으로 바뀐다.
// 4. 맞음/틀림을 판단할때 해당 알파벳으로 판단한다.