class Receta:
    def __init__(self, id, nombre, objetivo, reactivos_utilizados, procedimiento, valores_a_medir):
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos_utilizados = reactivos_utilizados
        self.procedimiento = procedimiento
        self.valores_a_medir = valores_a_medir

    def __str__(self):
        return f"Receta: {self.nombre}\nObjetivo: {self.objetivo}\nReactivos Utilizados: {self.reactivos_utilizados}\nProcedimiento: {self.procedimiento}\nValores a Medir: {self.valores_a_medir}"

