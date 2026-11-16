from pydantic import BaseModel

class EstabelecimentoResponse(BaseModel):
    id: int
    nome: str
    municipio: str
    tipo: str | None = None
    ativo: bool | None = None
