function checkResult() {
  var score = document.querySelector('#results .score').innerHTML;
  var button = document.querySelector('#results button').innerHTML;
  if (score != null && button == 'Test Again')
    return score;
}

function startTests() {
  benchmarkController.startBenchmark();
}