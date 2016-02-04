var markerList = [];
var markerCount = [];
var tagList = [];
var google_map;
var nowMarker = '';
var flag = 0;

function initMap() {
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
        addMarker(google_map, markerList[i].title, {lat: markerList[i].lat, lng: markerList[i].lng})
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
        filter_photos_ForMarker(marker.title);
    });

    for ( i in markerCount ) {
        if( markerCount[i].title.match(marker.title) != null ){
            var infowindow = new google.maps.InfoWindow({
                content: '一共有' + markerCount[i].count + '張照片',
            });
            break;
        }
    }
    marker.addListener('mouseover', function() {
        infowindow.open(map, marker);
    });
    marker.addListener('mouseout', function(){
        infowindow.close();
    });
}

function initMarker(markers){
    markerList = markers;
}

function initMarkerCount(markers){
    markerCount = markers;
}

function initTag(tags){
    tagList = tags;
}

function filter_photos_ForMarker(filt_key){
    for( i in photo_list ) {
        if( photo_list[i].isReady == 'True' ) {
            if( photo_list[i].location.match(filt_key)==null ){
                document.getElementById(photo_list[i].fbID).style.display = 'none';
            }
            else {
                document.getElementById(photo_list[i].fbID).style.display = 'block';
            }
        }
    }
    nowMarker = filt_key;
    document.getElementById("show_marker").innerHTML = "目前Map Marker: " + filt_key;
}

function filter_photos_ForTag(filt_key){
    var nowTags = document.getElementById("show_tag").innerHTML;
    if( nowTags.match(filt_key) == null ){
        document.getElementById(filt_key).style.background = 'red';
        for( i in photo_list) {
            if( photo_list[i].location.match(nowMarker) != null ) {
                var tags_atLocation = photo_list[i].tags.split(' ');
                var tmp_atLocation = 0;
                for( j in tags_atLocation ) {
                    if( tags_atLocation[j] == filt_key ) {
                        document.getElementById(photo_list[i].fbID).style.display = 'block';
                        photo_list[i].isReady = 'True';
                        tmp_atLocation = 1;
                        break;
                    }
                }
                if( tmp_atLocation == 0 ) {
                    if( flag == 0 ) {
                        document.getElementById(photo_list[i].fbID).style.display = 'none';
                        photo_list[i].isReady = 'False';
                    }
                }
            }
            else {
                var tags_not_atLocation = photo_list[i].tags.split(' ');
                var tmp_not_atLocation = 0;
                for( j in tags_not_atLocation ) {
                    if( tags_not_atLocation[j] == filt_key ) {
                        photo_list[i].isReady = 'True';
                        tmp_not_atLocation = 1;
                        break;
                    }
                }
                if( tmp_not_atLocation == 0 ) {
                    photo_list[i].isReady = 'False';
                }
            }
        }
        document.getElementById("show_tag").innerHTML += " " + filt_key;
    }
    flag = 1;
}

function cancel_filter(){
	for( i in photo_list) {
		document.getElementById(photo_list[i].fbID).style.display = 'block';
        photo_list[i].isReady = 'True';
	}
    for ( i in tagList){
        document.getElementById(tagList[i].title).style.background = '#e7e7e7';
    }
        
    document.getElementById("show_tag").innerHTML = "目前Tag:";
    document.getElementById("show_marker").innerHTML = "目前Map Marker: ";
	flag = 0;
    nowMarker = '';
}