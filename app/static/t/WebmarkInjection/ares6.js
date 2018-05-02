function checkResult() {
  var score = document.querySelector('#Geomean span.value').innerHTML;
  var status = document.querySelector('#status').innerHTML;
  if (score != '∅' && status == 'Restart') {
    return score;
  }
}

function startTests() {
  var trigger = document.querySelector('#trigger');
  trigger.click();
}