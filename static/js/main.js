function updatePlot() {
    var variableSelect = document.getElementById('variable');
    var selectedVariable = variableSelect.value;
    var descriptionContainer = document.getElementById('variableDescription');

    console.log('Selected Variable:', selectedVariable);

    var variableDescription = getVariableDescription(selectedVariable);
    console.log('Variable Description:', variableDescription);

    if (descriptionContainer) {
        descriptionContainer.textContent = variableDescription;
    } else {
        console.error("Elemen dengan ID 'variableDescription' tidak ditemukan.");
    }

    fetch(`/get_variable_description?variable=${selectedVariable}`)
        .then(response => response.text())
        .then(data => {
            if (descriptionContainer) {
                descriptionContainer.textContent = data;
            } else {
                console.error("Elemen dengan ID 'variableDescription' tidak ditemukan.");
            }
        })
        .catch(error => console.error('Error fetching variable description:', error));
}

function loadVariableDescription(variable) {
    var descriptionContainer = document.getElementById('variableDescription');

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_variable_description?variable=' + variable, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            var variableDescription = xhr.responseText;

            // Periksa apakah elemen dengan ID 'variableDescription' ditemukan
            if (descriptionContainer) {
                descriptionContainer.textContent = variableDescription;
            } else {
                console.error("Elemen dengan ID 'variableDescription' tidak ditemukan.");
            }
        }
    };
    xhr.send();
}