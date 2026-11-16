from fastapi import APIRouter

from app.schemas import EstabelecimentoResponse
from ..repositories.estabelecimentos import listar_estabelecimentos, listar_estabelecimento_por_municipio, listar_estabelecimento_por_id

router = APIRouter()

@router.get("/api/estabelecimentos", response_model=list[EstabelecimentoResponse])
def get_estabelecimentos():
    
    return listar_estabelecimentos()

