const $labelcheckt = document.querySelector('#escadatipot');
const $labelchecke = document.querySelector('#escadatipoe');

$labelcheck.addEventListener('change', function(){

    if ($labelcheckt.checked == true){
        document.getElementById("imga").src="static/img/img2.jpg";
    } else {
        if ($labelchecke.checked == true){
            document.getElementById("imgb").src="static/img/img1.jpg";
        } else {
            document.getElementById("imga").src="static/img/img2.jpg";
        }
    }

})


