import datetime

class Usuario:
    def __init__(self, id, nome, senha, admin=False, ativo=True):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.admin = admin
        self.ativo = ativo

    @staticmethod
    def from_row(row):
        if row:
            return Usuario(row[0], row[1], row[2], bool(row[3]), bool(row[4]))
        return None


class SessaoAtiva:
    def __init__(self, id, usuario_id, token, criado_em, expira_em):
        self.id = id
        self.usuario_id = usuario_id
        self.token = token
        self.criado_em = criado_em
        self.expira_em = expira_em

    @staticmethod
    def from_row(row):
        if row:
            return SessaoAtiva(row[0], row[1], row[2], row[3], row[4])
        return None 