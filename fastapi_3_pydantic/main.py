from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "API de Juegos"


NOT_FOUND_RESPONSE = {
    404: {
        "description": "No se encontró un juego con ese ID",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Juego no encontrado"
                }
            }
        },
    }
}


# Type aliases con Annotated + Field
IdJuego = Annotated[int, Field(gt=0, description="ID del juego")]
NombreJuego = Annotated[str, Field(min_length=2, max_length=40)]
GeneroJuego = Annotated[str, Field(min_length=3, max_length=30)]
PrecioJuego = Annotated[float, Field(ge=0, le=999999)]
DisponibleJuego = Annotated[bool, Field(description="Indica si el juego está disponible")]


class JuegoSchema(BaseModel):
    id: IdJuego
    nombre: NombreJuego
    genero: GeneroJuego
    precio: PrecioJuego
    disponible: DisponibleJuego = True


class JuegoUpdateSchema(BaseModel):
    nombre: NombreJuego
    genero: GeneroJuego
    precio: PrecioJuego
    disponible: DisponibleJuego = True


juegos = [
    {"id": 1, "nombre": "Valorant", "genero": "Shooter", "precio": 0, "disponible": True},
    {"id": 2, "nombre": "Minecraft", "genero": "Sandbox", "precio": 15000, "disponible": True},
    {"id": 3, "nombre": "FIFA 25", "genero": "Deportes", "precio": 70000, "disponible": False},
]


@app.get("/juegos", response_model=list[JuegoSchema])
async def obtener_juegos(
    solo_disponibles: Annotated[
        bool,
        Query(description="Si es true, muestra solo los juegos disponibles")
    ] = False
):
    if solo_disponibles:
        return [juego for juego in juegos if juego["disponible"]]

    return juegos


@app.get(
    "/juegos/{id}",
    response_model=JuegoSchema,
    responses=NOT_FOUND_RESPONSE
)
async def obtener_juego_por_id(
    id: Annotated[int, Path(gt=0, description="ID del juego a buscar")]
):
    for juego in juegos:
        if juego["id"] == id:
            return juego

    raise HTTPException(status_code=404, detail="Juego no encontrado")


@app.post("/juegos", response_model=list[JuegoSchema])
async def crear_juego(juego_nuevo: JuegoSchema):
    for juego in juegos:
        if juego["id"] == juego_nuevo.id:
            raise HTTPException(status_code=400, detail="Ya existe un juego con ese ID")

    juegos.append(juego_nuevo.model_dump())
    return juegos


@app.put(
    "/juegos/{id}",
    response_model=JuegoSchema,
    responses=NOT_FOUND_RESPONSE
)
async def editar_juego(
    id: Annotated[int, Path(gt=0, description="ID del juego a editar")],
    juego_editado: JuegoUpdateSchema
):
    for juego in juegos:
        if juego["id"] == id:
            juego["nombre"] = juego_editado.nombre
            juego["genero"] = juego_editado.genero
            juego["precio"] = juego_editado.precio
            juego["disponible"] = juego_editado.disponible
            return juego

    raise HTTPException(status_code=404, detail="Juego no encontrado")


@app.delete(
    "/juegos/{id}",
    response_model=JuegoSchema,
    responses=NOT_FOUND_RESPONSE
)
async def eliminar_juego(
    id: Annotated[int, Path(gt=0, description="ID del juego a eliminar")],
    logico: Annotated[
        bool,
        Query(description="Si es true, no borra el juego, solo lo marca como no disponible")
    ] = False
):
    for juego in juegos:
        if juego["id"] == id:
            if logico:
                juego["disponible"] = False
                return juego

            juegos.remove(juego)
            return juego

    raise HTTPException(status_code=404, detail="Juego no encontrado")