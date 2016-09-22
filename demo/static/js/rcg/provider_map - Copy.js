      function getQueryVariable(variable)
      {
             var query = window.location.search.substring(1);
             var vars = query.split("&");
             for (var i=0;i<vars.length;i++) {
                     var pair = vars[i].split("=");
                     if(pair[0] == variable){return pair[1];}
             }
             return(false);
      }
      // This example requires the Places library. Include the libraries=places
      // parameter when you first load the API. For example:
      // <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

      var map;
      var infowindow;
      var markers = [];
      var people = [];
      var nyc = {lat: 40.713, lng: 74.001};
      // var pinColor1 = "FE7569";
      // var pinColor2 = "0000AA";
      // var pinImage1, pinImage2, pinShadow;
      var pinColor = "0000AA";

       function initMap() {
        // var pyrmont = {lat: -33.867, lng: 151.195};

        // pinImage1 = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor1,
        //     new google.maps.Size(21, 34),
        //     new google.maps.Point(0,0),
        //     new google.maps.Point(10, 34));
        // pinImage2 = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor2,
        //     new google.maps.Size(21, 34),
        //     new google.maps.Point(0,0),
        //     new google.maps.Point(10, 34));
        // pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        //     new google.maps.Size(40, 37),
        //     new google.maps.Point(0, 0),
        //     new google.maps.Point(12, 35));

        // alert("hi2");
        map = new google.maps.Map(document.getElementById('map'), {
          center: nyc,
          // zoom: 15      // zoomed in neighborhood
          zoom: 13      // zoomed
          // zoom: 10   // zoomed out super county
          // SC for fun
          //, mapTypeId: 'terrain'
        });

        var geocoder = new google.maps.Geocoder();

        document.getElementById('submitNearby').addEventListener('click', function() {
          geocodeAddress(geocoder, map, 'My Address');
          // searchNearby(geocoder, map);
          searchBoth(geocoder, map);
        });

        /* document.getElementById('submitText').addEventListener('click', function() {
          geocodeAddress(geocoder, map, 'My Address');
          searchText(geocoder, map);
        }); */

        //  document.getElementById('getMembers').addEventListener('click', function() {
        //   addMemberAddresses(geocoder, map);
        // });

        // My location
        infoWindow = new google.maps.InfoWindow({map: map});

        // console.log(navigator.userAgent.toLowerCase())
        chrome = /chrome/.test(navigator.userAgent.toLowerCase());
        // chrome = navigator.userAgent.toLowerCase().indexOf('chrom')
        console.log('is chrome: ' + chrome)
        // console.log("after me")
        // map = new google.maps.Map(document.getElementById('map'), {
        //   center: nyc,
        //   zoom: 13      // zoomed
        // });
        // var geocoder = new google.maps.Geocoder();
        if (!chrome || true) {
          getMyAddress(map, infoWindow);
        }
        geocodeAddress(geocoder, map, 'My Address');
        addMemberAddresses(geocoder, map);

        // pinColor = "FE7569";

        /*infowindow = new google.maps.InfoWindow();
        var service = new google.maps.places.PlacesService(map);
        service.nearbySearch({
          location: pyrmont,
          radius: 500,
          type: ['store']
        }, callback);*/
      }

      function getMyAddress(map, infoWindow) {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Your current location.');
            map.setCenter(pos);
            // addMarker(pos);
            // var marker = new google.maps.Marker({
            //   map: map,
            //   position: pos,
            //   title: 'Me'
            // });
            addPerson(pos, 'Me', 'Me', 0)
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }

      function handleLocationError(browserHasGeolocation, infoWindow, pos) {

        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Could not determine your location.' :
                              'Error: Your browser doesn\'t support geolocation.');
        map.setCenter(nyc);
        console.log("error")
      }

      function callback(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          for (var i = 0; i < results.length; i++) {
            // createMarker(results[i]);
            addMarker(results[i]);
          }
        }
      }

      // function createMarker(place) {
      function addMarker(place) {
        var placeLoc = place.geometry.location;
        var marker = new google.maps.Marker({
          map: map,
          position: place.geometry.location
          // icon: pinImage2,
          // shadow: pinShadow
        });

        google.maps.event.addListener(marker, 'click', function() {
          infowindow.setContent(place.name);
          infowindow.open(map, this);
        });
        markers.push(marker);
      }

      // function createMarker(place) {
      //http://stackoverflow.com/questions/7095574/google-maps-api-3-custom-marker-color-for-default-dot-marker
      function addPerson(location, hover, popup, membid) {
        var marker = new google.maps.Marker({
          map: map,
          position: location,
          title: hover
        });
        // marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
        if (membid == 0) {
          marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
        } else {
          marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
        }
        // console.log(hover, membid)
        google.maps.event.addListener(marker, 'click', function() {
          // infoWindow.setContent('<a href= "http://127.0.0.1:8000/">'+popup+'</a>');
          // infoWindow.setContent('<a href= "{% url 'member_detail' pk=4 %}">'+popup+'</a>');
          if (membid == 0) {
            infoWindow.setContent(popup);
          } else {
            // mstr = 'member_detail pk=' + id
            // memburl = "{% url 'member_detail' pk=1 %}"
            memburl = $member_detail_url
            url2 = memburl.substr(0,memburl.length-2) + membid + '/'
            console.log(url2)
            infoWindow.setContent('<a href= "' + url2 + '">'+popup+'</a>');
          }
          infoWindow.open(map, this);
        });
        people.push(marker);
      }

