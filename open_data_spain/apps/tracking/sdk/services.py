class Services:
    """
    Esta clase debe contener los servicios disponibles en la API de Open Data Spain
    """
    SUBASTAS_BOE = "subastas-publicas"
    GEO_POLITICO = "geo-politico"


def service_resolver(_path: str) -> str:
    """
    Esta función debe resolver el path de un servicio a su correspondiente
    """
    if _path is None:
        raise ValueError("El path no puede ser None")

    if _path.startswith("/api/v1.0/geo-politico/"):
        return Services.GEO_POLITICO

    if _path.startswith("/api/v1.0/subastas-publicas/"):
        return Services.SUBASTAS_BOE

    raise ValueError(f"El servicio {_path} no existe")


__all__ = ("Services", "service_resolver")
