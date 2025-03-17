from reactivo import Reactivo
from datetime import datetime


class GestionReactivos:
    def __init__(self):
        self.reactivos = []

    def agregar_reactivo(self, reactivo):
        self.reactivos.append(reactivo)

    def eliminar_reactivo(self, nombre):
        nombre = nombre.strip().lower()
        self.reactivos = [r for r in self.reactivos if r.nombre.strip().lower() != nombre]

    def editar_reactivo(self, nombre, **kwargs):
        for reactivo in self.reactivos:
            if reactivo.nombre == nombre:
                for key, value in kwargs.items():
                    setattr(reactivo, key, value)

    def listar_reactivos(self):
        for reactivo in self.reactivos:
            print(reactivo)

    def cargar_reactivos_desde_archivo(self, archivo):
        with open(archivo, "r") as file:
            for line in file:
                datos = line.strip().split(",")
                (
                    nombre,
                    descripcion,
                    costo,
                    categoria,
                    inventario,
                    unidad_medicion,
                    fecha_caducidad,
                ) = datos
                reactivo = Reactivo(
                    nombre,
                    descripcion,
                    float(costo),
                    categoria,
                    int(inventario),
                    unidad_medicion,
                    (
                        datetime.strptime(fecha_caducidad, "%Y-%m-%d")
                        if fecha_caducidad
                        else None
                    ),
                )
                self.agregar_reactivo(reactivo)

    def verificar_inventario_minimo(self, minimo):
        for reactivo in self.reactivos:
            if reactivo.inventario < minimo:
                print(
                    f"Advertencia: El reactivo {reactivo.nombre} está por debajo del inventario mínimo sugerido."
                )
