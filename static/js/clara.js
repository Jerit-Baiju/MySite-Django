document.getElementById("textid").value = "Clara: Hello " + user + "\n";

function scroll_down() {
  var textarea = document.getElementById("textid");
  textarea.scrollTop = textarea.scrollHeight;
}
function set(text) {
  inp = document.getElementById("input").value;
  old = document.getElementById("textid").value;
  document.getElementById("textid").value =
    old + "You: " + inp + "\n" + "Clara: " + text + "\n";
  document.getElementById("input").value = "";
}
function send() {
  main = document.getElementById("input").value;
  main = main.toLowerCase();
  op = await fetch('https://elio-bot.herokuapp.com/api/'+user+'/'+main)
  alert(op)
  op = await op.json()
  alert(op)
  set(op);
  scroll_down();
}
document.addEventListener("DOMContentLoaded", () => {
  document.querySelector("#input").addEventListener("keydown", function (e) {
    if (e.code === "Enter") {
      send();
    }
  });
});
