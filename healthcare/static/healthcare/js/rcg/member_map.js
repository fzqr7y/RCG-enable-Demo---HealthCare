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
      var allMarkers = {};
      allMarkers.default = markers;
      var searchTerm = null;
      var people = [];
      var nyc = {lat: 40.713, lng: 74.001};
      // var pinColor1 = "FE7569";
      // var pinColor2 = "0000AA";
      // var pinImage1, pinImage2, pinShadow;
      // var pinColor = "0000AA";
      // var my_address = document.getElementById('address').value;

      // This function is used in the home / county_map pages.
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
          geocodeAddress(geocoder, map, 'Address');
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

        // checkboxes in _wid_member_map_search.html
        $("form#member-map-search-form input:checkbox").change(function() {
            if(this.checked) {
                // alert("value: " + this.value + ' this.offsetParent.innerText: ' + this.offsetParent.innerText)
                console.log("value: " + this.value + ' this.offsetParent.innerText: ' + this.offsetParent.innerText);
                // console.log('document.getElementById("chklabelid"): ' + document.getElementById("chklabelid").innerHTML);
                // console.log('Searching for: ' + this.value);
                searchByItems(geocoder, map, this.value);
            }
            var searchItems = [];
            $.each($("form#member-map-search-form input:checked"), function(){
                searchItems.push($(this).val());
            });
            // alert("Selected elements: " + searchItems.join(", "));
        });

        // My location
        infoWindow = new google.maps.InfoWindow({map: map});

        // console.log(navigator.userAgent.toLowerCase())
        chrome = /chrome/.test(navigator.userAgent.toLowerCase());
        // chrome = navigator.userAgent.toLowerCase().indexOf('chrom')
        console.log('is chrome: ' + chrome)
        console.log(location.hostname);
        console.log(document.domain);
        console.log(location.protocol)
        // window.location.protocol != "https:"
        // console.log("after me")
        // map = new google.maps.Map(document.getElementById('map'), {
        //   center: nyc,
        //   zoom: 13      // zoomed
        // });
        // var geocoder = new google.maps.Geocoder();
// alert("my address");
        geocodeAddress(geocoder, map, 'My Address');
