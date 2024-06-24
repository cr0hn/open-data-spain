def add_titulo(bien: dict, lote: dict, subasta: dict, config) -> bool:
    if bien.get("titulo"):
        return False

    provincia = bien.get("provincia")
    municipio = bien.get("municipio")

    if municipio and provincia:
        titulo = f"Vivienda sita en {municipio} ({provincia})"

    elif provincia:
        titulo = f"Vivienda sita en {provincia}"

    else:
        descripcion = bien.get("descripcion", "")

        titulo = descripcion[:descripcion.find(".")]

    bien["titulo"] = titulo

    return True


__all__ = ("add_titulo",)
