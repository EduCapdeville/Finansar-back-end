from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def connect_to_database():
    conn = sqlite3.connect("finansar.sqlite")
    return conn


@app.get("/transactions/{ano}/{mes}")
def obter_transacoes_por_mes(ano: int, mes: int) -> List[dict]:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM transactions WHERE strftime('%Y-%m', Data) = '{ano}-{mes:02}'"
    )
    transactions = cursor.fetchall()
    conn.close()
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma transação encontrada para o mês especificado",
        )

    transactions_dict = [
        {
            "Localizador": row[0],
            "Data": row[1],
            "Valor": row[2],
            "Tipo": row[3],
            "Descricao": row[4],
            "Categoria": row[5],
        }
        for row in transactions
    ]
    return transactions_dict


@app.get("/transactions/gastos/{ano}/{mes}")
def obter_gastos_por_mes(ano: int, mes: int) -> List[dict]:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM transactions WHERE Valor < 0 AND strftime('%Y-%m', Data) = '{ano}-{mes:02}' ORDER BY Data DESC"
    )
    transactions = cursor.fetchall()
    conn.close()
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma transação encontrada para o mês especificado",
        )

    transactions_dict = [
        {
            "Localizador": row[0],
            "Data": row[1],
            "Valor": row[2],
            "Tipo": row[3],
            "Descricao": row[4],
            "Categoria": row[5],
        }
        for row in transactions
    ]
    return transactions_dict


@app.get("/transactions/recebimentos/{ano}/{mes}")
def obter_gastos_por_mes(ano: int, mes: int) -> List[dict]:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT * FROM transactions WHERE Valor > 0 AND strftime('%Y-%m', Data) = '{ano}-{mes:02}' ORDER BY Data DESC"
    )
    transactions = cursor.fetchall()
    conn.close()
    if not transactions:
        raise HTTPException(
            status_code=404,
            detail="Nenhuma transação encontrada para o mês especificado",
        )

    transactions_dict = [
        {
            "Localizador": row[0],
            "Data": row[1],
            "Valor": row[2],
            "Tipo": row[3],
            "Descricao": row[4],
            "Categoria": row[5],
        }
        for row in transactions
    ]
    return transactions_dict


@app.get("/transactions/categories")
def obter_categorias() -> List[str]:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT categoria FROM transactions WHERE Descricao IS NOT NULL"
    )
    categories = cursor.fetchall()
    conn.close()
    return [category[0] for category in categories]


@app.get("/transactions/summary")
def obter_gastos_sumarizados() -> List[dict]:
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT STRFTIME('%m-%Y', Data) as mes_ano, SUM(Valor) as total_gastos FROM transactions GROUP BY mes_ano"
    )
    summary = cursor.fetchall()
    conn.close()

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Nenhum gasto encontrado"
        )

    summary_dict = [
        {
            "mes_ano": row[0],
            "total_gastos": row[1]
        }
        for row in summary
    ]
    return summary_dict


@app.put("/transactions/{transacao_id}/{categoria}")
def atualizar_categoria(transacao_id: int, categoria: str):
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE transactions SET Categoria = ? WHERE Localizador = ?",
        (categoria, transacao_id),
    )
    conn.commit()
    conn.close()
    return {"Categoria atualizada com sucesso"}
