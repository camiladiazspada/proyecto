class Reactivo:
    def __init__(
        self,
        id,
        nombre,
        descripcion,
        costo,
        categoria,
        inventario_disponible,
        unidad_medida,
        fecha_caducidad=None,
        minimo_sugerido=0,
        conversiones_posibles=None,
    ):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario_disponible = inventario_disponible
        self.unidad_medida = unidad_medida
        self.fecha_caducidad = fecha_caducidad
        self.minimo_sugerido = minimo_sugerido
        self.conversiones_posibles = conversiones_posibles or {}

    def __str__(self):
        return f"{self.nombre} ({self.categoria}): {self.descripcion} - {self.inventario_disponible} {self.unidad_medida} disponibles, costo: {self.costo}, caducidad: {self.fecha_caducidad}"

    def cambiar_unidad_medicion(self, nueva_unidad):
        if nueva_unidad in self.conversiones_posibles:
            factor_conversion = self.conversiones_posibles[nueva_unidad]
            self.inventario_disponible *= factor_conversion
            self.unidad_medida = nueva_unidad
        else:
            print(f"No se puede convertir de {self.unidad_medida} a {nueva_unidad}")
