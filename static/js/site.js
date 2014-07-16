var ws = null;
function connect() {
    if (ws == null) {
      ws = new WebSocket('ws://127.0.0.1:8060/1');
        ws.onopen = function () {
              log('mikasa connected');
        };
        ws.onerror = function (error) {
              log(error);
        };
        ws.onmessage = function (e) {
              log('  ' + e.data);
        };
        ws.onclose = function () {
              log('mikasa disconnected');
              ws = null;
        };
    }
    else log('mikasa ws already connected');
    return false;
}

function disconnect() {
    if (ws != null) ws.close(); else log('mikasa already disconnected');
    return false;
}
function send() {
    if (ws === null) return log('please connect first');
      var text = document.getElementById('message').value;
      document.getElementById('message').value = "";
      ws.send(text);
      return false;
}
function log(text) {
    var li = document.createElement('li');
    li.appendChild(document.createTextNode(text));
    document.getElementById('log').appendChild(li);
    return false;
}