// alert("members");
        addMemberAddresses(geocoder, map);
        if (!chrome || location.protocol == "https:" ||
          location.hostname == '127.0.0.1' || location.hostname == 'localhost') {
// alert("my location");
          getMyLocation(map, infoWindow);
        }

        // pinColor = "FE7569";

        /*infowindow = new google.maps.InfoWindow();
        var service = new google.maps.places.PlacesService(map);
        service.nearbySearch({
          location: pyrmont,
          radius: 500,
          type: ['store']
        }, callback);*/
      }


      // This function is used in the member detail pages.
      function initMemberMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: nyc,
          zoom: 13      // zoomed
        });
        var geocoder = new google.maps.Geocoder();
        infoWindow = new google.maps.InfoWindow({map: map});

        document.getElementById('submitNearby').addEventListener('click', function() {
          geocodeAddress(geocoder, map, 'Address');
          searchBoth(geocoder, map);
        });

        geocodeAddress(geocoder, map, 'My Address');
      }

      function getMyLocation(map, infoWindow) {
        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
// alert("found me");
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            // infoWindow.setPosition(pos);
            // infoWindow.setContent('Your current location.');
            map.setCenter(pos);
            // addMarker(pos);
            // var marker = new google.maps.Marker({
            //   map: map,
            //   position: pos,
            //   title: 'Me'
            // });
            addPerson(pos, 'Me', 'Me', 0)
            // console.log('Me' + people.length);
            // console.log('Me' + people[people.length-1]);
          }, function() {
// alert("location error");
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
// alert("browser error");
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
          searchTerm = null;
        }
        console.log(allMarkers);
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
        marker.setIcon('http://maps.google.com/mapfiles/ms/icons/lightblue.png')

        google.maps.event.addListener(marker, 'click', function() {
          infowindow.setContent(place.name);
          infowindow.open(map, this);
        });
        markers.push(marker);
        // console.log('searchTerm: ' + searchTerm)
        if (searchTerm == null) {
          allMarkers.default.push(marker);
        } else {
          if (!(searchTerm in allMarkers)) {
            allMarkers[searchTerm] = []
          }
          allMarkers[searchTerm].push(marker)
          marker.setIcon('http://maps.google.com/mapfiles/ms/icons/ltblue-dot.png')
        }
        // console.log(allMarkers);
      }

      // function createMarker(place) {
      //http://stackoverflow.com/questions/7095574/google-maps-api-3-custom-marker-color-for-default-dot-marker
      function addPerson(location, member_name, member_addr, membid, member_sex, member_alert) {
        var marker = new google.maps.Marker({
          map: map,
          position: location,
          title: member_name
        });
        // marker.setIcon('http://maps.google.com/mapfiles/ms/icons/green-dot.png')
        if (membid == 0 && member_name == 'Me') {
          marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue-dot.png')
        } else if (membid == 0) {
          marker.setIcon('http://maps.google.com/mapfiles/ms/icons/blue.png')
        } else if (member_alert == 'Alert'){
          if (member_sex == 'M') {
            marker.setIcon('/static/healthcare/img/icons/man-red.png')
          } else {
            marker.setIcon('/static/healthcare/img/icons/woman-red.png')
          }
        } else {
          if (member_sex == 'M') {
            marker.setIcon('/static/healthcare/img/icons/man-green.png')
          } else {
            marker.setIcon('/static/healthcare/img/icons/woman-green.png')
          }
        }
        // console.log(member_name, membid)
        var popup = member_name + ' ' + member_addr
        google.maps.event.addListener(marker, 'click', function() {
          // infoWindow.setContent('<a href= "http://127.0.0.1:8000/">'+member_addr+'</a>');
          // infoWindow.setContent('<a href= "{% url 'member_detail' pk=4 %}">'+member_addr+'</a>');
          $("#wid-member-map-search").removeClass("jarviswidget-collapsed")
              .children('div')
              .show();
          document.getElementById('address').value = member_addr;
          if (membid == 0 && member_name == 'Me') {
            infoWindow.setContent(popup);
          } else if (membid == 0) {
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
        // console.log('Addr:' + people.length);
        // console.log('Addr:' + people[people.length-1]);
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
// alert("geocode address:" + address);
        geocoder.geocode({'address': address}, function(results, status) {
          if (status === 'OK') {
// alert("ok:" + address);
            resultsMap.setCenter(results[0].geometry.location);
            // var marker = new google.maps.Marker({
            //   map: resultsMap,
            //   position: results[0].geometry.location,
            //   title: 'My Address'
            // });
            addPerson(results[0].geometry.location, title, address, 0)

//             infowindow = new google.maps.InfoWindow();
//             var service = new google.maps.places.PlacesService(resultsMap);
//             service.nearbySearch({
//               location: results[0].geometry.location,
//               radius: 500,
// //              type: ['store']
//               type: [document.getElementById('searchTerm').value]
//             }, callback);

          } else {
// alert("error:" + address + " " + status);
            alert('Geocode Address was not successful for the following reason: ' + status);
          }
        });

      }

      // need jdata because geocode is asynchronous
      var jdata = []
      function addMemberAddresses(geocoder, resultsMap) {
          var i = 0, j = 0
          var member_name, member_addr, member_id, member_alert, member_sex
          jdata = []
          $.getJSON("/provider_members/" + $person_id, {},
            function(json){
              // console.log(json);  // sanity check
              $.each(json, function (index, value) {
                  member_name = value.first_name + " " + value.last_name;
                  member_addr = value.address + ", " + value.state + " " + value.zip;
                  member_id = value.id;
                  member_alert = value.alert;
                  member_sex = value.sex;
                  // console.log(nm + addr);
                  jdata.push([member_name, member_addr, member_id, member_sex, member_alert]);
                  // console.log(jdata[i])
// alert("geocode member:" + member_addr);
                  geocoder.geocode({'address': member_addr}, function(results, status) {
                    if (status === 'OK') {
// alert("member:" + jdata[j][1]);
                      // console.log("--"+nm+j+results)
                      // console.log(j+"--"+jdata[j])
                      // resultsMap.setCenter(results[0].geometry.location);
                      // addPerson(results[0].geometry.location, member_name, member_name + " " + member_addr, member_id)
                      addPerson(results[0].geometry.location, jdata[j][0], jdata[j][1], jdata[j][2], jdata[j][3], jdata[j][4])
                      j++
                    } else {
// alert("member error:" + member_addr + " " + status);
                      alert('Geocode Member was not successful for the following reason: ' + status);
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
          var searchField = document.getElementById('searchType').value;
          if (status === 'OK') {

            resultsMap.setCenter(results[0].geometry.location);
            addPerson(results[0].geometry.location, address, address, 0)

            if (searchField != 'none') {

              deleteMarkers();

              // resultsMap.setCenter(results[0].geometry.location);
              // var marker = new google.maps.Marker({
              //   map: resultsMap,
              //   position: results[0].geometry.location
              // });

              infowindow = new google.maps.InfoWindow();

              var service = new google.maps.places.PlacesService(resultsMap);
              // alert('Search: ' + document.getElementById('searchType').value);
              var request = {
                location: results[0].geometry.location,
                radius: 500,
                type: [searchField]
                // type: ['hospital']
                // type: ['store']
                // valid types: https://developers.google.com/places/supported_types
              }
              searchTerm = searchField // have to have this twice since searchTerm gets reset by callback
              service.nearbySearch(request, callback);

              var request = {
                location: results[0].geometry.location,
                radius: 500,
                query: [searchField]
              }
              // searchTerm = searchField // have to have this twice since searchTerm gets reset by callback
              service.textSearch(request, callback);

              // setMapOnAll(resultsMap)
              showMarkers();
            }
          } else {
            alert('Geocode was not successful for the following reason: ' + status);
          }
        });

      }


      function searchByItems(geocoder, resultsMap, term) {
        var address = document.getElementById('address').value;
        geocoder.geocode({'address': address}, function(results, status) {
          // var searchField = document.getElementById('searchType').value;
          var searchField = term;
          // console.log('SearchField: ' + term)
          if (status === 'OK') {

            resultsMap.setCenter(results[0].geometry.location);
            // addPerson(results[0].geometry.location, address, address, 0)
            if (searchField != 'none') {

              deleteMarkers();
              // resultsMap.setCenter(results[0].geometry.location);
              // var marker = new google.maps.Marker({
              //   map: resultsMap,
              //   position: results[0].geometry.location
              // });
              infowindow = new google.maps.InfoWindow();
              var service = new google.maps.places.PlacesService(resultsMap);
              // alert('Search: ' + document.getElementById('searchType').value);
              // var request = {
              //   location: results[0].geometry.location,
              //   radius: 500,
              //   type: [searchField]
              //   // type: ['hospital']
              //   // valid types: https://developers.google.com/places/supported_types
              // }
              // searchTerm = searchField // have to have this twice since searchTerm gets reset by callback
              // service.nearbySearch(request, callback);

              var request = {
                location: results[0].geometry.location,
                radius: 500,
                query: [searchField]
              }
              searchTerm = searchField // have to have this twice since searchTerm gets reset by callback
              service.textSearch(request, callback);

              showMarkers();
            }
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
