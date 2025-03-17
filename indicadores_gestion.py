import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter


class IndicadoresGestion:
    def __init__(self, gestion_experimentos, gestion_reactivos):
        self.gestion_experimentos = gestion_experimentos
        self.gestion_reactivos = gestion_reactivos

    def investigadores_mas_utilizan(self):
        investigadores = [
            investigador
            for exp in self.gestion_experimentos.experimentos
            for investigador in exp.personas_responsables
        ]
        contador = Counter(investigadores)
        return contador.most_common()

    def experimento_mas_menos_hecho(self):
        experimentos = [exp.receta_id for exp in self.gestion_experimentos.experimentos]
        contador = Counter(experimentos)
        mas_hecho = contador.most_common(1)
        menos_hecho = contador.most_common()[:-2:-1]
        return mas_hecho, menos_hecho

    def reactivos_mas_alta_rotacion(self):
        reactivos = [reactivo.nombre for reactivo in self.gestion_reactivos.reactivos]
        contador = Counter(reactivos)
        return contador.most_common(5)

    def reactivos_mayor_desperdicio(self):
        desperdicio = [
            (reactivo.nombre, reactivo.inventario_disponible * 0.225)
            for reactivo in self.gestion_reactivos.reactivos
        ]
        desperdicio.sort(key=lambda x: x[1], reverse=True)
        return desperdicio[:3]

    def reactivos_mas_vencen(self):
        vencidos = [
            reactivo
            for reactivo in self.gestion_reactivos.reactivos
            if reactivo.fecha_caducidad
            and datetime.strptime(reactivo.fecha_caducidad, "%Y-%m-%d").date()
            < datetime.now().date()
        ]
        contador = Counter([reactivo.nombre for reactivo in vencidos])
        return contador.most_common()

    def experimentos_no_realizados_por_falta_reactivos(self):
        return len(
            [
                exp
                for exp in self.gestion_experimentos.experimentos
                if exp.resultado == "No realizado por falta de reactivos"
            ]
        )

    def graficar_estadisticas(self):
        # Gráfico de investigadores que más utilizan el laboratorio
        investigadores = self.investigadores_mas_utilizan()
        nombres = [inv[0] for inv in investigadores]
        valores = [inv[1] for inv in investigadores]
        plt.figure(figsize=(10, 5))
        plt.bar(nombres, valores)
        plt.xlabel("Investigadores")
        plt.ylabel("Número de usos")
        plt.title("Investigadores que más utilizan el laboratorio")
        plt.show()

        # Gráfico de reactivos con más alta rotación
        reactivos = self.reactivos_mas_alta_rotacion()
        nombres = [reactivo[0] for reactivo in reactivos]
        valores = [reactivo[1] for reactivo in reactivos]
        plt.figure(figsize=(10, 5))
        plt.bar(nombres, valores)
        plt.xlabel("Reactivos")
        plt.ylabel("Rotación")
        plt.title("Reactivos con más alta rotación")
        plt.show()

        # Gráfico de reactivos con mayor desperdicio
        desperdicio = self.reactivos_mayor_desperdicio()
        nombres = [reactivo[0] for reactivo in desperdicio]
        valores = [reactivo[1] for reactivo in desperdicio]
        plt.figure(figsize=(10, 5))
        plt.bar(nombres, valores)
        plt.xlabel("Reactivos")
        plt.ylabel("Desperdicio")
        plt.title("Reactivos con mayor desperdicio")
        plt.show()
