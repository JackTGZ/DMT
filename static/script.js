function predict() {
    var form = document.getElementById('predictionForm');
    var formData = new FormData(form);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/predict', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');

    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            displayPrediction(response.prediction);
        }
    };

    xhr.send(new URLSearchParams(formData));
}

function displayPrediction(prediction) {
    var resultDiv = document.getElementById('predictionResult');
    resultDiv.innerHTML = prediction;
}
