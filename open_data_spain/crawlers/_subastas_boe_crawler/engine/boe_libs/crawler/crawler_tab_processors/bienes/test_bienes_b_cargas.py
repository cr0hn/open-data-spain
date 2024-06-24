# -*- coding: utf-8 -*-

from subastas_boe.sdk.constants import Cargas

from .rules_tab_bienes import b_cargas


def test_b_cargas_con_cargas():
    words = (
        ("""CARGAS KUTXABANK 5.537,58""", 5537.58),
        ("""TGSS 1.595 €""", 1595),
        ("""4918,19""", 4918.19),
        ("""SI , PRESTAMO BANKIA CON HIPOTECA SOBRE LA VIVIENDA IMPORTE TOTAL 32763,42€""", 32763.42),
        ("""dos prestamos hipotecarios a favor de Unicaja: 6.826,40 y 11.787,35""", 18613.75),
        ("""<td>TITULARES DEL CR&#201;DITO CON PRIVILEGIO ESPECIAL: Por un total de 65.791,19 &#8364;, que se corresponde con el 
        siguiente detalle:
          - BILBAO BIZKAIA KUTXA (ahora KUTXABANK, S.A.), con un cr&#233;dito con privilegio especial de 17.818,79 &#8364;.
          - KUTXABANK, S.A., con un cr&#233;dito con privilegio especial de 47.798,15 &#8364;.
          - Ayuntamiento de Ermua, por el IBI 2018, hipoteca legal t&#225;cita, cr&#233;dito con privilegio especial por importe de 174,
          25 &#8364;</td>""",
         65791.19),
    )

    for text, price in words:
        res = b_cargas(text)

        assert res['cargas'] == Cargas.CON_CARGAS
        assert res['cargas_numero'] == price
        assert res['cargas_raw'] == text


def test_b_cargas_sin_cargas():
    words = (
        """NO CARGAS POSTERIORES A FECHA DEL EDICTO (21-10-2019)""",
        """SIN CARGAS PREFERENTES.""",
        """SIN CARGAS ANTERIORES""",
        """NO FIGURAN""",
        """NO CONSTAN""",
        """NO CONSTAN CARGAS""",
        """LIBRE DE CARGAS""",
        """No constan cargas preferentes""",
        """No constan cargas registradas""",
    )

    for text in words:
        res = b_cargas(text)

        assert res['cargas_raw'] == text
        assert res['cargas_numero'] == 0
        assert res['cargas'] == Cargas.SIN_CARGAS, text


def test_b_cargas_externas():
    words = (
        """se encuentra disponible la certificación de cargas en la Secretaría del Juzgado""",
        """EN DOCUMENTACION ADJUNTA""",
        """SEGÚN CERTIFICACIÓN DE CARGAS""",
        """SE ACOMPAÑA CERTIFICACION DE CARGAS""",
        """se adjunta certificación de CARGAS""",
        """REGISTRO DE LA PROPIEDAD DE ALBARRACÍN , TOMO 761  LIBRO 49   FOLIO 46    FINCA NUMERO 6247""",
        """SE ADJUNTA PDF""",
        """EN LA SECRETARÍA DEL JUZGADO ES POSIBLE LA CONSULTA DE LA CERTIFICACIÓN DE DOMINIO Y CARGAS.""",
        """CERTIFICACION EN EL JUZGADO""",
        """Ver edicto""",
        """Edicto más cargas""",
        """Ver certificación de cargas que se adjunta en los anexos  junto al edicto de subasta""",
        """Ver certificación de cargas adjunta al edicto""",
        """certificado""",
        """REFLEJADAS EN LA CERTIFICACION ADJUNTA""",
        """VER NOTA REGISTRAL""",
        """De acuerdo con el art. 667 LEC, el Portal de Subastas se comunicará, a través de los sistemas del Colegio de Registradores, 
        con el Registro correspondiente a fin de que este confeccione y expida una información registral electrónica referida a la finca 
        o fincas subastadas que se mantendrá permanentemente actualizada hasta el término de la subasta, y será servida a través del 
        Portal de Subastas.""",
        """LAS QUE CONSTEN EN EL REGISTRO DE LA PROPIEDAD""",
        """LAS QUE FIGUREN EN EL REGISTRO DE LA PROPIEDAD""",
        """VER CETIFICACION""",
        """De acuerdo con el art. 656.2 LEC, el registrador de la propiedad notificará al Portal de Subastas el hecho de haberse 
        presentado otro u otros títulos que afecten o modifiquen la información inicial a los efectos del artículo 667.""",
        """A DISPOSICIÓN EN EL REGISTRO DE LA PROPIEDAD DE GERNIKA-LUMO""",
        """CONFORME A LO DISPUESTO EN LA LEC HABRA DE FACILITARSE CERTIFICACION DE CARGAS POR PARTE DEL REGISTRO DE LA PROPIEDAD""",
        """CONSULTAR LA CERTIFICACION DE CARGAS""",
        """Cargas subsistentes: constan en la certificación registral de dominio y cargas con información continuada de fecha 
        16-12-2020.""",
        """Estar a lo dispuesto en el art. 667.2 de la LEC""",
        """CONSULTAR CERTIFCACION DE CARGAS QUE HABRA DE SER APORTADA POR EL REGISTRO DE LA PROPIEDAD""",
        """Consultar en el Registro de la Propiedad de Bilbao nº6""",
        """SEGUN CERTIFIACION DE CARGAS""",
        """PODRÁN CONSULTARSE EN EL REGISTRO DE LA PROPIEDAD DE GERNIA-LUMO.""",
    )

    for text in words:
        res = b_cargas(text)

        assert res['cargas_raw'] == text
        assert res['cargas_numero'] == 0, text
        assert res['cargas'] == Cargas.DOCUMENTO_EXTERNO, text


def test_b_cargas_desconocido():
    words = (
        """Se ejecuta la hipoteca inscripción 3ª.""",
        """el crédito que se ejecuta, es el que está garantizado con la hipoteca constituida en la inscripción 11""",
    )

    for text in words:
        res = b_cargas(text)

        assert res['cargas_raw'] == text
        assert res['cargas_numero'] == 0
        assert res['cargas'] == Cargas.DESCONOCIDO, text
