# TUPLA: Estructura fija con los nombres de campos del estudiante
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


class Estudiante:
    """MODELO: Representa a la entidad Estudiante.

    Aplica el uso de las 4 colecciones:
    - Tupla (tuple): CAMPOS_ESTUDIANTE (Estructura rígida).
    - Diccionario (dict): Estructura general de la entidad y registro de notas por materia.
    - Lista (list): Almacenamiento de notas numéricas.
    - Conjunto (set): Materias inscritas sin elementos duplicados.
    """

    def __init__(
        self,
        id_estudiante,
        nombre,
        apellido,
        email,
        carnet,
        notas=None,
        materias=None,
    ):
        self.id = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.carnet = carnet
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Física": [15]}
        self.notas = notas if notas else {}
        # CONJUNTO: Almacena materias únicas
        self.materias = set(materias) if materias else set()

    def obtener_nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def inscribir_materia(self, materia):
        materia_formateada = materia.strip().title()
        self.materias.add(materia_formateada)

    def agregar_nota(self, materia, nota):
        materia_formateada = materia.strip().title()
        self.inscribir_materia(materia_formateada)
        self.notas.setdefault(materia_formateada, []).append(nota)

    def obtener_promedio(self):
        todas_las_notas = []
        for lista in self.notas.values():
            todas_las_notas.extend(lista)
        if not todas_las_notas:
            return 0.0
        return round(sum(todas_las_notas) / len(todas_las_notas), 2)

    def materias_en_comun(self, otro_estudiante):
        # Operación de INTERSECCIÓN entre dos conjuntos (sets)
        return self.materias & otro_estudiante.materias

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # Se convierte el conjunto a lista ordenada para poder serializar en JSON
            "materias": sorted(list(self.materias)),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            # Al reconstruir el objeto se pasa la lista recibida a un set
            materias=set(datos.get("materias", [])),
        )

    def __str__(self):
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"