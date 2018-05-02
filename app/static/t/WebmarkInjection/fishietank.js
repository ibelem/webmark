function checkResult() {
  var scoreE = document.querySelector('#fpsCanvas');
  score = scoreE.getAttribute('title');
  score = score.replace('Demo is running at', '').replace('FPS', '').replace(/\s+/g, "");
  console.log(score)
  return score;
}

function startTests() {
  var rasc = document.querySelector('#ReturnAndShareControls');
  rasc.setAttribute('style', 'display:none');

  var controls = document.querySelectorAll('a.control');
  for (var i of controls) {
    if (i.innerHTML == '9000') {
      i.click();
    }
  }
}