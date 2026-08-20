from models.chamado import Chamado
from repositories.chamado_repository import ChamadoRepository
from repositories.usuario_repository import UsuarioRepository

PRIORIDADES_VALIDAS = ["Baixa", "Média", "Alta"]
PRIORIDADE_LIMITADA = "Alta"
LIMITE_CHAMADOS_PRIORIDADE_LIMITADA = 5
TRANSICOES_PERMITIDAS = {
    "Aberto": ["Em atendimento"],
    "Em atendimento": ["Encerrado"],
    "Encerrado": [],
}


class ChamadoService:
    @staticmethod
    def listar_chamados():
        return [c.to_dict() for c in ChamadoRepository.listar()]

    @staticmethod
    def buscar_chamado(chamado_id) -> Chamado:
        chamado = ChamadoRepository.buscar_por_id(chamado_id)
        if not chamado:
            raise ValueError("Chamado não encontrado")
        return chamado

    @staticmethod
    def _validar_limite_prioridade_alta(usuario_id, prioridade, chamado_atual=None):
        if prioridade != PRIORIDADE_LIMITADA:
            return

        if chamado_atual and chamado_atual.status == "Encerrado":
            return

        if chamado_atual and chamado_atual.prioridade == PRIORIDADE_LIMITADA:
            return

        total = ChamadoRepository.contar_nao_encerrados_por_prioridade(
            usuario_id, PRIORIDADE_LIMITADA
        )
        if total >= LIMITE_CHAMADOS_PRIORIDADE_LIMITADA:
            raise ValueError(
                f"Usuário já possui {LIMITE_CHAMADOS_PRIORIDADE_LIMITADA} "
                f"chamados de prioridade {PRIORIDADE_LIMITADA} não encerrados"
            )

    @staticmethod
    def criar_chamado(dados: dict) -> Chamado:
        titulo = (dados.get("titulo") or "").strip()
        descricao = (dados.get("descricao") or "").strip()
        prioridade = dados.get("prioridade")
        tecnico = dados.get("tecnico")
        usuario_id = dados.get("usuario_id")

        if not titulo or len(titulo) < 5:
            raise ValueError("Título é obrigatório e deve possuir pelo menos 5 caracteres")
        if not descricao or len(descricao) < 10:
            raise ValueError("Descrição deve possuir pelo menos 10 caracteres")
        if prioridade not in PRIORIDADES_VALIDAS:
            raise ValueError(
                f"Prioridade deve ser uma das seguintes: {', '.join(PRIORIDADES_VALIDAS)}"
            )
        if not usuario_id:
            raise ValueError("O chamado deve estar vinculado a um usuário")
        if not UsuarioRepository.buscar_por_id(usuario_id):
            raise ValueError("Usuário vinculado não encontrado")

        ChamadoService._validar_limite_prioridade_alta(usuario_id, prioridade)

        chamado = Chamado(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            status="Aberto",
            tecnico=tecnico,
            usuario_id=usuario_id,
        )
        return ChamadoRepository.criar(chamado)

    @staticmethod
    def atualizar_chamado(chamado_id, dados: dict) -> Chamado:
        chamado = ChamadoService.buscar_chamado(chamado_id)

        titulo = str(dados.get("titulo", chamado.titulo) or "").strip()
        descricao = str(dados.get("descricao", chamado.descricao) or "").strip()
        prioridade = dados.get("prioridade", chamado.prioridade)
        tecnico = dados.get("tecnico", chamado.tecnico)

        if len(titulo) < 5:
            raise ValueError("Título deve possuir pelo menos 5 caracteres")
        if len(descricao) < 10:
            raise ValueError("Descrição deve possuir pelo menos 10 caracteres")
        if prioridade not in PRIORIDADES_VALIDAS:
            raise ValueError(
                f"Prioridade deve ser uma das seguintes: {', '.join(PRIORIDADES_VALIDAS)}"
            )

        ChamadoService._validar_limite_prioridade_alta(
            chamado.usuario_id, prioridade, chamado_atual=chamado
        )

        chamado.titulo = titulo
        chamado.descricao = descricao
        chamado.prioridade = prioridade
        chamado.tecnico = tecnico
        ChamadoRepository.salvar_alteracoes()
        return chamado

    @staticmethod
    def excluir_chamado(chamado_id):
        chamado = ChamadoService.buscar_chamado(chamado_id)
        ChamadoRepository.excluir(chamado)

    @staticmethod
    def _validar_transicao(status_atual, novo_status):
        if novo_status not in TRANSICOES_PERMITIDAS.get(status_atual, []):
            raise ValueError(
                f"Transição de status inválida: {status_atual} -> {novo_status}"
            )

    @staticmethod
    def iniciar_atendimento(chamado_id) -> Chamado:
        chamado = ChamadoService.buscar_chamado(chamado_id)
        ChamadoService._validar_transicao(chamado.status, "Em atendimento")
        chamado.status = "Em atendimento"
        ChamadoRepository.salvar_alteracoes()
        return chamado

    @staticmethod
    def encerrar_chamado(chamado_id) -> Chamado:
        chamado = ChamadoService.buscar_chamado(chamado_id)
        ChamadoService._validar_transicao(chamado.status, "Encerrado")
        chamado.status = "Encerrado"
        ChamadoRepository.salvar_alteracoes()
        return chamado

    @staticmethod
    def listar_abertos():
        return [c.to_dict() for c in ChamadoRepository.listar_abertos()]

    @staticmethod
    def listar_prioridade_alta():
        return [c.to_dict() for c in ChamadoRepository.listar_por_prioridade("Alta")]

    @staticmethod
    def estatisticas():
        return {
            "usuarios": len(UsuarioRepository.listar()),
            "chamados": ChamadoRepository.contar_total(),
            "abertos": ChamadoRepository.contar_por_status("Aberto"),
            "em_atendimento": ChamadoRepository.contar_por_status("Em atendimento"),
            "encerrados": ChamadoRepository.contar_por_status("Encerrado"),
        }
