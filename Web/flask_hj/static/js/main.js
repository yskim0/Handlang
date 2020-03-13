function question(){
  $.ajax({
    url: '/question',
    method: 'GET'
  }).done(function(r){
    // console.log(r);
    $('#label').text(r)
    console.log("ajax-success")
  }).fail(function(){
    console.log("ajax fail")
  });

}

// 순서 1. button을 누른다.
// 2. button 의 아이디(알파벳)가 ajax를 통해 서버로 보내지고 이걸 저장한다.
// 3. html의 question이 해당 알파벳으로 바꾼다. & 이미지도 해당 알파벳으로 바뀐다.
// 4. 맞음/틀림을 판단할때 해당 알파벳으로 판단한다.