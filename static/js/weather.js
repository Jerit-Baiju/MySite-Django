async function getData(){
    alert(city)
    url = 'https://192.168.43.21:5000/api/weather/' + city
    await fetch(url).then((response) => response.json()).then((data) => alert(data))
    alert(response)
}
$(document).ready(function () {
    $("#submit_btn").click(function () {
        city = document.getElementById("city_name").value
        getData()
        
    })
    // $("#bar").hide()
    // $("#image").hide()
})