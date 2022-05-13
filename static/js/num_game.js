chance = 0;
  random = Math.floor(Math.random() * 101)
  document.getElementById("img").style.display = "none";
  document.getElementById("new").style.display = "none";

  function win() {
    document.getElementById("img").style.display = "unset";
    document.getElementById("new").style.display = "unset";
    document.getElementById("inp").style.display = "none";
  }

  function newGame() {
    document.getElementById("new").style.display = "none";
  }

  function set(text) {
    document.getElementById("textarea").innerHTML = text;
    document.getElementById("guess").value = ''
  }

  function check() {
    chance = chance + 1;
    guess = document.getElementById("guess").value;
    if (chance == 10) {
      alert("Game Over");
      window.location = "/projects/num_game";
    }
    if (guess == random) {
      win();
    } if (guess < random) {
      set("The number is greater than guess (" + guess + ")");
    } if (guess > random) {
      set("The number is less than guess (" + guess + ")");
    }
  }