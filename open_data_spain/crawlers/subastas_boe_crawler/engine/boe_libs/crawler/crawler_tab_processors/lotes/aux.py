def crear_lote(shared_data: dict, nombre: str, informacion_lote: dict | None, descripcion_lote: str | None, bienes: list) -> dict:
    try:
        lotes = shared_data["lotes"]
    except KeyError:
        lotes = []
        shared_data["lotes"] = lotes

    lotes.append({
        "nombre": nombre,
        "informacion_lote": informacion_lote,
        "descripcion_lote": descripcion_lote,
        "bienes": bienes
    })
