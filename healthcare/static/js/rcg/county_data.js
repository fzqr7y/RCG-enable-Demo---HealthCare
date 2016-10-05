// SC: this outer function is not required
// $(function() {


// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Submit post on submit
$('#countydata-form').on('submit', function(event){
    // event.preventDefault();
    // alert("form submitted!");
    console.log("form submitted!");  // sanity check
    // get_counties();
});

// Submit post on submit
$('#id_state').change(function(){
    console.log("state: " + this.value);
    get_counties();
});

// AJAX for posting
function get_counties() {
    console.log("get_counties is working!") // sanity check
    console.log($('#id_state').val())

    $.ajax({
        url : "/county_lookup/", // the endpoint
        type : "POST", // http method
        data : { 'state' : $('#id_state').val() }, // data sent with the post request
        dataType: 'json',
        success : function(json) {
            // console.log(json); // log the returned json to the console
            // $("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+"</span></li>");
            // $("#id_county").prepend("<li><strong>"+json.text+"</strong> - <em> "+json.author+"</em> - <span> "+json.created+"</span></li>");
            // $("#id_county").val(json);
            // $("#id_county").html("");
            // for(key in json)
            //     $("#fillME").append("<option value='"+json[key].value+"'>"+json[key].title+"</option>");
            //      console.log("success"); // another sanity check
            // $("#state").prepend($("<option></option>")
            //             .attr("value", "").text("Please Select a State"))
            var $el = $("#id_county");
            $el.empty(); // remove old options
            $el.append($("<option></option>")
                    .attr("value", '').text('Please Select'));
            $.each(json, function(value, key) {
                // console.log('key: ' + key + ' value: ' + value)
                $el.append($("<option></option>")
                        .attr("value", key).text(key));
            });
        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

};

// AJAX for posting
function get_counties2() {
    console.log("get_counties2 is working!") // sanity check
    console.log($('#id_state').val())

    $.getJSON("/county_lookup/", {
            state: $('#id_state').val() },
        function(json){
            $.each(json, function (index, value) {
console.log(index + " - " + value)
                    // queryData.push([t, val]);
            });
    });
};
