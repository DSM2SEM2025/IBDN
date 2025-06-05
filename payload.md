# Documentação de Testes de Rotas

## Ramo ( /ramos )
### GET /ramos/
- Descrição: Lista todos os ramos cadastrados.
- Body: Não requer.
- Response exemplo:

```json
[
  {
    "id": 1,
    "nome": "Tecnologia",
    "descricao": "Empresas de desenvolvimento de software"
  },
  {
    "id": 2,
    "nome": "Alimentício",
    "descricao": "Indústrias e comércio de alimentos"
  }
]
```


### GET /ramos/{id}
- Descrição: Retorna um ramo específico.
- Body: Não requer.
- Response exemplo:

```json
{
  "id": 1,
  "nome": "Tecnologia",
  "descricao": "Empresas de desenvolvimento de software"
}
```

### POST /ramos/
- Descrição: Cria um novo ramo.
- Request Body exemplo:

```json
{
  "nome": "Educação",
  "descricao": "Empresas da área educacional e ensino"
}
```
- Response exemplo:

```json
{
  "id": 3,
  "nome": "Educação",
  "descricao": "Empresas da área educacional e ensino"
}
```

### PUT /ramos/{id}
- Descrição: Atualiza um ramo existente.
- Request Body exemplo:

```json
{
  "nome": "Tecnologia da Informação",
  "descricao": "Empresas focadas em TI, desenvolvimento e inovação"
}
```

- Response exemplo:
```json
{
  "id": 1,
  "nome": "Tecnologia da Informação",
  "descricao": "Empresas focadas em TI, desenvolvimento e inovação"
}
```

### DELETE /ramos/{id}
- Descrição: Remove um ramo do sistema.
- Body: Não requer.
- Response: 204 No Content (Sem retorno).

## Empresa x Ramo ( /empresas/{id_empresa}/ramos/ )

### POST /empresas/{id_empresa}/ramos/
- Descrição: Associa um ou mais ramos a uma empresa.
- Request Body exemplo:

```json
{
  "ids_ramos": [1, 3]
}
```
- Response exemplo:

```json
[
  {
    "id": 1,
    "id_empresa": 10,
    "id_ramo": 1
  },
  {
    "id": 2,
    "id_empresa": 10,
    "id_ramo": 3
  }
]
```

### DELETE /empresas/{id_empresa}/ramos/{id_ramo}
- Descrição: Remove a associação de um ramo de uma empresa.
- Body: Não requer.
- Response: 204 No Content (Sem retorno).

### GET /empresas/{id_empresa}/ramos/
- Descrição: Lista todos os ramos associados a uma empresa.
- Body: Não requer.
- Response exemplo:

```json
[
  {
    "id": 1,
    "nome": "Tecnologia",
    "descricao": "Empresas de desenvolvimento de software"
  },
  {
    "id": 3,
    "nome": "Educação",
    "descricao": "Empresas da área educacional e ensino"
  }
]
```

---
---

## Empresa ( /empresas )

### DELETE /empresas/
- Descrição: Realiza a exclusão lógica de uma empresa. Requer autenticação. A permissão varia conforme o perfil: ADM pode excluir qualquer empresa (informando o ID no corpo), Cliente pode excluir apenas a sua própria (sem informar ID no corpo).
- Request Body exemplo (para ADM):

```json
{
  "empresa_id": 2
}
```
- Response exemplo (Sucesso 200 OK):

```json
{
  "message": "Empresa excluída com sucesso."
}
```
- Response exemplo (Erro 404 Not Found):

```json
{
  "detail": "Empresa com ID 999 não encontrada ou já está inativa."
}
```
- Response exemplo (Erro 403 Forbidden):

```json
{
  "detail": "Clientes não podem especificar um 'empresa_id'."
}
```
- Response exemplo (Erro 400 Bad Request):

```json
{
  "detail": "O campo 'empresa_id' é obrigatório para administradores."
}
```

---

## Estruturas Globais

### Estrutura do Payload do Token JWT
- Descrição: Conteúdo encontrado dentro do token JWT decodificado, usado pelo backend para identificar o usuário e suas permissões.

- **Exemplo de Token de Administrador:**
```json
{
  "email": "admin@sistema.com",
  "tipo_usuario": "ADM",
  "empresa_id": null,
  "iat": 1728134400,
  "exp": 1728220800
}
```
- **Exemplo de Token de Cliente:**
```json
{
  "email": "ana.silva@example.com",
  "tipo_usuario": "Cliente",
  "empresa_id": 1,
  "iat": 1728134450,
  "exp": 1728220850
}
```

### Estrutura Padrão de Respostas de Erro
- Descrição: As respostas de erro da API (4xx) geralmente seguem este formato padrão com a chave `detail`.

- **Exemplo Genérico:**
```json
{
  "detail": "Mensagem descritiva do erro ocorrido."
}
```