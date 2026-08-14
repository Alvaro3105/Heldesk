from database import db
from models.usuario import Usuario


class UsuarioRepository:
    @staticmethod
    def listar():
        return Usuario.query.all()

    @staticmethod
    def buscar_por_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def buscar_por_email(email):
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def criar(usuario: Usuario) -> Usuario:
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def salvar_alteracoes():
        db.session.commit()

    @staticmethod
    def excluir(usuario: Usuario):
        db.session.delete(usuario)
        db.session.commit()
