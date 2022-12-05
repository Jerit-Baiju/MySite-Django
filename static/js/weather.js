async function getData(city){
    var url = 'https://jeritbaiju.pythonanywhere.com/api/weather/' + city
  	const response = await fetch(url);
  	var data = await response.json();
  	var location = "<h4>"+ data["location"] +"</h4>"
  	var time = "<h4>"+ data["time"] +"</h4>"
  	var status = "<h4>"+ data["status"] +"</h4>"
  	var temperature = "<h2>"+ data["temp"] +"</h2>"
  	var image = '<img id="image" src="'+ data["image_url"] +'" alt="weather_image" srcset="" />'
  	$("#bar").show()
  	$("#context").empty()
  	$("#temperature").empty()
  	$("#image_holder").empty()
  	$("#context").append(location)
  	$("#context").append(time)
  	$("#context").append(status)
  	$("#temperature").append(temperature)
	$("#image_holder").append(image)
}
function get(){
	$("#bar").hide()
	city = document.getElementById("city_name").value
	if (city != ''){
		$("#city_name").val('')
		getData(city)
	}
	
}
$(document).ready(function () {
    $("#submit_btn").click(function () {
		get()
    })
	$("#city_name").change(function (){
		get()
	})
    $("#bar").hide()
})
