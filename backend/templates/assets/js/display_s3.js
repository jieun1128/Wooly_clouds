var request = new XMLHttpRequest();
    request.open('GET', "./test.json");

    request.responseType = 'json';
    request.send();

    request.onload = function () {
      var jsonfile = request.response;
      populateHeader(jsonfile);
    }

function populateHeader(jsonfile) {
	var s3 = document.getElementById('s3-info');
	var s3_element = document.createElement('h2');
	var s3_id = document.createElement('p');
	for(var i = 0; i < jsonfile.length; i++){
		if(jsonfile[i].element == 's3') {
			var data_element = jsonfile[i].element;
			var data_id = jsonfile[i].id;
		}
	}
	s3_element.textContent = data_element;
	s3_id.textContent = data_id;
	s3.appendChild(s3_element);
	s3.appendChild(s3_id);
}