from fastapi import Body, FastAPI, Path, Query

app = FastAPI()

app.title = "API de Juegos"

juegos = [
    {"id": 1, "nombre": "Minecraft", "genero": "Sandbox", "precio": 12000, "activo": True},
    {"id": 2, "nombre": "Valorant", "genero": "Shooter", "precio": 0, "activo": True},
    {"id": 3, "nombre": "League of Legends", "genero": "MOBA", "precio": 0, "activo": True},
]


@app.get("/juegos")
async def get_juegos(
    solo_activos: bool = Query(default=True, description="Mostrar solo juegos activos")
):
    if solo_activos:
        return [juego for juego in juegos if juego["activo"] == True]

    return juegos


@app.get("/juegos/{id}")
async def get_juego_by_id(
    id: int = Path(gt=0, description="Id del juego. Debe ser mayor a 0")
):
    for juego in juegos:
        if juego["id"] == id:
            return juego

    return {"detail": "Juego no encontrado"}


@app.post("/juegos")
async def crear_juego(
    id: int = Body(gt=0),
    nombre: str = Body(min_length=2, max_length=60),
    genero: str = Body(min_length=3, max_length=40),
    precio: float = Body(ge=0, lt=99999999),
):
    nuevo_juego = {
        "id": id,
        "nombre": nombre,
        "genero": genero,
        "precio": precio,
        "activo": True
    }

    juegos.append(nuevo_juego)

    return nuevo_juego


@app.put("/juegos/{id}")
async def editar_juego(
    id: int = Path(gt=0, description="Id del juego. Debe ser mayor a 0"),
    nombre: str = Body(min_length=2, max_length=60),
    genero: str = Body(min_length=3, max_length=40),
    precio: float = Body(ge=0, lt=99999999),
):
    for juego in juegos:
        if juego["id"] == id:
            juego["nombre"] = nombre
            juego["genero"] = genero
            juego["precio"] = precio

            return juego

    return {"detail": "Juego no encontrado"}


@app.delete("/juegos/{id}")
async def borrar_juego(
    id: int = Path(gt=0, description="Id del juego. Debe ser mayor a 0"),
    logico: bool = Query(default=False, description="Si es true, no borra el juego, solo lo desactiva")
):
    for juego in juegos:
        if juego["id"] == id:
            if logico:
                juego["activo"] = False
            else:
                juegos.remove(juego)

            return {"detail": "Juego borrado correctamente"}

    return {"detail": "Juego no encontrado"}