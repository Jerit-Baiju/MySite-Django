document.getElementById("textid").value = "Clara: Hello " + user + "\n";

function scroll_down() {
  var textarea = document.getElementById("textid");
  textarea.scrollTop = textarea.scrollHeight;
}
function set(text) {
  inp = document.getElementById("input").value;
  old = document.getElementById("textid").value;
  document.getElementById("textid").value =
    old + "You: " + inp + "\n" + "Clara: " + text + "\n\n";
  document.getElementById("input").value = "";
}

async function send() {
  main = document.getElementById("input").value;
  main = main.toLowerCase();
  
  if (main===''){
  	set('please type something')
  }
  else{
  var url = "http://elio-bot.herokuapp.com/api/clara/"+user+"/"+main;
	await fetch(url)
  .then(response => response.json())
  .then(data => set(data))
  .then(scroll_down())

  }
  
  scroll_down();
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#input").addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      send();
    }
  });
});
