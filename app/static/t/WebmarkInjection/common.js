var urlParam = function(name) {
  var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
  if (results == null) {
    return null;
  } else {
    return decodeURI(results[1]) || 0;
  }
}

var score;
var sendScore = function() {
  var obj = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Authorization': 'Basic ' + btoa(urlParam('t') + ':')
    },
    body: JSON.stringify({
      'author_id': urlParam('u'),
      'score_id': urlParam('sid'),
      'score': checkResult(),
      'webmark_id': urlParam('w'),
      'cpu': urlParam('cpu') || '',
    })
  }

  fetch(location.protocol + '//' + location.host + '/api/v1/scoresfinal/', obj).then(function(res) {
    console.log(res)
    var json = res.json();
    json.then(function(value) {
      console.log(JSON.stringify(value))
    }, function(error) {
      console.log(error);
    });
  }).catch(function(e) {
    console.log(e);
  });
}

function runTest() {
  startTests();
  const timeId = setInterval(() => {
    console.log(checkResult())
    if (checkResult()) {
      console.log(checkResult());
      sendScore();
      clearInterval(timeId);
      setTimeout(function() {
        var backurl = location.protocol + '//' + location.host + '/view-browser/';
        location.href = backurl;
      }, 5000);
    };
  }, 2000)
}

window.addEventListener('load', runTest, false);