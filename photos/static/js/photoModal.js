var out = "";
var quest;
var modalHead = "";
var modalBody = "";
var modalFoot = "";
var tempName = "";
function statusChangeCallback(response) {
  var userInput;
  console.log('statusChangeCallback');
  console.log(response);
  // The response object is returned with a status field that lets the
  // app know the current login status of the person.
  // Full docs on the response object can be found in the documentation
  // for FB.getLoginStatus().
  if (response.status === 'connected') {
    // Logged into your app and Facebook.
    //如果使用者成功登入就使用FB api去使用者牆上抓文章
    FB.api('me/photos','GET',{"fields":"name,picture,id"},function(response){
        if(!response || response.error){
          console.log("wrong request");
        }
        else{
          //console.log(response);
          //console.log(response.data[0]);
          //得到的json檔中所有的文章都存在data陣列中
          quest = response.data;
        }
        console.log(quest);
        //console.log(quest[0].images[7].source);
        //設定網頁標題
        //document.getElementById("QuestionTitle").innerHTML = "Let\'s see what you got on your wall";
        //document.getElementById("info").innerHTML = "The latest 25 posts. Choose one and see the comments.";
        //瀏覽所有文章，並將每個文章的文字擷取出來，當作瀏覽留言的連結
        for(var j = 0;j<quest.length;j++){
          if(!quest[j].name||quest[j].name.error){
            tempName = "沒有說明"
          }
          else{
            tempName = quest[j].name;
          }
          out += "<li id = \"" + quest[j].id + "\"><a href = \"#\" onclick = \"getPhotoInfo(\'" + quest[j].id + "\',setModal)\"><img id = \"" + quest[j].id + "\" src = \"" + quest[j].picture
          + "\" ></a><p>" + tempName + "</p></li>";
          //data-toggle = \"modal\" data-target = \"#PhotoModal\"
        }
        document.getElementById("photoList").innerHTML = out;
    });

    console.log("successful login");
    //window.location = "http://localhost:5000/"
  } else if (response.status === 'not_authorized') {
    alert('Please log ' + 'into this app.');
    FB.login(function(response){statusChangeCallback(response);},{scope: 'user_photos'});
  } else {
    alert('Please log ' + 'into Facebook.');
    FB.login(function(response){statusChangeCallback(response);},{scope: 'user_photos'});
  }
}

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    //呼叫statusChangeCallback檢查使用者登入情形
    statusChangeCallback(response);
  });
}

// $('#PhotoModal').on('show.bs.modal',function(event){
//   var relatePic = $(event.relatedTarget);
//   var modal = $(this);
//   console.log("beforeGet");
//   //console.log(relatePic);
//   //console.log(relatePic.context.id);
//   getPhotoInfo(relatePic.context.id,setModal);
//   console.log("afterGet");
//   console.log(modalHead);
//   modal.find('.modal-title').text(modalHead);
// })

function getPhotoInfo(id,setM){
  console.log("beforeFB");
  //console.log("ID: " + id);
  FB.api('/' + id,'GET',{"fields":"name,likes.summary(total_count),images{source},comments{message,likes.summary(total_count),from{name,picture{url}}}"},function(response){
    console.log(response);
    console.log("justGet response");
    setModal(response);
    console.log("finishSetting");
  });
}

function setModal(response){
  var nameGot;
  var imagesGot;
  var likesGot;
  var commentsGot;
  console.log("TestRes:" + response);
  if(!response.name || response.name.error){
    nameGot = "沒有說明"
  }
  else{
    nameGot = response.name;
  }
  if(!response.images||response.images.error){
    imagesGot = "No images"
  }
  else{
    imagesGot = response.images;
  }
  if(!response.likes||response.likes.error){
    likesGot = 0;
  }
  else{
    likesGot = response.likes.summary.total_count;
  }
  console.log("setting modal");
  modalHead = "<h4 class = \"modal-title\">" + nameGot + "</h4><small>讚：" + likesGot + "</small>";
  //console.log("modalheadinsetmodal:" + modalHead);
  document.getElementById("PhotoModalLabel").innerHTML = modalHead;
  //console.log(imagesGot);
  modalBody = "<img src = \"" + imagesGot[0].source + "\">";
  document.getElementById("modB").innerHTML = modalBody;
  modalFoot = "";
  modalFoot += "<ul>";
  if(!response.comments || response.comments.error){
    document.getElementById("modF").innerHTML = "沒有回應";
  }
  else{
    commentsGot = response.comments.data;
    for(var i = 0;i<commentsGot.length;i++){
      modalFoot += "<li><img src = \"" + commentsGot[i].from.picture.data.url + "\"><span>" + commentsGot[i].from.name + "</span><div>" + commentsGot[i].message +"   讚："+likesGot+"</div></li>";
    }
    modalFoot += "</ul>";
    document.getElementById("modF").innerHTML = modalFoot;
  }
  $('#PhotoModal').modal('show');
}


window.fbAsyncInit = function() {
  FB.init({
    appId      : '1645068735761448',
    xfbml      : true,
    version    : 'v2.5'
  });

// Now that we've initialized the JavaScript SDK, we call
// FB.getLoginStatus().  This function gets the state of the
// person visiting this page and can return one of three states to
// the callback you provide.  They can be:
//
// 1. Logged into your app ('connected')
// 2. Logged into Facebook, but not your app ('not_authorized')
// 3. Not logged into Facebook and can't tell if they are logged into
//    your app or not.
//
// These three cases are handled in the callback function.

//在進入此頁面FB load完他的SDK時檢查使用者登入情況
checkLoginState();

};

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/sdk.js";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph API after login is
// successful.  See statusChangeCallback() for when this call is made.
function testAPI() {
  console.log('Welcome!  Fetching your information.... ');
  FB.api('/me', function(response) {
    console.log('Successful login for: ' + response.name);
    document.getElementById('status').innerHTML =
      'Thanks for logging in, ' + response.name + '!';
  });
}