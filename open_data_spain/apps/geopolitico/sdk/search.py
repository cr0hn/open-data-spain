from ..models import Provincia


def search_provincia(codigo: str) -> Provincia:
    """
    Search for a provincia by codigo
    """
    return Provincia.objects.get(codigo=codigo)
