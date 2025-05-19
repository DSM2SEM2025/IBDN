const formCadastro = document.getElementById('form-cadastro')

formCadastro.addEventListener('submit', evento =>{
    evento.preventDefault();

    const FormData = new FormData(formCadastro);
    const data = Object.fromEntries(FormData);

    //Precisa arrumar o endereço
    fetch('#', {
        method: 'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body: JSON.stringify(data)

    })
    .then(res => res.json())
    .then(data => console.log(data))
});