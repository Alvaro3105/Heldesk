# Helpdesk API

API REST para gerenciamento de **usuários e chamados de suporte**, desenvolvida em Python com Flask, Flask-SQLAlchemy e SQLite.

O projeto foi desenvolvido como atividade acadêmica no **COTEMIG** para aplicar arquitetura em camadas, regras de negócio, persistência de dados e construção de endpoints REST.

## Principais recursos

- Cadastro, consulta, atualização e exclusão de usuários
- Cadastro, consulta, atualização e exclusão de chamados
- Associação de chamados a usuários
- Controle de prioridade dos chamados
- Fluxo de status: `Aberto -> Em atendimento -> Encerrado`
- Filtro de chamados abertos
- Filtro de chamados com prioridade alta
- Estatísticas gerais da API
- Validações e regras de negócio na camada de serviços
- Testes automatizados com `unittest`

## Arquitetura

O projeto utiliza separação em camadas:

```text
Helpdesk/
├── controllers/          # Rotas HTTP e respostas da API
│   ├── __init__.py
│   ├── chamado_controller.py
│   └── usuario_controller.py
├── models/               # Entidades e mapeamento do banco
│   ├── __init__.py
│   ├── chamado.py
│   └── usuario.py
├── repositories/         # Acesso e persistência dos dados
│   ├── __init__.py
│   ├── chamado_repository.py
│   └── usuario_repository.py
├── services/             # Regras de negócio e validações
│   ├── __init__.py
│   ├── chamado_service.py
│   └── usuario_service.py
├── instance/             # Banco SQLite criado localmente
│   └── .gitkeep
├── tests/
│   └── test_api.py
├── .gitignore
├── app.py
├── database.py
├── requirements.txt
└── README.md
```

### Fluxo de uma requisição

```text
Cliente -> Controller -> Service -> Repository -> Model / Banco de Dados
```

- **Controller:** recebe a requisição e devolve a resposta HTTP.
- **Service:** concentra validações e regras de negócio.
- **Repository:** realiza consultas e alterações no banco.
- **Model:** representa as tabelas e entidades da aplicação.

## Tecnologias

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- API REST
- Git / GitHub

## Regras de negócio

### Usuários

- Nome é obrigatório.
- E-mail é obrigatório e único.
- Um usuário que possui chamados cadastrados não pode ser excluído.

### Chamados

- Título deve possuir pelo menos 5 caracteres.
- Descrição deve possuir pelo menos 10 caracteres.
- Prioridade deve ser `Baixa`, `Média` ou `Alta`.
- Todo chamado deve pertencer a um usuário existente.
- O status inicial é sempre `Aberto`.
- As transições de status permitidas são:

```text
Aberto -> Em atendimento -> Encerrado
```

- Não é possível pular ou retroceder etapas de status.
- Cada usuário pode possuir no máximo 5 chamados de prioridade `Alta` que ainda não estejam encerrados.

## Endpoints

### Geral

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Verifica se a API está online |
| GET | `/estatisticas` | Retorna estatísticas gerais |

### Usuários

| Método | Rota | Descrição |
|---|---|---|
| GET | `/usuarios` | Lista usuários |
| GET | `/usuarios/<id>` | Busca um usuário por ID |
| POST | `/usuarios` | Cadastra um usuário |
| PUT | `/usuarios/<id>` | Atualiza um usuário |
| DELETE | `/usuarios/<id>` | Exclui um usuário sem chamados |
| GET | `/usuarios/<id>/chamados` | Lista os chamados do usuário |

### Chamados

| Método | Rota | Descrição |
|---|---|---|
| GET | `/chamados` | Lista chamados |
| GET | `/chamados/<id>` | Busca um chamado por ID |
| POST | `/chamados` | Cadastra um chamado |
| PUT | `/chamados/<id>` | Atualiza dados do chamado |
| DELETE | `/chamados/<id>` | Exclui um chamado |
| PATCH | `/chamados/<id>/iniciar` | Altera de Aberto para Em atendimento |
| PATCH | `/chamados/<id>/encerrar` | Altera de Em atendimento para Encerrado |
| GET | `/chamados/abertos` | Lista chamados abertos |
| GET | `/chamados/prioridade/alta` | Lista chamados de prioridade alta |

## Como executar

### 1. Clone o projeto

```bash
git clone https://github.com/Alvaro3105/Heldesk.git
cd Heldesk
```

> Depois que o repositório for renomeado para `Helpdesk`, utilize o novo endereço no comando acima.

### 2. Crie o ambiente virtual

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a API

```bash
python app.py
```

A aplicação ficará disponível em:

```text
http://127.0.0.1:5000
```

Na primeira execução, o banco SQLite é criado automaticamente em `instance/helpdesk.db`.

## Exemplos de requisição

### Criar usuário

```http
POST /usuarios
Content-Type: application/json
```

```json
{
  "nome": "Maria Silva",
  "email": "maria@empresa.com",
  "setor": "TI"
}
```

### Criar chamado

```http
POST /chamados
Content-Type: application/json
```

```json
{
  "titulo": "Impressora não funciona",
  "descricao": "A impressora do setor administrativo não liga.",
  "prioridade": "Alta",
  "usuario_id": 1
}
```

### Iniciar atendimento

```http
PATCH /chamados/1/iniciar
```

### Encerrar atendimento

```http
PATCH /chamados/1/encerrar
```

## Testes

O projeto possui testes automatizados usando a biblioteca padrão `unittest` e um banco SQLite em memória.

Execute:

```bash
python -m unittest discover -s tests -v
```

Os testes cobrem o fluxo principal da API, validações de chamado e o bloqueio da exclusão de usuários que possuem chamados.

## Códigos HTTP utilizados

- `200 OK` — consulta ou alteração realizada com sucesso
- `201 Created` — recurso criado
- `204 No Content` — recurso excluído
- `400 Bad Request` — dados inválidos ou regra de negócio violada
- `404 Not Found` — recurso inexistente
- `409 Conflict` — tentativa de excluir usuário que possui chamados

## Autor

**Álvaro Pires de Souza**

- GitHub: [Alvaro3105](https://github.com/Alvaro3105)
- LinkedIn: [alvaro-pires-de-souza](https://www.linkedin.com/in/alvaro-pires-de-souza/)
