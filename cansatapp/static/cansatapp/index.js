let timerInSeconds = 0;

console.log("hey");
setInterval(() => {
  timerInSeconds += 1;

  if (timerInSeconds >= 2) {
    window.location.reload();
  }
}, 3000); 
