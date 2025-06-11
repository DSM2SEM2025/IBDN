export default class CadastroForm {
    constructor(fetchService) {
        this.fetchService = fetchService;
    }

    render() {
        return `
            <div class="cadastro-container">
                <h2>Criar Conta</h2>
                <form id="form-cadastro">
                    <div class="cadastro-input-group">
                        <input type="text" id="cadastroRazaoSocial" name="razao-social" placeholder="DIGITE A RAZÃO SOCIAL" required>
                    </div>

                    <div class="cadastro-input-group">
                        <input type="text" id="cadastroNomeFantasia" name="nome-fantasia" placeholder="DIGITE FANTASIA" required>
                    </div>

                    <div class="cadastro-input-group">
                        <input type="text" id="cadastroCNPJ" name="CNPJ" placeholder="DIGITE O CNPJ" required>
                    </div>

                    <div class="cadastro-input-group">
                        <input type="email" id="cadastroEmail" name="email" placeholder="DIGITE O EMAIL" required>
                    </div>
                    
                    <div class="cadastro-input-group">
                        <input type="tel" id="cadastroTelefone" name="telefone" placeholder="DIGITE TELEFONE" pattern="\\d*" inputmode="numeric">
                    </div>

                    <div class="cadastro-input-group">
                        <select id="cadastroTipoEmpresa" name="tipo-empresa" required>
                            <option value="" disabled selected hidden>SELECIONAR TIPO DE EMPRESA</option>
                            <option value="comercio">COMÉRCIO</option>
                            <option value="servico">PRESTADOR DE SERVIÇO</option>
                            <option value="industria">INDÚSTRIA</option>
                            <option value="agropecuaria">AGROPECUÁRIA</option>
                            <option value="outros">OUTROS</option>
                        </select>
                    </div>

                    <div class="cadastro-input-group">
                        <input type="password" id="cadastroSenha" name="senha" placeholder="DIGITE UMA SENHA" required>
                    </div>

                    <div class="cadastro-input-group">
                        <input type="password" id="cadastroConfirmarSenha" name="confirme-senha" placeholder="CONFIRME A SENHA" required>
                    </div>

                    <button type="submit" class="cadastro-botao">Enviar</button>
                </form>
            </div>
        `;
    }

    afterRender() {
        document.getElementById('form-cadastro').addEventListener('submit', (e) => this.cadastrar(e));
    }

    async cadastrar(event) {
        event.preventDefault();

        const razaoSocial = document.getElementById('cadastroRazaoSocial').value;
        const nomeFantasia = document.getElementById('cadastroNomeFantasia').value;
        const cnpj = document.getElementById('cadastroCNPJ').value;
        const email = document.getElementById('cadastroEmail').value;
        const telefone = document.getElementById('cadastroTelefone').value;
        const tipoEmpresa = document.getElementById('cadastroTipoEmpresa').value;
        const senha = document.getElementById('cadastroSenha').value;
        const confirmarSenha = document.getElementById('cadastroConfirmarSenha').value;

        if (!razaoSocial || !nomeFantasia || !cnpj || !email || !senha || !confirmarSenha || !tipoEmpresa) {
            alert('Por favor, preencha todos os campos obrigatórios.');
            return;
        }

        if (senha !== confirmarSenha) {
            alert('As senhas não coincidem.');
            return;
        }

        try {
            const response = await this.fetchService.fetch('/cadastro', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    razaoSocial,
                    nomeFantasia,
                    cnpj,
                    email,
                    telefone,
                    tipoEmpresa,
                    senha
                })
            });

            if (response) {
                alert('Cadastro realizado com sucesso!');
                location.hash = '#';
            } else {
                alert('Erro no cadastro: ' + (response.message || 'Erro desconhecido'));
            }
        } catch (error) {
            alert('Erro ao tentar cadastrar: ' + error.message);
        }
    }
}
