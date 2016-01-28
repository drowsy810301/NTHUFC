var markerList = [];
var markerCount = [];
var google_map;
var flag = 0;

function initMap_1() {
	var customMapType = new google.maps.StyledMapType([
		  {
		    stylers: [
		      {visibility: 'simplified'},
		      {gamma: 0.5},
		      {weight: 0.5}
		    ]
		  },
	], {
	  name: 'Custom Style'
	});
	var customMapTypeId = 'custom_style';

    var myLatLng = {lat: 24.7945436, lng: 120.9932738};

    var mapOptions = {
        zoom: 15,
        center: myLatLng,
        mapTypeControlOptions: {
	      mapTypeIds: [google.maps.MapTypeId.ROADMAP, customMapTypeId]
	    }
    };
    google_map = new google.maps.Map(document.getElementById('google_map'),mapOptions);
    google_map.mapTypes.set(customMapTypeId, customMapType);
		google_map.setMapTypeId(customMapTypeId);
    for ( i in markerList ) {
        addMarker_1(google_map, markerList[i].title, {lat: markerList[i].lat, lng: markerList[i].lng})
    }
    console.log('google map loading finish')
}

function addMarker_1(map, title, location){
    var marker = new google.maps.Marker({
        position: location,
        map: map,
        label: title,
        title: title,
    });

    marker.addListener('click', function() {
        filter_photos(marker.title);
    });

    for ( i in markerCount ) {
        if( markerCount[i].title.match(marker.title) != null ){
            var infowindow = new google.maps.InfoWindow({
                content: '一共有' + markerCount[i].count + '張照片',
            });
            break;
        }
    }

    /*var infowindow = new google.maps.InfoWindow({
        //content: 'Hello World',
    });*/

    marker.addListener('mouseover', function() {
        infowindow.open(map, marker);
    });
}

function initMarker(markers){
    markerList = markers
}

function initMarkerCount(markers){
    markerCount = markers
}

function filter_photos(filt_key){
	for( i in photo_list) {
    	if( photo_list[i].title.match(filt_key)==null && photo_list[i].content.match(filt_key)==null && photo_list[i].tags.match(filt_key)==null && photo_list[i].location.match(filt_key)==null){
    		document.getElementById(photo_list[i].fbID).style.display = 'none';
    	}
    	else {
    		document.getElementById(photo_list[i].fbID).style.display = 'block';
    	}
    }
    document.getElementById("show_marker").innerHTML = "目前Map Marker: " + filt_key;
}

function filter_photos2(filt_key){
	for( i in photo_list) {
		if( photo_list[i].title.match(filt_key)==null && photo_list[i].content.match(filt_key)==null && photo_list[i].tags.match(filt_key)==null && photo_list[i].location.match(filt_key)==null){
    		if(flag == 0){
    			document.getElementById(photo_list[i].fbID).style.display = 'none';
    		}
    	}
    	else {
    		document.getElementById(photo_list[i].fbID).style.display = 'block';
    	}
	}
    document.getElementById("show_tag").innerHTML += " " + filt_key; 
	flag = 1;
}

function cancel_filter(){
	for( i in photo_list) {
		document.getElementById(photo_list[i].fbID).style.display = 'block';
	}
    document.getElementById("show_tag").innerHTML = "目前Tag:";
    document.getElementById("show_marker").innerHTML = "目前Map Marker: ";
	flag = 0;
}