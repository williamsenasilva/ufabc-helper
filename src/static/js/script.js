$(document).ready(function() {
    console.log("ready!");
});

function atualizarDisciplina(codigo,ano,periodo) {
    var data = {};
    conceito = $('#select-conceito-'+codigo+'-'+ano+'-'+periodo).val();
    data['codigo'] = codigo.toString();
    data['ano'] = parseInt(ano);
    data['periodo'] = periodo.toString();
    data['conceito'] = conceito.toString();
    console.log(data);
    $.ajax({
        type: 'POST',
        url: "/ficha/atualizar/disciplina/",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(resultData) {
            console.log("sucesso");
            window.location.reload();
        },
        error: function(resultData) {
            console.log("erro");
        }
    });
}

function inserirDisciplina() {
    var data = {};
    data['nome'] = $('#input-nome').val();
    data['codigo'] = $('#input-codigo').val();
    data['ano'] = parseInt($('#input-ano').val());
    data['periodo'] = $('#select-periodo').val();
    data['categoria'] = $('#select-categoria').val();
    data['creditos'] = parseInt($('#select-creditos').val());
    data['conceito'] = $('#select-conceito').val();
    console.log(data);
    $.ajax({
        type: 'POST',
        url: "/ficha/inserir/disciplina/",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(resultData) {
            console.log("sucesso");
            window.location.reload();
        },
        error: function(resultData) {
            console.log("erro");
        }
    });
}