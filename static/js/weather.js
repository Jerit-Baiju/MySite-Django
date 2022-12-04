async function getData(city){
    url = 'http://192.168.43.21:5000/api/weather/' + city
  	const response = await fetch(url);
  	var data = await response.json();
  	var image = '<img id="image" src="'+ data["image_url"] +'" alt="weather_image" srcset="" />'
  	
  	$("#bar").show()
  	$("#context").empty()
  	var location = "<h4>"+ data["temp"] +"</h4>"
  	$("#context").append(location)
  	$("#image_holder").empty()
		$("#image_holder").append(image)

  	
}
$(document).ready(function () {
    $("#submit_btn").click(function () {
        city = document.getElementById("city_name").value
        getData(city)
        
    })
    $("#bar").hide()
})
