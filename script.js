ENDPOINT = "http://localhost:5000";
var s;


reset = function () {
  graph.style = 'display: none;';
  result.innerHTML = '';
  barfill.style = 'width: 0px;';
  monitor.style = 'margin-top: 130px;';
}


submit = function() {
    text = document.getElementById('client_input').value;

  if (text == ''){
    result.style = 'color: #008DD5';
    result.innerHTML = 'Please Enter Text';
    return;
  }

    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("readystatechange", function () {
    if (this.readyState === 4) {
        response = this.responseText;
      s = response;
      console.log(s);
      s = s.replace('[', '');
      s = s.replace(']', '');
      s = s.replace('[', '');
      s = s.replace(']', '');
      console.log(s);
      s = s.split(' ');
      for (var i = 0; i < s.length; i++){
        s[i] = parseFloat(s[i]);
      }

      if (Math.abs(s[0]-s[1]) < 0.07){
        result.style = 'color: #008DD5';
        result.innerHTML = 'The model is unsure if this data is impartial';
      } else if (s[0] > s[1]){
        result.style = 'color: #008DD5';
        result.innerHTML = 'This text shows no sign of political bias.';
      } else {

        confidence = (s[1])/(s[1] + s[0]);
        percent.innerHTML = Math.round(confidence*100,1);
        monitor.style = 'margin-top: 20px;';
        graph.style = 'display: block;';
        result.style = 'color: #DE3C4B';
        result.innerHTML = 'You should be cautious about the impartiality of the source of this material.';

        setTimeout(function() {
          //console.log('width: ' + (bar.offsetWidth * confidence).toString() + 'px');
          barfill.style = 'width: ' + (bar.offsetWidth * confidence).toString() + 'px';
        }, 500);
        
      }



        /*if (response == '[1]'){
            result.style = 'color: #DE3C4B';
            result.innerHTML = 'You should be cautious about the impartiality of the source of this material.';
        } else if (response == '[0]'){
            result.style = 'color: #008DD5';
            result.innerHTML = 'This text shows no sign of political bias.';

        }

      console.log(response);*/

    }
  });
  xhttp.open("GET", ENDPOINT + "/?input=" + text, true);
  xhttp.send();
};