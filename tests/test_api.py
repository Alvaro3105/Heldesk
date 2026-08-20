import unittest

from app import create_app
from database import db


class HelpdeskApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def criar_usuario(self):
        resposta = self.client.post(
            "/usuarios",
            json={
                "nome": "Maria Silva",
                "email": "maria@empresa.com",
                "setor": "TI",
            },
        )
        self.assertEqual(resposta.status_code, 201)
        return resposta.get_json()

    def test_fluxo_principal_da_api(self):
        usuario = self.criar_usuario()

        resposta_usuario = self.client.get(f"/usuarios/{usuario['id']}")
        self.assertEqual(resposta_usuario.status_code, 200)

        resposta_chamado = self.client.post(
            "/chamados",
            json={
                "titulo": "Impressora não funciona",
                "descricao": "A impressora do setor administrativo não liga.",
                "prioridade": "Alta",
                "usuario_id": usuario["id"],
            },
        )
        self.assertEqual(resposta_chamado.status_code, 201)
        chamado = resposta_chamado.get_json()
        self.assertEqual(chamado["status"], "Aberto")

        resposta_busca = self.client.get(f"/chamados/{chamado['id']}")
        self.assertEqual(resposta_busca.status_code, 200)

        resposta_inicio = self.client.patch(f"/chamados/{chamado['id']}/iniciar")
        self.assertEqual(resposta_inicio.status_code, 200)
        self.assertEqual(resposta_inicio.get_json()["status"], "Em atendimento")

        resposta_fim = self.client.patch(f"/chamados/{chamado['id']}/encerrar")
        self.assertEqual(resposta_fim.status_code, 200)
        self.assertEqual(resposta_fim.get_json()["status"], "Encerrado")

        resposta_estatisticas = self.client.get("/estatisticas")
        self.assertEqual(resposta_estatisticas.status_code, 200)
        estatisticas = resposta_estatisticas.get_json()
        self.assertEqual(estatisticas["usuarios"], 1)
        self.assertEqual(estatisticas["chamados"], 1)
        self.assertEqual(estatisticas["encerrados"], 1)

    def test_bloqueia_exclusao_de_usuario_com_chamado(self):
        usuario = self.criar_usuario()

        resposta_chamado = self.client.post(
            "/chamados",
            json={
                "titulo": "Erro no computador",
                "descricao": "O computador reinicia durante a utilização.",
                "prioridade": "Média",
                "usuario_id": usuario["id"],
            },
        )
        self.assertEqual(resposta_chamado.status_code, 201)

        resposta_exclusao = self.client.delete(f"/usuarios/{usuario['id']}")
        self.assertEqual(resposta_exclusao.status_code, 409)

    def test_valida_dados_do_chamado(self):
        usuario = self.criar_usuario()

        resposta = self.client.post(
            "/chamados",
            json={
                "titulo": "Erro",
                "descricao": "Curta",
                "prioridade": "Urgente",
                "usuario_id": usuario["id"],
            },
        )
        self.assertEqual(resposta.status_code, 400)


if __name__ == "__main__":
    unittest.main()
