var hasLogin = false
function postLike_btn(facebook_post_id){
	if ($('#'+facebook_post_id+' .facebook_btn').attr('disable') == 'true' ){
		return;
	}

	$('#'+facebook_post_id+' .facebook_btn').toggleClass("fa-pulse fa-spinner fa-thumbs-up");
	$('#photoModal #photo_liked .facebook_btn').toggleClass("fa-pulse fa-spinner fa-thumbs-up");
	$('#'+facebook_post_id+' .facebook_btn').attr('disable',true);
	$('#photoModal #photo_liked .facebook_btn').attr('disable',true);

	var method = ''
	var v = $('.votes_'+facebook_post_id)
	var foo;
	if ($('#'+facebook_post_id+' .facebook_btn').hasClass('liked')){
		method = 'DELETE'
		foo = function(){
			$('#'+facebook_post_id+' .facebook_btn').toggleClass("liked");
			$('#photoModal #photo_liked .facebook_btn').toggleClass("liked");
			v.html(Number(v.html())-1);
			$('#photo_votes').html(Number($('#photo_votes').html())-1);
		};
	}
	else{
		method = 'POST'
		foo = function(){
			$('#'+facebook_post_id+' .facebook_btn').toggleClass("liked");
			$('#photoModal #photo_liked .facebook_btn').toggleClass("liked");
			v.html(Number(v.html())+1);
			$('#photo_votes').html(Number($('#photo_votes').html())+1);
		};
	}

	var default_func = function(){
		$('#'+facebook_post_id+' .facebook_btn').toggleClass("fa-pulse fa-spinner fa-thumbs-up");
		$('#photoModal #photo_liked .facebook_btn').toggleClass("fa-pulse fa-spinner fa-thumbs-up");
		$('#'+facebook_post_id+' .facebook_btn').attr('disable',false);
		$('#photoModal #photo_liked .facebook_btn').attr('disable',false);
	}

	if (hasLogin){
		__facebook_post_like(facebook_post_id,method,foo,default_func);
	}
	else{
		FB.login(function(response) {
			if (response.status === 'connected') {
				var __facebook_user_id = response.authResponse.userID;
				hasLogin = true
		      	if (response && !response.error) {
	        		__facebook_post_like(facebook_post_id,method,foo,default_func);
		      	}
		      	else{
		      		console.log('login failed');
		      		console.log(response);
		      	}
			}
			else{
				default_func();
			   	console.log('Please login and accept the permission');
			   	alert('Please login and accept the permission');
			}
		}, {auth_type: 'rerequest', scope: 'publish_actions',return_scopes: true});
	}

}

function __facebook_post_like(facebook_post_id,method,sucess_func, default_func){
	FB.api(
	    "/"+facebook_post_id+"/likes",
	    method,
	    function (response) {
	    	default_func();
	    	console.log(response)
	      	if (response && !response.error) {
	      		sucess_func();
	      	}
	      	else{
	      		hasLogin = false;
				alert('Please login to FB and accept the "publish_action" permission so we can post your like to the photo');
	      	}
	    }
	);
}

function likeComment(comment_id,element){

	if($('.facebook_btn',element).attr('disable') == 'true' ){
		return;
	}

	$('.facebook_btn',element).toggleClass("fa-pulse fa-spinner fa-thumbs-up");
	$('.facebook_btn',element).attr('disable',true);

	var method ='';
	var votes = $('.fb_likecount',element);
	var foo;
	if ( element.hasClass('liked') ){
		method = 'DELETE';
		foo = function(){
			element.toggleClass('liked');
			votes.html(Number(votes.html())-1);
		};
	}
	else{
		method = 'POST';
		foo = function(){
			element.toggleClass('liked');
			votes.html(Number(votes.html())+1);
		};
	}

	var default_func = function(){
		$('.facebook_btn',element).toggleClass("fa-pulse fa-spinner fa-thumbs-up");
		$('.facebook_btn',element).attr('disable',false);
	}

	if (hasLogin){
		__facebook_post_like(comment_id,method,foo,default_func);
	}
	else{
		FB.login(function(response) {
			if (response.status === 'connected') {
				var __facebook_user_id = response.authResponse.userID;
				hasLogin = true
		      	if (response && !response.error) {
	        		__facebook_post_like(comment_id,method,foo,default_func);
		      	}
		      	else{
		      		console.log('login failed');
		      		console.log(response);
		      	}
			}
			else{
				default_func();
			   	console.log('Please login and grant the permission');
			   	alert('請登入FB，並給予應用程式授權');
			}
		}, {auth_type: 'rerequest', scope: 'publish_actions',return_scopes: true});
	}
}

