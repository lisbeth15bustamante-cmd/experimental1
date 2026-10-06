from models import Estudiante, CAMPOS_ESTUDIANTE
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor = GestorJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


def carnets_registrados(excepto_id=None):
    """CONJUNTO: Búsqueda rápida O(1) de carnets existentes."""
    return {
        reg["carnet"].upper()
        for reg in gestor.leer()
        if reg["id"] != excepto_id
    }


def emails_registrados(excepto_id=None):
    """CONJUNTO: Búsqueda rápida O(1) de emails existentes."""
    return {
        reg["email"].lower()
        for reg in gestor.leer()
        if reg["id"] != excepto_id
    }


def siguiente_id():
    ids = [reg["id"] for reg in gestor.leer()]
    return max(ids) + 1 if ids else 1


# ===================== OPERACIONES CRUD =====================


def crear_estudiante(datos):
    try:
        valores = {
            campo: str(datos.get(campo, "")).strip()
            for campo in CAMPOS_ESTUDIANTE
        }

        faltantes = [
            campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]
        ]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no es válido."

        if valores["email"].lower() in emails_registrados():
            return False, "El email ingresado ya está registrado."

        if valores["carnet"].upper() in carnets_registrados():
            return False, f"El carnet '{valores['carnet']}' ya pertenece a otro estudiante."

        estudiante = Estudiante(
            siguiente_id(),
            valores["nombre"],
            valores["apellido"],
            valores["email"],
            valores["carnet"].upper(),
        )

        registros = gestor.leer()
        registros.append(estudiante.a_diccionario())

        if gestor.guardar(registros):
            return (
                True,
                f"Estudiante '{estudiante.obtener_nombre_completo()}' guardado exitosamente con ID {estudiante.id}.",
            )
        return False, "Error al escribir en el archivo JSON."

    except Exception as e:
        return False, f"Error inesperado: {e}"


def obtener_todos():
    return [Estudiante.desde_diccionario(reg) for reg in gestor.leer()]


def obtener_por_id(id_estudiante):
    for est in obtener_todos():
        if est.id == id_estudiante:
            return est
    return None


def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []

    encontrados = []
    for reg in gestor.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(reg.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(reg))
                break
    return encontrados


def actualizar_estudiante(id_estudiante, cambios):
    try:
        # Uso de diferencia de conjuntos para encontrar claves inválidas
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se proporcionaron cambios para actualizar."

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email ingresado no es válido."
            if cambios["email"].lower() in emails_registrados(
                excepto_id=id_estudiante
            ):
                return False, "El email ya pertenece a otro estudiante."

        if "carnet" in cambios:
            carnet_nuevo = cambios["carnet"].upper()
            if carnet_nuevo in carnets_registrados(excepto_id=id_estudiante):
                return False, f"El carnet '{carnet_nuevo}' ya está registrado."
            cambios["carnet"] = carnet_nuevo

        registros = gestor.leer()
        posicion = None
        for idx, reg in enumerate(registros):
            if reg["id"] == id_estudiante:
                posicion = idx
                break

        if posicion is None:
            return False, f"No existe ningún estudiante con el ID {id_estudiante}."

        registros[posicion].update(cambios)
        gestor.guardar(registros)
        return (
            True,
            f"Estudiante ID {id_estudiante} ha sido actualizado correctamente.",
        )

    except Exception as e:
        return False, f"Error inesperado: {e}"


def eliminar_estudiante(id_estudiante):
    registros = gestor.leer()
    filtrados = [reg for reg in registros if reg["id"] != id_estudiante]

    if len(filtrados) == len(registros):
        return False, f"No existe el estudiante con ID {id_estudiante}."

    gestor.guardar(filtrados)
    return True, f"Estudiante con ID {id_estudiante} fue eliminado con éxito."


# ===================== FUNCIONES DE CONJUNTOS / NOTAS =====================


def registrar_nota(id_estudiante, materia, nota):
    if not (0 <= nota <= 20):
        return False, "La nota debe estar comprendida entre 0 y 20."

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        return False, f"No existe estudiante con ID {id_estudiante}."

    estudiante.agregar_nota(materia, nota)

    registros = gestor.leer()
    for idx, reg in enumerate(registros):
        if reg["id"] == id_estudiante:
            registros[idx] = estudiante.a_diccionario()
            break

    gestor.guardar(registros)
    return (
        True,
        f"Se agregó la nota {nota} en '{materia.strip().title()}' a {estudiante.obtener_nombre_completo()}.",
    )


def materias_ofertadas():
    """UNIÓN DE CONJUNTOS: Obtiene la lista completa de materias registradas."""
    todas = set()
    for est in obtener_todos():
        todas |= est.materias
    return sorted(list(todas))


def estudiantes_en_comun(id_a, id_b):
    """INTERSECCIÓN DE CONJUNTOS: Encuentra materias compartidas entre dos estudiantes."""
    est_a = obtener_por_id(id_a)
    est_b = obtener_por_id(id_b)

    if not est_a:
        return False, f"Estudiante ID {id_a} no encontrado."
    if not est_b:
        return False, f"Estudiante ID {id_b} no encontrado."

    comunes = est_a.materias_en_comun(est_b)
    return True, {
        "estudiante_a": est_a.obtener_nombre_completo(),
        "estudiante_b": est_b.obtener_nombre_completo(),
        "materias": sorted(list(comunes)),
    }