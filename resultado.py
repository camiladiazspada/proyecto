class Resultado:
    def __init__(self, nombre, valor, valor_aceptable_min, valor_aceptable_max):
        self.nombre = nombre
        self.valor = valor
        self.valor_aceptable_min = valor_aceptable_min
        self.valor_aceptable_max = valor_aceptable_max

    def es_aceptable(self):
        return self.valor_aceptable_min <= self.valor <= self.valor_aceptable_max

    def __str__(self):
        return f"{self.nombre}: {self.valor} (Aceptable: {self.valor_aceptable_min} - {self.valor_aceptable_max})"
