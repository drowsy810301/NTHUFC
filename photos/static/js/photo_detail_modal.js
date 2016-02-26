var hasLogin = false

// used to store usre's vote on each photo, the result will be stored using cookie
var vote_record = {}

// used to store usre's reported comments, the result will be stored using cookie
var reported_comments_record = []

$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
	//Used for recording user's like and favorite
	var tmp = Cookies.getJSON('vote_record')
	if ( tmp ){
		vote_record = tmp
		for ( facebook_post_id in vote_record ){
			if ( vote_record.hasOwnProperty(facebook_post_id) ){
				if ( vote_record[facebook_post_id].fb ){
					$('#'+facebook_post_id+' .facebook_btn').toggleClass("liked");
				}

				if ( vote_record[facebook_post_id].flickr ){
					$('#'+facebook_post_id+' .flickr_btn').toggleClass("favorited");
				}

				if ( vote_record[facebook_post_id].vote > Number($('.votes_'+facebook_post_id).html()) ){
					$('.votes_'+facebook_post_id).html( vote_record[facebook_post_id].vote )
				}
			}
		}
	}

	var tmp = Cookies.getJSON('reported_comments_record')
	if (tmp){
		reported_comments_record = tmp
	}
});


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
			if ( vote_record[facebook_post_id] ){
				if ( vote_record[facebook_post_id].flickr == false ){
					delete vote_record[facebook_post_id]
				}
				else{
					vote_record[facebook_post_id].vote = Number(v.html())
					vote_record[facebook_post_id].fb = false
				}
			}
			Cookies.set('vote_record',vote_record)
		};
	}
	else{
		method = 'POST'
		foo = function(){
			$('#'+facebook_post_id+' .facebook_btn').toggleClass("liked");
			$('#photoModal #photo_liked .facebook_btn').toggleClass("liked");
			v.html(Number(v.html())+1);
			$('#photo_votes').html(Number($('#photo_votes').html())+1);
			if ( vote_record[facebook_post_id] ){
				vote_record[facebook_post_id].vote = Number(v.html())
				vote_record[facebook_post_id].fb = true
			}
			else{
				vote_record[facebook_post_id] = { 'vote': Number(v.html()), 'fb': true, 'flickr': false }
			}
			Cookies.set('vote_record',vote_record)
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
		}, {auth_type: 'rerequest', scope: 'publish_actions'});
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
					  			modal_facebook_comment_list.push({
									facebook_comment_id:response.id,
									name: name,
									message: $(modal_id+' #comment').val(),
								})
					  			item = $('#fb_comment_template').clone();
								item.attr('id','comment_'+response.id);
								$('.fb_avatar_frame img',item).attr('src',avatar_url);
								$('.fb_text_frame .fb_name',item).html(name);
								$('.fb_text_frame .fb_likecount',item).html(0);
								$('.fb_text_frame .fb_message',item).html($(modal_id+' #comment').val().replace(/(\n|\r)+/g,'<br>'));
								$('.fb_text_frame .fb_like',item).attr('onclick','likeComment("'+response.id+'",$(this))');
								$('.fb_text_frame .fb_report',item).attr('onclick','reportComment('+(modal_facebook_comment_list.length-1)+')');
								$('#photoModal #facebook_comments').append(item);
								$(modal_id+' #comment').val('');
								$(modal_id+' [data-toggle="tooltip"]').tooltip();
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
		appId      : '1645068735761448',
		cookie     : true,  // enable cookies to allow the server to access
	                        // the session
		xfbml      : true,  // parse social plugins on this page
		version    : 'v2.5' // use version 2.2
	});
};

(function(d, s, id) {
		var js, fjs = d.getElementsByTagName(s)[0];
		if (d.getElementById(id)) return;
		js = d.createElement(s); js.id = id;
		js.src = "//connect.facebook.net/en_US/sdk.js";
		fjs.parentNode.insertBefore(js, fjs);
	}(document, 'script', 'facebook-jssdk')
);