//SC: http://127.0.0.1:8000/static/map.html?city=Morris%20Plains
      function geocodeAddress(geocoder, resultsMap, title) {
        // var address = document.getElementById('address').value;
        // alert("hi");
        // var city = decodeURI(getQueryVariable("city"));
        // // alert(city);
        // var state = decodeURI(getQueryVariable("state"));
        // var address = city + ", " + state;
        // document.getElementById('address').value = address;
        address = document.getElementById('address').value;
        console.log('address: ' + address)
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
            resultsMap.setCenter(results[0].geometry.location);
            // var marker = new google.maps.Marker({
            //   map: resultsMap,
            //   position: results[0].geometry.location,
            //   title: 'My Address'
            // });
            addPerson(results[0].geometry.location, title, title, 0)

//             infowindow = new google.maps.InfoWindow();
//             var service = new google.maps.places.PlacesService(resultsMap);
//             service.nearbySearch({
//               location: results[0].geometry.location,
//               radius: 500,
// //              type: ['store']
//               type: [document.getElementById('searchTerm').value]
//             }, callback);

          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

      }

      var jdata = []
      function addMemberAddresses(geocoder, resultsMap) {
          var i = 0, j = 0
          var name, addr
          jdata = []
          $.getJSON("/provider_members/" + $provider_id, {},
            function(json){
              // console.log(json);  // sanity check
              $.each(json, function (index, value) {
                  nm = value.first_name + " " + value.last_name;
                  addr = value.address + ", " + value.state + " " + value.zip;
                  member_id = value.id;
                  // console.log(nm + addr);
                  jdata.push([nm, addr, member_id]);
                  // console.log(jdata[i])
                  geocoder.geocode({'address': addr}, function(results, status) {
                    if (status === 'OK') {
                      // console.log("--"+nm+j+results)
                      // console.log(j+"--"+jdata[j][0])
                      // resultsMap.setCenter(results[0].geometry.location);
                      addPerson(results[0].geometry.location, jdata[j][0], jdata[j][0] + " " + jdata[j][1], jdata[j][2])
                      j++
                    } else {
                      alert('Geocode was not successful for the following reason: ' + status);
                    }
                  });
                  i++;
              });
            //   queryData = jdata;
            // ajaxComplete = true;
            // console.log("queryMin: " + (new Date(queryMin)).toLocaleTimeString() + " queryMax: " + (new Date(queryMax)).toLocaleTimeString() + " queryData.length: " + queryData.length);
            // console.log("queryData: queryData.length: " + queryData.length + " queryDataMin: " + (new Date(queryData[0][0])).toLocaleTimeString() + " queryDataMax: " + (new Date(queryData[queryData.length-1][0])).toLocaleTimeString());

          });
        // call is asynchronous so data is not populated by this point
          return;
      };

//       function searchNearby(resultsMap) {
//         infowindow = new google.maps.InfoWindow();
//         var service = new google.maps.places.PlacesService(resultsMap);
//         service.nearbySearch({
//           location: results[0].geometry.location,
//           radius: 500,
// //              type: ['store']
//           type: [document.getElementById('searchTerm').value]
//         }, callback);

//       }

      function searchNearby(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {

            deleteMarkers();

            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });

            infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(resultsMap);
            // alert('Search: ' + document.getElementById('searchType').value);
            var request = {
              location: results[0].geometry.location,
              radius: 500,
              type: [document.getElementById('searchType').value]
              // type: ['hospital']
              // type: ['store']
              // valid types: https://developers.google.com/places/supported_types
            }
            service.nearbySearch(request, callback);

            // setMapOnAll(resultsMap)
            showMarkers();

          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

      }


      function searchText(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {

            deleteMarkers();

            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });

            infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(resultsMap);
            // alert('Search: ' + document.getElementById('searchTerm').value);
            var request = {
              location: results[0].geometry.location,
              radius: 500,
//              type: ['store']
              query: [document.getElementById('searchTerm').value]
            }
            service.textSearch(request, callback);

            // setMapOnAll(resultsMap)
            showMarkers();

          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

      }


      function searchBoth(geocoder, resultsMap) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {

            deleteMarkers();

            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
              map: resultsMap,
              position: results[0].geometry.location
            });

            infowindow = new google.maps.InfoWindow();
            var service = new google.maps.places.PlacesService(resultsMap);
            // alert('Search: ' + document.getElementById('searchType').value);
            var request = {
              location: results[0].geometry.location,
              radius: 500,
              type: [document.getElementById('searchType').value]
              // type: ['hospital']
              // type: ['store']
              // valid types: https://developers.google.com/places/supported_types
            }
            service.nearbySearch(request, callback);

            var request = {
              location: results[0].geometry.location,
              radius: 500,
//              type: ['store']
              query: [document.getElementById('searchType').value]
            }
            service.textSearch(request, callback);

            // setMapOnAll(resultsMap)
            showMarkers();

          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

      }


      // Sets the map on all markers in the array.
      function setMapOnAll(map) {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(map);
        }
      }

      // Removes the markers from the map, but keeps them in the array.
      // function clearMarkers() {
      //   setMapOnAll(null);
      // }
      function clearMarkers(map) {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(null);
        }
      }

      // Shows any markers currently in the array.
      function showMarkers() {
        setMapOnAll(map);
      }

      // Deletes all markers in the array by removing references to them.
      function deleteMarkers() {
        clearMarkers();
        markers = [];
      }