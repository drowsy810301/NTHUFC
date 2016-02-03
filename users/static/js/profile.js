$(document).ready(function(){

    $("[rel='tooltip']").tooltip();

    $('#hover-cap-4col .thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(250);
        },
        function(){
            $(this).find('.caption').slideUp(250);
        }
    );

    $('#hover-cap-3col .thumbnail').hover(
        function(){
            $(this).find('.caption').fadeIn(250);
        },
        function(){
            $(this).find('.caption').fadeOut(250);
        }
    );

    $('#hover-cap-unique .thumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(500);
        },
        function(){
            $(this).find('.caption').slideUp(500);
        }
    );

    $('#hover-cap-6col .thumbnail').hover(
        function(){
            $(this).find('.caption').show();
        },
        function(){
            $(this).find('.caption').hide();
        }
    );
    $('.test-jquery-click').click(function() {
        delete_photo($(this).attr('id'));
    });
    $(".popconfirm").popConfirm();
});

function fb_link(post_id, object){
    var str = post_id.split('_');
    var id = str[1];
    object.href = "https://www.facebook.com/1528712347441804/photos/a.1528722767440762.1073741826.1528712347441804/" + id + "/?type=3&theater";
    console.log(object.href);
}

function delete_photo(delete_id){
    window.location.href = "http://" + window.location.host +
    "/users/delete_photo/" + delete_id;
}
