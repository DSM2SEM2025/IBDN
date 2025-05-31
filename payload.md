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
