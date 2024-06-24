import hashlib


def add_bien_id(bien: dict, lote: dict, subasta: dict, config) -> bool:
    """Genera un bien ID único para cada bien"""

    nombre_lote = lote.get("nombre", "")
    subasta_id = subasta.get("identificador")
    bien_descripcion = bien.get("descripcion_raw", "")

    hash_id = hashlib.sha256(f"{nombre_lote}{subasta_id}{bien_descripcion}".encode()).hexdigest()

    bien["id"] = hash_id

    return True


__all__ = ("add_bien_id",)
