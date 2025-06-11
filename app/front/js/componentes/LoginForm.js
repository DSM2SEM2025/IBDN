export default class LoginForm {
    constructor(fetchService) {
        this.fetchService = fetchService;
    }

    render() {
        return `
            <div class="login-container">
                <h2>Login</h2>
                <form id="form-login">
                    <div class="login-input-group">
                        <input type="email" id="loginEmail" name="email" placeholder="DIGITE SEU EMAIL" required>
                    </div>
                    
                    <div class="login-input-group">
                        <input type="password" id="loginSenha" name="senha" placeholder="DIGITE SUA SENHA" required>
                    </div>


                    <button type="submit" class="login-botao">Entrar</button>

                    <div class="login-link-registro">
                        <p> A empresa não possui conta? <a href="#cadastro"> Criar conta</a></p>
                    </div>
                </form>
            </div>
        `;
    }

    afterRender() {
        document.getElementById('form-login').addEventListener('submit', (e) => this.login(e));
    }

    async login(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const senha = document.getElementById('loginSenha').value;

        if (!email || !senha) {
            alert('Por favor, preencha todos os campos');
            return;
        }

        try {
            const response = await this.fetchService.fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, senha })
            });

            if (response) {
                localStorage.setItem('token', response.token);
                alert('Login realizado com sucesso!');
                location.hash = '#';
            } else {
                alert('Erro no login: ' + (response.message || 'Credenciais inválidas'));
            }
        } catch (error) {
            alert('Erro ao tentar fazer login: ' + error.message);
        }
    }
}
