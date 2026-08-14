from models.usuario import Usuario
from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository


class UsuarioService:
    @staticmethod
    def listar_usuarios():
        return [u.to_dict() for u in UsuarioRepository.listar()]

    @staticmethod
    def buscar_usuario(usuario_id) -> Usuario:
        usuario = UsuarioRepository.buscar_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuário não encontrado")
        return usuario

    @staticmethod
    def criar_usuario(dados: dict) -> Usuario:
        nome = (dados.get("nome") or "").strip()
        email = (dados.get("email") or "").strip()
        setor = dados.get("setor")

        if not nome:
            raise ValueError("Nome é obrigatório")
        if not email:
            raise ValueError("E-mail é obrigatório")
        if UsuarioRepository.buscar_por_email(email):
            raise ValueError("Já existe um usuário com este e-mail")

        usuario = Usuario(nome=nome, email=email, setor=setor)
        return UsuarioRepository.criar(usuario)

    @staticmethod
    def atualizar_usuario(usuario_id, dados: dict) -> Usuario:
        usuario = UsuarioService.buscar_usuario(usuario_id)

        nome = dados.get("nome", usuario.nome)
        email = dados.get("email", usuario.email)
        setor = dados.get("setor", usuario.setor)

        if not nome or not str(nome).strip():
            raise ValueError("Nome é obrigatório")
        if not email or not str(email).strip():
            raise ValueError("E-mail é obrigatório")

        email_dono = UsuarioRepository.buscar_por_email(email)
        if email_dono and email_dono.id != usuario.id:
            raise ValueError("Já existe um usuário com este e-mail")

        usuario.nome = nome
        usuario.email = email
        usuario.setor = setor
        UsuarioRepository.salvar_alteracoes()
        return usuario

    @staticmethod
    def excluir_usuario(usuario_id):
        usuario = UsuarioService.buscar_usuario(usuario_id)
        if ChamadoRepository.listar_por_usuario(usuario_id):
            raise ValueError(
                "Não é possível excluir um usuário que possui chamados cadastrados"
            )
        UsuarioRepository.excluir(usuario)

    @staticmethod
    def listar_chamados_do_usuario(usuario_id):
        UsuarioService.buscar_usuario(usuario_id) 
        return [c.to_dict() for c in ChamadoRepository.listar_por_usuario(usuario_id)]
