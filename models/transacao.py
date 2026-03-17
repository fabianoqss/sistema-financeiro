class Transacao:
  def __init__(self, id, descricao, valor, tipo, data, categoria_id, usuario_id):
    self.id = id;
    self.descricao = descricao;
    self.valor = valor;
    self.tipo = tipo;
    self.data = data;
    self.categoria_id = categoria_id;
    self.usuario_id = usuario_id;