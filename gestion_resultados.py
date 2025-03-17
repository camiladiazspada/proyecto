import matplotlib.pyplot as plt


class GestionResultados:
    def __init__(self):
        self.resultados = []

    def agregar_resultado(self, resultado):
        self.resultados.append(resultado)

    def verificar_resultados(self):
        for resultado in self.resultados:
            if resultado.es_aceptable():
                print(
                    f"Resultado {resultado.nombre} está dentro de los parámetros aceptables."
                )
            else:
                print(
                    f"Resultado {resultado.nombre} está fuera de los parámetros aceptables."
                )

    def graficar_resultados(self):
        nombres = [resultado.nombre for resultado in self.resultados]
        valores = [resultado.valor for resultado in self.resultados]
        minimos = [resultado.valor_aceptable_min for resultado in self.resultados]
        maximos = [resultado.valor_aceptable_max for resultado in self.resultados]

        plt.figure(figsize=(10, 5))
        plt.plot(nombres, valores, label="Valor", marker="o")
        plt.plot(nombres, minimos, label="Mínimo Aceptable", linestyle="--")
        plt.plot(nombres, maximos, label="Máximo Aceptable", linestyle="--")
        plt.xlabel("Resultados")
        plt.ylabel("Valores")
        plt.title("Resultados del Experimento")
        plt.legend()
        plt.show()
