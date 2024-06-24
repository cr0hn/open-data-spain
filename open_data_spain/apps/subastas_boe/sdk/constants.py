# -------------------------------------------------------------------------
# Tipos de subasta
# -------------------------------------------------------------------------
def get_values(class_name):
    return [getattr(class_name, atributo) for atributo in vars(class_name) if not atributo.startswith("__")]


class TipoSubasta:
    SEGURIDAD_SOCIAL = "seguridad-social"
    HACIENDA = "hacienda"
    NOTARIAL = "notarial"
    JUDICIAL = "judicial"
    DESCONOCIDO = "desconocido"


class ValorSubasta:
    GENERAL = "general"
    POR_LOTE = "por-lote"
    DESCONOCIDO = "desconocido"


class TipoFecha:
    FIJADAS = "fijada"
    NO_FIJADAS = "no-fijada"
    PROXIMA_APERTURA = "proxima-apertura"
    DESCONOCIDO = "desconocido"


class OrigenSubasta:
    BOE = "boe"
    SEGURIDAD_SOCIAL = "seguridad-social"


class Bancos:
    BBVA = "bbva"
    CAIXA = "caixa"
    SANTANDER = "santander"
    BANKIA = "bankia"
    SABADELL = "sabadell"
    KUTXABANK = "kutxabank"
    UNICAJA = "unicaja"
    IBERCAJA = "ibercaja"
    BANKINTER = "bankinter"
    LIBERBANK = "liberbank"
    MARCH = "march"
    PUEYO = "pueyo"
    BANKOA = "bankoa"
    ALCALA = "alcala"
    OPENBANK = "openbank"
    ACTIVO_BANK = "activo_bank"
    CAJASUR = "cajasur"
    EVO = "evo"
    WIZINK = "wizink"
    ARQUIA = "arquia"
    SELF_BANK = "self-bank"
    CAMINOS = "caminos"
    IMAGINBANK = "imaginbank"
    CAJAMAR = "cajamar"
    CAJA_RURAL = "caja-rural"
    LABORAL_KUTXA = "laboral-kutxa"
    BANTIERRA = "bantierra"
    CAJASIETE = "cajasiete"
    INGENIEROS = "ingenieros"
    GUISSONA = "quissona"
    ING = "ing"
    BANCA_CIVICA = "banca-civica"
    BANIF = "banif"
    NINGUNO = "ninguno"


BANCOS_MAP = {
    Bancos.BBVA: "BBVA",
    Bancos.CAIXA: "Caixa Bank",
    Bancos.SANTANDER: "Banco Santander",
    Bancos.BANKIA: "Bankia",
    Bancos.SABADELL: "Banco Sabadell",
    Bancos.KUTXABANK: "Kutxabank",
    Bancos.UNICAJA: "Unicaja Banco",
    Bancos.IBERCAJA: "Ibercaja",
    Bancos.BANKINTER: "Bankinter",
    Bancos.LIBERBANK: "Liberbank",
    Bancos.MARCH: "Banca March",
    Bancos.PUEYO: "Banca Pueyo",
    Bancos.BANKOA: "Bankoa",
    Bancos.ALCALA: "Banca Alcalá",
    Bancos.OPENBANK: "Openbank",
    Bancos.ACTIVO_BANK: "Activo Bank",
    Bancos.CAJASUR: "Cajasur",
    Bancos.EVO: "Evo Banco",
    Bancos.WIZINK: "Wizink",
    Bancos.ARQUIA: "Arquia",
    Bancos.SELF_BANK: "Self Bank",
    Bancos.CAMINOS: "Banco Caminos",
    Bancos.IMAGINBANK: "Imaginbank",
    Bancos.CAJAMAR: "Cajamar",
    Bancos.CAJA_RURAL: "Caja Rural",
    Bancos.LABORAL_KUTXA: "Laboral Kutxa",
    Bancos.BANTIERRA: "Bantierra",
    Bancos.CAJASIETE: "Cajasiete",
    Bancos.INGENIEROS: "Caja de Ingenieros",
    Bancos.GUISSONA: "Guissona",
    Bancos.ING: "ING Direct",
    Bancos.BANCA_CIVICA: "Banca Cívica",
    Bancos.BANIF: "Banif",
}

