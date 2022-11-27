async function getData(){
    alert(city)
    url = 'https://jerit.herokuapp.com/api/weather/' + city
    await fetch(url).then((response) => response.json()).then((data) => alert(data))
    alert(response)
}
$(document).ready(function () {
    $("#submit_btn").click(function () {
        city = document.getElementById("city_name").value
        if (city != ""){
            getData()
        }
        else{
            Swal.fire ({
                icon: 'warning',
                title: 'title',
                text: 'text',
            })
        }
        
    })
    // $("#bar").hide()
    // $("#image").hide()
})