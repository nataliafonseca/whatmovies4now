document.getElementById('input-value').addEventListener('change', function (){
    var idUsuario = parseInt(document.getElementById('input-value').value)
    if (idUsuario !== "" &&  idUsuario >= 1 && idUsuario <= 610){
        document.getElementById('btn-submit').href = "recommend/"+idUsuario
    } else {
        alert("ID de usuário inválido")
    }
})
