from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class Form(BaseModel):
    nome: str
    email: str
    usuario_msg: str


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

def criar_string(nome, email, mensagem):
    return f"Nome: {nome}\nEmail: {email}\nMensagem: {mensagem}\n\n"


@app.post("/forms")
async def create_form(form: Form):
    texto = criar_string(form.nome, form.email, form.usuario_msg)
    with open("Output.txt", "a") as text_file:
        text_file.write(texto)