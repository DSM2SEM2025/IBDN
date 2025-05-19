const formLogin = document.getElementById('form-login')

formLogin.addEventListener('submit', evento =>{
    evento.preventDefault();

    const FormData = new FormData(formLogin);
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