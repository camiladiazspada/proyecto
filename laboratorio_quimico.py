import os
import json
import requests
from datetime import datetime
from gestion_reactivos import GestionReactivos
from gestion_experimento import GestionExperimentos
from gestion_resultados import GestionResultados
from indicadores_gestion import IndicadoresGestion
from reactivo import Reactivo
from receta import Receta
from experimento import Experimento
from resultado import Resultado


class LaboratorioQuimico:
    def __init__(self):
        self.gestion_reactivos = GestionReactivos()
        self.gestion_experimentos = GestionExperimentos()
        self.gestion_resultados = GestionResultados()
        self.indicadores_gestion = IndicadoresGestion(
            self.gestion_experimentos, self.gestion_reactivos
        )

    def cargar_datos_iniciales(self):
        """Carga los datos iniciales desde la API."""
        base_url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main"
        reactivos_url = f"{base_url}/reactivos.json"
        recetas_url = f"{base_url}/recetas.json"
        experimentos_url = f"{base_url}/experimentos.json"

        reactivos = requests.get(reactivos_url).json()
        recetas = requests.get(recetas_url).json()
        experimentos = requests.get(experimentos_url).json()

        return reactivos, recetas, experimentos

    def guardar_estado(self, archivo):
        """Guarda el estado del programa en un archivo JSON."""
        datos = {
            "reactivos": [
                reactivo.__dict__ for reactivo in self.gestion_reactivos.reactivos
            ],
            "recetas": [
                receta.__dict__ for receta in self.gestion_experimentos.recetas
            ],
            "experimentos": [
                experimento.__dict__
                for experimento in self.gestion_experimentos.experimentos
            ],
        }
        with open(archivo, "w") as file:
            json.dump(datos, file, default=str)

    def cargar_estado(self, archivo):
        """Carga el estado del programa desde un archivo JSON."""
        with open(archivo, "r") as file:
            datos = json.load(file)
            self.gestion_reactivos.reactivos = [
                Reactivo(**reactivo) for reactivo in datos["reactivos"]
            ]
            self.gestion_experimentos.recetas = [
                Receta(**receta) for receta in datos["recetas"]
            ]
            self.gestion_experimentos.experimentos = [
                Experimento(**experimento) for experimento in datos["experimentos"]
            ]

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system("cls" if os.name == "nt" else "clear")

    def esperar_enter(self):
        """Espera a que el usuario presione Enter para continuar."""
        input("\nPresione Enter para continuar...")

    def mostrar_menu(self):
        """Muestra el menú de opciones para el usuario."""
        self.limpiar_pantalla()
        print("Menú de opciones:")
        print("1. Cargar datos iniciales desde la API")
        print("2. Guardar estado del programa")
        print("3. Cargar estado del programa")
        print("4. Gestión de reactivos")
        print("5. Gestión de experimentos")
        print("6. Gestión de resultados")
        print("7. Indicadores de gestión")
        print("8. Salir")

    def mostrar_menu_reactivos(self):
        """Muestra el submenú de opciones para la gestión de reactivos."""
        self.limpiar_pantalla()
        print("\nGestión de Reactivos:")
        print("1. Agregar reactivo")
        print("2. Eliminar reactivo")
        print("3. Editar reactivo")
        print("4. Listar reactivos")
        print("5. Volver al menú principal")

    def mostrar_menu_experimentos(self):
        """Muestra el submenú de opciones para la gestión de experimentos."""
        self.limpiar_pantalla()
        print("\nGestión de Experimentos:")
        print("1. Agregar experimento")
        print("2. Eliminar experimento")
        print("3. Editar experimento")
        print("4. Listar experimentos")
        print("5. Volver al menú principal")

    def mostrar_menu_resultados(self):
        """Muestra el submenú de opciones para la gestión de resultados."""
        self.limpiar_pantalla()
        print("\nGestión de Resultados:")
        print("1. Agregar resultado")
        print("2. Verificar resultados")
        print("3. Graficar resultados")
        print("4. Volver al menú principal")

    def mostrar_menu_indicadores(self):
        """Muestra el submenú de opciones para los indicadores de gestión."""
        self.limpiar_pantalla()
        print("\nIndicadores de Gestión:")
        print("1. Investigadores que más utilizan el laboratorio")
        print("2. Experimento más hecho y menos hecho")
        print("3. Reactivos con más alta rotación")
        print("4. Reactivos con mayor desperdicio")
        print("5. Reactivos que más se vencen")
        print("6. Experimentos no realizados por falta de reactivos")
        print("7. Graficar estadísticas")
        print("8. Volver al menú principal")

    def validar_entrada(self, tipo, mensaje, condicion=None):
        """Valida la entrada del usuario."""
        while True:
            entrada = input(mensaje)
            try:
                if tipo == int:
                    valor = int(entrada)
                elif tipo == float:
                    valor = float(entrada)
                elif tipo == str:
                    valor = str(entrada)
                if condicion and not condicion(valor):
                    raise ValueError("Condición no cumplida.")
                return valor
            except ValueError:
                print(f"Entrada inválida. Por favor, ingrese un valor {tipo.__name__}.")

    def gestionar_reactivos(self):
        """Permite gestionar los reactivos del laboratorio."""
        while True:
            self.mostrar_menu_reactivos()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                id = self.validar_entrada(str, "ID: ")
                nombre = self.validar_entrada(str, "Nombre: ")
                descripcion = self.validar_entrada(str, "Descripción: ")
                costo = self.validar_entrada(float, "Costo: ")
                categoria = self.validar_entrada(str, "Categoría: ")
                inventario_disponible = self.validar_entrada(
                    int, "Inventario disponible: "
                )
                unidad_medida = self.validar_entrada(str, "Unidad de medición: ")
                fecha_caducidad = input(
                    "Fecha de caducidad (YYYY-MM-DD) o dejar en blanco: "
                )
                fecha_caducidad = (
                    datetime.strptime(fecha_caducidad, "%Y-%m-%d").date()
                    if fecha_caducidad
                    else None
                )
                minimo_sugerido = self.validar_entrada(int, "Mínimo sugerido: ")
                conversiones_posibles = {}
                while True:
                    conversion = input(
                        "Agregar conversión posible (unidad=factor) o dejar en blanco para terminar: "
                    )
                    if not conversion:
                        break
                    try:
                        unidad, factor = conversion.split("=")
                        conversiones_posibles[unidad] = float(factor)
                    except ValueError:
                        print(
                            "Entrada inválida. Por favor, ingrese en el formato unidad=factor."
                        )
                reactivo = Reactivo(
                    id,
                    nombre,
                    descripcion,
                    costo,
                    categoria,
                    inventario_disponible,
                    unidad_medida,
                    fecha_caducidad,
                    minimo_sugerido,
                    conversiones_posibles,
                )
                self.gestion_reactivos.agregar_reactivo(reactivo)
                print("Reactivo agregado.")
                self.esperar_enter()
            elif opcion == "2":
                nombre = self.validar_entrada(str, "Nombre del reactivo a eliminar: ").strip().lower()
                self.gestion_reactivos.eliminar_reactivo(nombre)
                print("Reactivo eliminado.")
                self.esperar_enter()
            elif opcion == "3":
                nombre = self.validar_entrada(str, "Nombre del reactivo a editar: ").strip().lower()
                descripcion = input(
                    "Nueva descripción (dejar en blanco para no cambiar): "
                )
                costo = input("Nuevo costo (dejar en blanco para no cambiar): ")
                categoria = input("Nueva categoría (dejar en blanco para no cambiar): ")
                inventario_disponible = input(
                    "Nuevo inventario (dejar en blanco para no cambiar): "
                )
                unidad_medida = input(
                    "Nueva unidad de medición (dejar en blanco para no cambiar): "
                )
                fecha_caducidad = input(
                    "Nueva fecha de caducidad (YYYY-MM-DD) o dejar en blanco para no cambiar: "
                )
                minimo_sugerido = input(
                    "Nuevo mínimo sugerido (dejar en blanco para no cambiar): "
                )
                conversiones_posibles = {}
                while True:
                    conversion = input(
                        "Agregar conversión posible (unidad=factor) o dejar en blanco para terminar: "
                    )
                    if not conversion:
                        break
                    try:
                        unidad, factor = conversion.split("=")
                        conversiones_posibles[unidad] = float(factor)
                    except ValueError:
                        print(
                            "Entrada inválida. Por favor, ingrese en el formato unidad=factor."
                        )
                cambios = {}
                if descripcion:
                    cambios["descripcion"] = descripcion
                if costo:
                    cambios["costo"] = float(costo)
                if categoria:
                    cambios["categoria"] = categoria
                if inventario_disponible:
                    cambios["inventario_disponible"] = int(inventario_disponible)
                if unidad_medida:
                    cambios["unidad_medida"] = unidad_medida
                if fecha_caducidad:
                    cambios["fecha_caducidad"] = datetime.strptime(
                        fecha_caducidad, "%Y-%m-%d"
                    )
                if minimo_sugerido:
                    cambios["minimo_sugerido"] = int(minimo_sugerido)
                if conversiones_posibles:
                    cambios["conversiones_posibles"] = conversiones_posibles
                self.gestion_reactivos.editar_reactivo(nombre, **cambios)
                print("Reactivo editado.")
                self.esperar_enter()
            elif opcion == "4":
                self.gestion_reactivos.listar_reactivos()
                self.esperar_enter()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def gestionar_experimentos(self):
        """Permite gestionar los experimentos del laboratorio."""
        while True:
            self.mostrar_menu_experimentos()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                receta_nombre = self.validar_entrada(str, "Nombre de la receta: ")
                persona_responsable = self.validar_entrada(str, "Persona responsable: ")
                self.gestion_experimentos.realizar_experimento(
                    receta_nombre, persona_responsable
                )
                self.esperar_enter()
            elif opcion == "2":
                nombre = self.validar_entrada(
                    str, "Nombre del experimento a eliminar: "
                )
                self.gestion_experimentos.eliminar_experimento(nombre)
                print("Experimento eliminado.")
                self.esperar_enter()
            elif opcion == "3":
                nombre = self.validar_entrada(str, "Nombre del experimento a editar: ")
                persona_responsable = input(
                    "Nueva persona responsable (dejar en blanco para no cambiar): "
                )
                fecha = input(
                    "Nueva fecha (YYYY-MM-DD) (dejar en blanco para no cambiar): "
                )
                costo_asociado = input(
                    "Nuevo costo asociado (dejar en blanco para no cambiar): "
                )
                resultado = input("Nuevo resultado (dejar en blanco para no cambiar): ")
                cambios = {}
                if persona_responsable:
                    cambios["persona_responsable"] = persona_responsable
                if fecha:
                    cambios["fecha"] = datetime.strptime(fecha, "%Y-%m-%d")
                if costo_asociado:
                    cambios["costo_asociado"] = float(costo_asociado)
                if resultado:
                    cambios["resultado"] = resultado
                self.gestion_experimentos.editar_experimento(nombre, **cambios)
                print("Experimento editado.")
                self.esperar_enter()
            elif opcion == "4":
                self.gestion_experimentos.listar_experimentos()
                self.esperar_enter()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def gestionar_resultados(self):
        """Permite gestionar los resultados de los experimentos."""
        while True:
            self.mostrar_menu_resultados()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = self.validar_entrada(str, "Nombre del resultado: ")
                valor = self.validar_entrada(float, "Valor: ")
                valor_aceptable_min = self.validar_entrada(
                    float, "Valor aceptable mínimo: "
                )
                valor_aceptable_max = self.validar_entrada(
                    float, "Valor aceptable máximo: "
                )
                resultado = Resultado(
                    nombre, valor, valor_aceptable_min, valor_aceptable_max
                )
                self.gestion_resultados.agregar_resultado(resultado)
                print("Resultado agregado.")
                self.esperar_enter()
            elif opcion == "2":
                self.gestion_resultados.verificar_resultados()
                self.esperar_enter()
            elif opcion == "3":
                self.gestion_resultados.graficar_resultados()
                self.esperar_enter()
            elif opcion == "4":
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def gestionar_indicadores(self):
        """Permite generar estadísticas y gráficos sobre la actividad del laboratorio."""
        while True:
            self.mostrar_menu_indicadores()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                investigadores = self.indicadores_gestion.investigadores_mas_utilizan()
                print("Investigadores que más utilizan el laboratorio:")
                for investigador, cantidad in investigadores:
                    print(f"{investigador}: {cantidad} usos")
                self.esperar_enter()
            elif opcion == "2":
                mas_hecho, menos_hecho = (
                    self.indicadores_gestion.experimento_mas_menos_hecho()
                )
                if mas_hecho:
                    print(
                        f"Experimento más hecho: {mas_hecho[0][0]} ({mas_hecho[0][1]} veces)"
                    )
                else:
                    print("No hay experimentos registrados.")
                if menos_hecho:
                    print(
                        f"Experimento menos hecho: {menos_hecho[0][0]} ({menos_hecho[0][1]} veces)"
                    )
                else:
                    print("No hay experimentos registrados.")
                self.esperar_enter()
            elif opcion == "3":
                reactivos = self.indicadores_gestion.reactivos_mas_alta_rotacion()
                print("Reactivos con más alta rotación:")
                for reactivo, cantidad in reactivos:
                    print(f"{reactivo}: {cantidad} veces")
                self.esperar_enter()
            elif opcion == "4":
                desperdicio = self.indicadores_gestion.reactivos_mayor_desperdicio()
                print("Reactivos con mayor desperdicio:")
                for reactivo, cantidad in desperdicio:
                    print(f"{reactivo}: {cantidad} unidades desperdiciadas")
                self.esperar_enter()
            elif opcion == "5":
                vencidos = self.indicadores_gestion.reactivos_mas_vencen()
                print("Reactivos que más se vencen:")
                for reactivo, cantidad in vencidos:
                    print(f"{reactivo}: {cantidad} veces")
                self.esperar_enter()
            elif opcion == "6":
                no_realizados = (
                    self.indicadores_gestion.experimentos_no_realizados_por_falta_reactivos()
                )
                print(
                    f"Experimentos no realizados por falta de reactivos: {no_realizados} veces"
                )
                self.esperar_enter()
            elif opcion == "7":
                self.indicadores_gestion.graficar_estadisticas()
                self.esperar_enter()
            elif opcion == "8":
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                self.esperar_enter()

    def ejecutar(self):
        """Ejecuta el menú principal del programa."""
        while True:
            self.mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                reactivos, recetas, experimentos = self.cargar_datos_iniciales()
                # Cargar reactivos
                for r in reactivos:
                    reactivo = Reactivo(**r)
                    self.gestion_reactivos.agregar_reactivo(reactivo)
                # Cargar recetas
                for r in recetas:
                    receta = Receta(**r)
                    self.gestion_experimentos.agregar_receta(receta)
                # Cargar experimentos
                for e in experimentos:
                    experimento = Experimento(**e)
                    self.gestion_experimentos.agregar_experimento(experimento)
                print("Datos iniciales cargados desde la API.")
                self.esperar_enter()
            elif opcion == "2":
                archivo = self.validar_entrada(
                    str, "Ingrese el nombre del archivo para guardar el estado: "
                )
                self.guardar_estado(archivo)
                print("Estado del programa guardado.")
                self.esperar_enter()
            elif opcion == "3":
                archivo = self.validar_entrada(
                    str, "Ingrese el nombre del archivo para cargar el estado: "
                )
                self.cargar_estado(archivo)
                print("Estado del programa cargado.")
                self.esperar_enter()
            elif opcion == "4":
                self.gestionar_reactivos()
            elif opcion == "5":
                self.gestionar_experimentos()
            elif opcion == "6":
                self.gestionar_resultados()
            elif opcion == "7":
                self.gestionar_indicadores()
            elif opcion == "8":
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                self.esperar_enter()
