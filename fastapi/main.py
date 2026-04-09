from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def inicio():
    return {"mensaje": "API funcionando correctamente"}


@app.post("/crear")
def crear():
    return {"mensaje": "POST funcionando"}


@app.put("/actualizar/{id}")
def actualizar(id: int):
    return {"mensaje": f"Usuario {id} actualizado"}


@app.delete("/eliminar/{id}")
def eliminar(id: int):
    return {"mensaje": f"Usuario {id} eliminado"}