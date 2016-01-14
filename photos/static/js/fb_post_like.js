var hasLogin = false
function postLike_btn(facebook_post_id){
	var method = ''
	var v = $('.votes_'+facebook_post_id)
	if ($('#'+facebook_post_id+' .fa-thumbs-up').hasClass('liked')){
		method = 'DELETE'
	}
	else{
		method = 'POST'
	}
	$('#'+facebook_post_id+' .fa-thumbs-up').toggleClass("liked");
	$('#photo_details_modal .fa-thumbs-up').toggleClass("liked");

	if (hasLogin){
		__facebook_post_like(facebook_post_id,method,v);
	}
	else{
		FB.login(function(response) {
			if (response.status === 'connected') {
				var __facebook_user_id = response.authResponse.userID;
				hasLogin = true
		      	if (response && !response.error) {
	        		__facebook_post_like(facebook_post_id,method,v);
		      	}
		      	else{
		      		console.log('login failed');
		      		console.log(response);
		      	}
			}
			else{
			   	console.log('Please login and grant the permission');
			   	alert('Please login and grant the permission');
			}
		}, {auth_type: 'rerequest', scope: 'publish_actions',return_scopes: true});
	}

}

function __facebook_post_like(facebook_post_id,method,element){
	FB.api(
	    "/"+facebook_post_id+"/likes",
	    method,
	    function (response) {
	    	console.log(response)
	      	if (response && !response.error) {
	      		if (method == 'POST')
	      			element.html(Number(element.html())+1);
	      		else
	      			element.html(element.html()-1);
	      	}
	      	else{
	      		hasLiked = false;
	      	}
	    }
	);
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