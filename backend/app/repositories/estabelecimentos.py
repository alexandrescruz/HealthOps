from ..database import pool
from psycopg.rows import dict_row

def listar_estabelecimentos():
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM estabelecimentos")
            estabelecimentos = cur.fetchall()
            return estabelecimentos

def listar_estabelecimento_por_municipio(municipio):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM estabelecimentos WHERE municipio = %s", (municipio,))
            estabelecimentos = cur.fetchall()
            return estabelecimentos
        
def listar_estabelecimento_por_id(id):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM estabelecimentos WHERE id = %s", (id,))
            estabelecimento = cur.fetchone()
            return estabelecimento
        
