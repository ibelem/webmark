function checkResult() {
  var statuslink = document.querySelector('#status a').innerHTML;
  var scorespan = document.querySelector('#result-summary .score').innerHTML;
  if (statuslink == 'Test Again') {
    var score = scorespan.split('<span')[0];
    score = score.replace("'", "")
    return score;
  }
}

function startTests() {
  JetStream.start();
}