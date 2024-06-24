from collections import Counter


class AnalyticMaxPerTerritorio(Exception):
    ...


class AnalyticMaxGlobal(Exception):
    ...


class _Analytics:

    def __init__(self):
        self.subasta_procesada_territorio = Counter()
        self.max_per_territorio = 50
        self.global_max_count = 1000

    def add_subasta_procesada_territorio(self, territorio: str):
        self.subasta_procesada_territorio[territorio] += 1

        if self.subasta_procesada_territorio[territorio] > self.max_per_territorio:
            raise AnalyticMaxPerTerritorio(
                f"Se han procesado {self.subasta_procesada_territorio[territorio]} "
                f"subastas para el territorio {territorio}"
            )

        if sum(self.subasta_procesada_territorio.values()) > self.global_max_count:
            raise AnalyticMaxGlobal("Se han procesado demasiadas subastas en total")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.subasta_procesada_territorio = Counter()

    def __call__(self, *args, **kwargs):
        return self.add_subasta_procesada_territorio(*args, **kwargs)


tracking = _Analytics()

__all__ = ("AnalyticMaxPerTerritorio", "AnalyticMaxGlobal", "tracking")
