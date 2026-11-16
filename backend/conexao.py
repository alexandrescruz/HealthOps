import psycopg

from app.database import DB_CONFIG


def listar_estabelecimentos():
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM estabelecimentos")
                return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar estabelecimentos: {e}")
        return []


if __name__ == "__main__":
    for estabelecimento in listar_estabelecimentos():
        print(estabelecimento)
