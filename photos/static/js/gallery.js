var small_frame_height = 0;

function render_gallery(){
	$('.image_frame').each(function(index){
    	$(this).height($(this).width()*3/4)
    });

    $('.small_frame').each(function(index){
    	if (index == 0)
    		small_frame_height = $(this).width()*3/4
    	$(this).height(small_frame_height)
    });

    $('img').each(function(index){
    	render_image($(this));
    })
}

function render_image(image){
	if (image.height() == 0 || image.width() == 0)
		return;

	if ( image.height() >= image.width() ){
		image.width(Math.floor(image.parent().width()))
		image.css('margin-top',-1*(image.height()-image.parent().height())/2)
	}
	else{
		image.height(Math.floor(image.parent().height()))
		image.css('margin-left',-1*(image.width()-image.parent().width())/2)
	}
}



function initGallery(){
	window.addEventListener("resize", render_gallery);
	$(document).ready(function(){
	    render_gallery();
	});
}