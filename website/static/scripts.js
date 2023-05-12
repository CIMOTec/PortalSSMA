window.onload = function () {
    var datalist = document.createElement("datalist");
    datalist.setAttribute("id", "search");
    datalist.className = "datalist";
    fetch("static/config_proj.json")
        .then(responseList => responseList.json())
        .then(data => {
            for (var i = 0; data.Name[i]; i++) {
                var opt = document.createElement("option");
                opt.text = data.Name[i];
                opt.value = data.Code[i];
                datalist.appendChild(opt);
            }
        })
    var datalistContainer = document.getElementById("datalist-container");
    datalistContainer.appendChild(datalist);
}