BANCOS_KEYWORDS = {
    Bancos.BBVA: "bbva",
    Bancos.CAIXA: "caixa",
    Bancos.SANTANDER: "santander",
    Bancos.BANKIA: "bankia",
    Bancos.SABADELL: "sabadell",
    Bancos.KUTXABANK: "kutxabank",
    Bancos.UNICAJA: "unicaja",
    Bancos.IBERCAJA: "ibercaja",
    Bancos.BANKINTER: "bankinter",
    Bancos.LIBERBANK: "liberbank",
    Bancos.MARCH: "march",
    Bancos.PUEYO: "pueyo",
    Bancos.BANKOA: "bankoa",
    Bancos.ALCALA: "alcal",
    Bancos.OPENBANK: "openbank",
    Bancos.ACTIVO_BANK: "activo",
    Bancos.CAJASUR: "cajasur",
    Bancos.EVO: "evo",
    Bancos.WIZINK: "wizink",
    Bancos.ARQUIA: "arquia",
    Bancos.SELF_BANK: "self",
    Bancos.CAMINOS: "caminos",
    Bancos.IMAGINBANK: "imaginbank",
    Bancos.CAJAMAR: "cajamar",
    Bancos.CAJA_RURAL: "rural",
    Bancos.LABORAL_KUTXA: "laboral kutxa",
    Bancos.BANTIERRA: "bantierra",
    Bancos.CAJASIETE: "cajasiete",
    Bancos.INGENIEROS: "ingenieros",
    Bancos.GUISSONA: "guissona",
    Bancos.ING: "ing",
    Bancos.BANCA_CIVICA: "vica",
    Bancos.BANIF: "banif",
}


class TipoAcreedor:
    BANCO = "banco"
    OTRO = "otro"
    EMPRESA = "empresa"
    PARTICULAR = "particular"
    DESCONOCIDO = "desconocido"


class SituacionPosesoria:
    DERECHO_USO = "derecho-uso"
    DERECHO_PERMANENCIA = "derecho-permanencia"
    OCUPANTE_DESCONOCIDO = "ocupante-desconocido"
    SIN_OCUPANTES = "sin-ocupantes"
    NO_CONSTA = "no-consta"
    DESCONOCIDO = "desconocido"
    PORCENTAJE_50 = "50-porciento"


class Visitable:
    SI = "si"
    NO = "no"
    NO_CONSTA = "no-consta"


class Cargas:
    CON_CARGAS = "con-cargas"
    SIN_CARGAS = "sin-cargas"
    NO_CONSTA = "no-consta"
    REGISTRADORES = "externo-registradores"
    DOCUMENTO_EXTERNO = "documento-externo"
    DESCONOCIDO = "desconocido"


class TituloJuridico:
    PLENO_DOMINIO = "pleno-condominio"
    PARTE = "parte"
    DESCONOCIDO = "desconocido"


class ViviendaHabitual:
    SI = "si"
    NO = "no"
    DESCONOCIDO = "desconocido"


class EstadoPujas:
    SIN_PUJAS = "sin-pujas"
    CON_PUJAS = "con-pujas"
    SUBASTA_SIN_INICIAR = "subasta-sin-iniciar"
    DESCONOCIDO = "desconocido"


class Fechas:
    FIJADAS = "fijadas"
    PROXIMA_APERTURA = "proxima-apertura"
    DESCONOCIDO = "desconocido"


class Tasacion:
    CON_TASACION = "con-tasacion"
    SIN_TASACION = "sin-tasacion"
    POR_LOTE = "por-lote"
    NO_CONSTA = "no-consta"
    DESCONOCIDO = "desconocido"


class PujaMinima:
    SIN_PUJA_MINIMA = "sin-puja-minima"
    CON_PUJA_MINIMA = "con-puja-minima"
    POR_LOTE = "por-lote"
    NO_CONSTA = "no-consta"
    DESCONOCIDO = "desconocido"


class TramosPujas:
    CON_TRAMOS = "con-tramos"
    SIN_TRAMOS = "sin-tramos"
    NO_CONSTA = "no-consta"
    POR_LOTE = "por-lote"
    DESCONOCIDO = "desconocido"


class Deposito:
    NECESARIO = "necesario"
    NO_NECESARIO = "no-necesario"
    NO_CONSTA = "no-consta"
    POR_LOTE = "por-lote"
    DESCONOCIDO = "desconocido"


# noinspection NonAsciiCharacters
class TipoEstancia:
    BAÑO = "baño"
    ASEO = "aseo"
    COCINA = "cocina"
    DORMITORIO = "dormitorio"
    TERRAZA = "terraza"
    PASILLO = "pasillo"
    LAVADERO = "lavadero"
    SALON = "salon"
    RECIBIDOR = "recididor"
    SOLARIUM = "solarion"
    OTRO = "otro"


class TipoPropiedad:
    URBANO = "urbano"
    RUSTICO = "rustico"
    DESCONOCIDO = "desconocido"


class TipoConstruccion:
    CASA = "casa"
    PISO = "piso"
    NAVE = "nave"
    ATICO = "atico"
    LOCAL = "local"
    LOCAL_COMERCIAL = "local-comercial"
    COMERCIO = "comercio"
    GARAGE = "garage"
    FINCA = "finca"
    FINCA_PARCELA = "finca-parcela"
    TRASTERO = "trastero"
    DUPLEX = "duplex"
    ALMACEN = "almacen"
    SOLAR = "solar"
    OFICINA = "oficina"
    PAJAR = "pajar"
    CUADRA = "cuadra"
    OTHER = "otros"


class OrigenInformacion:
    TAB = "tab"
    SCRIPT = "script"
