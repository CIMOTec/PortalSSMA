// -------------------------------------------- Correios -----------------------------------------------

function meu_callbackR(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('floatEnderecoR').value = (conteudo.logradouro);
        document.getElementById('floatBairroR').value = (conteudo.bairro);
        document.getElementById('floatCidadeR').value = (conteudo.localidade);
        document.getElementById('floatEstadoR').value = (conteudo.uf);
    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cep(letra);
        alert("CEP não encontrado.");
    }
}

function meu_callbackD(conteudo) {
    if (!("erro" in conteudo)) {
        //Atualiza os campos com os valores.
        document.getElementById('floatEnderecoD').value = (conteudo.logradouro);
        document.getElementById('floatBairroD').value = (conteudo.bairro);
        document.getElementById('floatCidadeD').value = (conteudo.localidade);
        document.getElementById('floatEstadoD').value = (conteudo.uf);
    } //end if.
    else {
        //CEP não Encontrado.
        limpa_formulário_cep(letra);
        alert("CEP não encontrado.");
    }
}

function pesquisacep(valor, letra) {

    //Nova variável "cep" somente com dígitos.
    var cep = valor.replace(/\D/g, '');

    //Verifica se campo cep possui valor informado.
    if (cep != "") {

        //Expressão regular para validar o CEP.
        var validacep = /^[0-9]{8}$/;

        //Valida o formato do CEP.
        if (validacep.test(cep)) {

            //Preenche os campos com "..." enquanto consulta webservice.
            document.getElementById('floatEndereco' + letra).value = "...";
            document.getElementById('floatBairro' + letra).value = "...";
            document.getElementById('floatCidade' + letra).value = "...";
            document.getElementById('floatEstado' + letra).value = "...";

            //Cria um elemento javascript.
            var script = document.createElement('script');
            //Sincroniza com o callback.

            if (letra == 'R') {
                script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callbackR';

                //Insere script no documento e carrega o conteúdo.
                document.body.appendChild(script);
            }
            else {
                script.src = 'https://viacep.com.br/ws/' + cep + '/json/?callback=meu_callbackD';

                //Insere script no documento e carrega o conteúdo.
                document.body.appendChild(script);
            }
        } //end if.
        else {
            //cep é inválido.
            limpa_formulário_cep();
            alert("Formato de CEP inválido.");
        }
    } //end if.
    else {
        //cep sem valor, limpa formulário.
        limpa_formulário_cep();
    }
};

// --------------------------------------Peso-----------------------------------------------

function peso(valor) {

    if (valor > 30) {
        document.getElementById("floatEmpresaColeta").value = ("Transportadora");
    } else {
        document.getElementById("floatEmpresaColeta").value = ("Correios");
    }
};

window.onload = function () {
    var dropdown = document.createElement("select");
    dropdown.classList.add('form__input');
    dropdown.setAttribute("id", "floatMarca");
    dropdown.setAttribute("name", "MARCA|00");
    dropdown.setAttribute("class", "form-select");
    dropdown.setAttribute("aria-label", ".form-select-lg example");

    fetch("static/config.json")
        .then(response => response.json())
        .then(data => {
            for (var i = 0; data.productBrandName[i]; i++) {
                console.log(data.productBrandName[i]);
                var opt = document.createElement("option");
                opt.text = data.productBrandName[i];
                opt.value = data.productBrandName[i];
                dropdown.options.add(opt);
            }
        })
    var dvContainer = document.getElementById("dropdown-container");
    dvContainer.appendChild(dropdown);

    var datalist = document.createElement("datalist");
    datalist.setAttribute("id", "search");
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