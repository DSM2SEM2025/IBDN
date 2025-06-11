import LoginForm from './componentes/LoginForm.js'; // Boa prática usar a extensão .js em imports de módulo no navegador

// 1. Encontrar o elemento principal da sua aplicação no DOM
const appContainer = document.getElementById('app');

// 2. Criar uma instância do seu componente de login
//    Nota: O construtor do seu LoginForm espera um 'fetchService'. 
//    Por enquanto, passaremos 'null' ou um objeto fetch genérico.
const loginForm = new LoginForm(null); 

// 3. Renderizar o HTML do componente dentro do container
appContainer.innerHTML = loginForm.render();

// 4. Chamar o método para adicionar os eventos (como o 'submit' do formulário)
loginForm.afterRender();