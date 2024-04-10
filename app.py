from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

origins = [
    '*',
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
        {"Data": row[0], "Valor": row[1], "Tipo": row[2], "Descricao": row[3]}
        for row in transactions
    ]
    return transactions_dict

@app.get("/transactions/gastos/{ano}/{mes}")
def obter_gastos_por_mes(ano:int, mes:int) -> List[dict]:
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
        {"Data": row[0], "Valor": row[1], "Tipo": row[2], "Descricao": row[3]}
        for row in transactions
    ]
    return transactions_dict

@app.get("/transactions/recebimentos/{ano}/{mes}")
def obter_gastos_por_mes(ano:int, mes:int) -> List[dict]:
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
        {"Data": row[0], "Valor": row[1], "Tipo": row[2], "Descricao": row[3]}
        for row in transactions
    ]
    return transactions_dict