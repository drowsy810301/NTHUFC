var all_tags = [], hot_tags=[], recent_tags=[];
var tag_input;
var google_map;
var markerList = [];

var substringMatcher = function(strs) {
	return function findMatches(q, cb) {
		var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
			if (substrRegex.test(str)) {
				matches.push(str);
            }
        });

        cb(matches);
    };
};

function init_tag_typeahead(id_input , _all_tags, _hot_tags, _recent_tags){
	all_tags = _all_tags;
	hot_tags = _hot_tags;
	recent_tags = _recent_tags;
	tag_input = $('#img-tags');
	tag_input.tagsinput({
		maxTags:3,
		maxChars:6,
		trimValue: true,
		tagClass: 'purple_label',
		typeaheadjs: [{
			highlight:true,
			minLength: 1
		},
		{
			name: 'tags',
			source: substringMatcher(all_tags)
		}],
	});

	tag_input.on('itemAdded', function(event) {
	 	$('#tag_count').html(tag_input.tagsinput('items').length)
	});
	$('input').on('itemRemoved', function(event) {
	  	$('#tag_count').html(tag_input.tagsinput('items').length)
	});
}


function addTag(str){
	tag_input.tagsinput('add', str);
}

function toggelMap(){
	if ($("#google_map").css('display') == 'none'){
		$('#toggle_map_button').html('收起')
	}
	else{
		$('#toggle_map_button').html('展開')
	}
	$("#google_map").animate({height: 'toggle'},{complete:initMap});
}

function initMap() {
    var myLatLng = {lat: 24.7913341, lng: 120.994148};

    var mapOptions = {
        zoom: 16,
        center: myLatLng,
    };
    google_map = new google.maps.Map(document.getElementById('google_map'),mapOptions);
    for ( i in markerList){
        addMarker(google_map, markerList[i].title, {lat: markerList[i].lat, lng: markerList[i].lng})
        if (markerList[i].title == $('#img-location').val())
        	google_map.setCenter({lat: markerList[i].lat, lng: markerList[i].lng})
    }
    console.log('google map loading finish')
}

function addMarker(map, title, location){
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        label: title,
        title: title,
    });

    marker.addListener('click', function() {
        $('#img-location').val(marker.title)
        google_map.setCenter(marker.getPosition())
    });
}

function initMarker(markers){
    markerList = markers
}
