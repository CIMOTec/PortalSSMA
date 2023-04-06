window.onload = function populateTable(){

  fetch("static/config_dash.json")
    .then(responseList => responseList.json())
    .then(data => {
      for(var i=0; data.solic[i] ; i++){
        let table = document.getElementById("tableSolics");
        let row = table.insertRow(1);
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);

        cell1.innerHTML = data.solic[i];
        cell2.innerHTML = data.Tipo[i];
        cell3.innerHTML = data.Data[i];
        cell4.innerHTML = data.Estado[i];

      }
    })
}