$(document).ready(function(){
    $("#yt_get").click(function(){
        $.ajax({
            url: "/projects"
        })
    })
})