function post_command(modal_id, facebook_post_id){
	if($(modal_id+' #comment').val()==''){
		return;
	}

	var foo = function(){
		FB.api(
		  	'/me',
		  	'GET',
		  	{"fields":"picture{url},name"},
		  	function(response) {
		      	if (response && !response.error){
		      		avatar_url = response.picture.data.url;
			      	name = response.name;
			      	FB.api(
					  	facebook_post_id+'/comments',
					  	'POST',
					  	{"message":$(modal_id+' #comment').val()},
					  	function(response) {
					  		if (response && !response.error){
					  			item = $('#fb_comment_template').clone();
								item.removeAttr('id');
								$('.fb_avatar_frame img',item).attr('src',avatar_url);
								$('.fb_text_frame .fb_name',item).html(name);
								$('.fb_text_frame .fb_likecount',item).html(0);
								$('.fb_text_frame .fb_message',item).html($(modal_id+' #comment').val().replace(/(\n|\r)+/g,'<br>'));
								$('.fb_text_frame .fb_like',item).click(function(){
									likeComment(response.id, $(this));
								});
								$('#photoModal #facebook_comments').append('<hr>');
								$('#photoModal #facebook_comments').append(item);
								$(modal_id+' #comment').val('');
					  		}
					  		else{
					  			console.log(response);
					  			alert('發佈留言失敗');
					  			hasLiked = false;
					  		}

					  	}
					);
		      	}
		      	else{
		      		console.log(response);
		      		alert('發佈留言失敗');
		      		hasLiked = false;
		      	}
		  	}
		);
	};
	if (modal_id[0] != '#')
		modal_id = '#'+modal_id;
	if (hasLogin){
		foo();
	}
	else{
		FB.login(function(response) {
			if (response.status === 'connected') {
				var __facebook_user_id = response.authResponse.userID;
				hasLogin = true
		      	if (response && !response.error) {
		      		foo();
		      	}
		      	else{
		      		console.log('login failed');
		      		console.log(response);
		      	}
			}
			else{
			   	console.log('Please login and grant the permission');
			   	alert('請登入FB，並給予應用程式授權');
			}
		}, {auth_type: 'rerequest', scope: 'publish_actions',return_scopes: true});
	}
}

window.fbAsyncInit = function() {
	FB.init({
		appId      : '1683882248550115',
		cookie     : true,  // enable cookies to allow the server to access
	                        // the session
		xfbml      : true,  // parse social plugins on this page
		version    : 'v2.5' // use version 2.2
	});


	/*FB.getLoginStatus(function(response) {
    	statusChangeCallback(response);
  	});*/
};

(function(d, s, id) {
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) return;
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk')
);

/*function statusChangeCallback(response) {
    if (response.status === 'connected') {
      	hasLogin = true;
    } else if (response.status === 'not_authorized') {
      	//alert('Please login to FB and accept the "publish_action" permission so we can post your like to the photo');

    } else {
      	//alert('Please login to FB and accept the "publish_action" permission so we can post your like to the photo');

    }
}

function checkLoginState() {
    FB.getLoginStatus(function(response) {
	      statusChangeCallback(response);
    });
}*/


