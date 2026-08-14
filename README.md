# Helpdesk API

API REST para gerenciamento de chamados de suporte, construída em **Flask +
SQLAlchemy + SQLite**, seguindo arquitetura em camadas:

```
helpdesk/
├── controllers/     # recebe requisições HTTP e devolve respostas
├── services/        # regras de negócio
├── repositories/     # acesso ao banco (SQLAlchemy)
├── models/           # entidades (tabelas)
├── database.py       # instância central do SQLAlchemy
└── app.py            # cria a aplicação Flask e registra as rotas
```

## Como executar

```bash
python3 -m venv venv
source venv/bin/activate   

pip install -r requirements.txt

python app.py
```

O servidor sobe em `http://127.0.0.1:5000`. Na primeira execução, o
SQLAlchemy cria automaticamente o arquivo `instance/helpdesk.db` com as
tabelas `usuarios` e `chamados`.

## Endpoints

### Usuários
| Método | Rota                         | Descrição                          |
|--------|------------------------------|-------------------------------------|
| GET    | `/usuarios`                  | Lista todos os usuários             |
| POST   | `/usuarios`                  | Cria um usuário                     |
| PUT    | `/usuarios/<id>`             | Atualiza um usuário                 |
| DELETE | `/usuarios/<id>`             | Exclui um usuário (se não tiver chamados) |
| GET    | `/usuarios/<id>/chamados`    | Lista os chamados de um usuário     |

### Chamados
| Método | Rota                            | Descrição                              |
|--------|----------------------------------|-----------------------------------------|
| GET    | `/chamados`                      | Lista todos os chamados                 |
| POST   | `/chamados`                      | Cria um chamado (status inicial "Aberto")|
| PUT    | `/chamados/<id>`                 | Atualiza título/descrição/prioridade/técnico |
| DELETE | `/chamados/<id>`                 | Exclui um chamado                       |
| PATCH  | `/chamados/<id>/iniciar`         | Aberto → Em atendimento                 |
| PATCH  | `/chamados/<id>/encerrar`        | Em atendimento → Encerrado              |
| GET    | `/chamados/abertos`              | Lista apenas chamados com status Aberto |
| GET    | `/chamados/prioridade/alta`      | Lista chamados de prioridade Alta       |
| GET    | `/estatisticas`                  | Retorna contagens gerais do sistema     |

## Exemplos de uso (curl)

```bash
curl -X POST http://127.0.0.1:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"Maria Silva","email":"maria@empresa.com","setor":"TI"}'

curl -X POST http://127.0.0.1:5000/chamados \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Impressora não funciona","descricao":"A impressora do setor não liga","prioridade":"Alta","usuario_id":1}'

curl -X PATCH http://127.0.0.1:5000/chamados/1/iniciar

curl -X PATCH http://127.0.0.1:5000/chamados/1/encerrar

curl http://127.0.0.1:5000/estatisticas
```

## Regras de negócio implementadas

**Usuários**
- Nome e e-mail são obrigatórios.
- Não é permitido cadastrar dois usuários com o mesmo e-mail.
- Não é permitido excluir um usuário que possua chamados cadastrados.

**Chamados**
- Título obrigatório, mínimo de 5 caracteres.
- Descrição obrigatória, mínimo de 10 caracteres.
- Prioridade só pode ser `Baixa`, `Média` ou `Alta`.
- Todo chamado deve pertencer a um usuário existente.
- Status inicial sempre `Aberto`.
- Transições de status permitidas apenas: `Aberto → Em atendimento → Encerrado`
  (não é possível pular etapas nem retroceder).

**Observação sobre uma regra ambígua do enunciado:** o texto original diz
*"Um usuário não pode possuir mais de cinco chamados com prioridade que
ainda não estejam encerrados"*, sem especificar qual prioridade (provável
perda de texto na cópia/exportação do enunciado). Implementamos essa regra
para a prioridade **Alta**, por ser a única que faz sentido limitar na
prática — veja a constante `PRIORIDADE_LIMITADA` em
`services/chamado_service.py`. Se o professor quis dizer outra coisa
(ex.: limite geral de 5 chamados não encerrados, independente da
prioridade), basta ajustar essa constante e o método
`contar_nao_encerrados_por_prioridade`.

## Testes manuais já realizados
O fluxo completo foi validado manualmente antes da entrega: criação de
usuário e chamado, bloqueio de e-mail duplicado, bloqueio de título curto,
transição válida de status, bloqueio de transição inválida (reabrir
chamado encerrado), bloqueio de exclusão de usuário com chamados, e
consulta de estatísticas/filtros.
