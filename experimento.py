class Experimento:
    def __init__(self, id, receta_id, personas_responsables, fecha, costo_asociado, resultado):
        self.id = id
        self.receta_id = receta_id
        self.personas_responsables = personas_responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado

    def __str__(self):
        return f"Experimento: {self.receta_id}\nResponsable: {self.personas_responsables}\nFecha: {self.fecha}\nCosto: {self.costo_asociado}\nResultado: {self.resultado}"
