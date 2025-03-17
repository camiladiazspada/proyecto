import json
import random
from datetime import datetime
from receta import Receta
from experimento import Experimento
from gestion_reactivos import GestionReactivos


class GestionExperimentos:
    def __init__(self):
        self.recetas = []
        self.experimentos = []
        self.gestion_reactivos = GestionReactivos()

    def agregar_receta(self, receta):
        self.recetas.append(receta)

    def eliminar_receta(self, nombre):
        self.recetas = [r for r in self.recetas if r.nombre != nombre]

    def editar_receta(self, nombre, **kwargs):
        for receta in self.recetas:
            if receta.nombre == nombre:
                for key, value in kwargs.items():
                    setattr(receta, key, value)

    def listar_recetas(self):
        for receta in self.recetas:
            print(receta)

    def agregar_experimento(self, experimento):
        self.experimentos.append(experimento)

    def eliminar_experimento(self, nombre):
        self.experimentos = [e for e in self.experimentos if e.receta_id != nombre]

    def editar_experimento(self, nombre, **kwargs):
        for experimento in self.experimentos:
            if experimento.receta_id == nombre:
                for key, value in kwargs.items():
                    setattr(experimento, key, value)

    def listar_experimentos(self):
        for experimento in self.experimentos:
            print(experimento)

    def realizar_experimento(self, receta_nombre, persona_responsable):
        receta = next((r for r in self.recetas if r.nombre == receta_nombre), None)
        if not receta:
            print(f"Receta {receta_nombre} no encontrada.")
            return

        # Validar disponibilidad de reactivos
        for reactivo_nombre, cantidad in receta.reactivos_utilizados.items():
            reactivo = next(
                (
                    r
                    for r in self.gestion_reactivos.reactivos
                    if r.nombre == reactivo_nombre
                ),
                None,
            )
            if (
                not reactivo
                or reactivo.inventario < cantidad
                or (
                    reactivo.fecha_caducidad
                    and reactivo.fecha_caducidad < datetime.now()
                )
            ):
                print(f"Reactivo {reactivo_nombre} no disponible o caducado.")
                return

        # Restar del inventario y aplicar error aleatorio
        costo_total = 0
        for reactivo_nombre, cantidad in receta.reactivos_utilizados.items():
            reactivo = next(
                (
                    r
                    for r in self.gestion_reactivos.reactivos
                    if r.nombre == reactivo_nombre
                ),
                None,
            )
            error = random.uniform(0.001, 0.225)
            cantidad_total = cantidad * (1 + error)
            reactivo.inventario -= cantidad_total
            costo_total += reactivo.costo * cantidad_total

        # Crear experimento
        experimento = Experimento(
            receta=receta,
            persona_responsable=persona_responsable,
            fecha=datetime.now(),
            costo_asociado=costo_total,
            resultado="Pendiente",
        )
        self.agregar_experimento(experimento)
        print(f"Experimento {receta_nombre} realizado con éxito.")

    def guardar_datos(self, archivo):
        datos = {
            "recetas": [receta.__dict__ for receta in self.recetas],
            "experimentos": [experimento.__dict__ for experimento in self.experimentos],
        }
        with open(archivo, "w") as file:
            json.dump(datos, file, default=str)

    def cargar_datos(self, archivo):
        with open(archivo, "r") as file:
            datos = json.load(file)
            self.recetas = [Receta(**receta) for receta in datos["recetas"]]
            self.experimentos = [
                Experimento(**experimento) for experimento in datos["experimentos"]
            ]
