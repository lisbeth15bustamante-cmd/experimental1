from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo,
    imprimir_exito,
    imprimir_error,
    imprimir_info,
    confirmar,
)
from views import (
    crear_estudiante,
    obtener_todos,
    obtener_por_id,
    buscar_estudiantes,
    actualizar_estudiante,
    eliminar_estudiante,
    registrar_nota,
    materias_ofertadas,
    estudiantes_en_comun,
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(
        f"{'ID':<5}{'CARNET':<12}{'NOMBRE':<25}{'EMAIL':<28}{'PROMEDIO':<10}"
    )
    print("-" * 80)
    for est in estudiantes:
        print(
            f"{est.id:<5}{est.carnet:<12}{est.obtener_nombre_completo():<25}"
            f"{est.email:<28}{est.obtener_promedio():<10}"
        )
    print("-" * 80)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


def opcion_crear():
    imprimir_titulo("REGISTRAR NUEVO ESTUDIANTE")
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_ver_todos():
    imprimir_titulo("LISTA GENERAL DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("No hay estudiantes registrados.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTES")
    termino = input("Ingrese término de búsqueda (Nombre, Carnet, Email): ")
    resultados = buscar_estudiantes(termino)
    if not resultados:
        imprimir_info("No se encontraron coincidencias.")
    else:
        mostrar_tabla(resultados)
    pausa()


def opcion_ver_por_id():
    imprimir_titulo("CONSULTAR ESTUDIANTE POR ID")
    try:
        id_est = int(input("Ingrese el ID: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"Estudiante ID {id_est} no encontrado.")
    else:
        dic = est.a_diccionario()
        print()
        for k, v in dic.items():
            print(f"  {k.capitalize():<15}: {v}")
    pausa()


def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR DATOS DE ESTUDIANTE")
    try:
        id_est = int(input("Ingrese el ID del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    print(
        f"Editando a: {est.obtener_nombre_completo()}. (Deje el campo vacío para no modificarlo)\n"
    )

    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        valor_actual = getattr(est, campo)
        nuevo_valor = input(f"{campo.capitalize()} [{valor_actual}]: ").strip()
        if nuevo_valor:
            cambios[campo] = nuevo_valor

    exito, mensaje = actualizar_estudiante(id_est, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_est = int(input("Ingrese el ID a eliminar: "))
    except ValueError:
        imprimir_error("El ID debe ser entero.")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe estudiante con ID {id_est}")
        return pausa()

    imprimir_info(f"Se eliminará a: {est.obtener_nombre_completo()}")
    if confirmar("¿Está seguro de eliminar este registro?"):
        exito, mensaje = eliminar_estudiante(id_est)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada.")
    pausa()


def opcion_agregar_nota():
    imprimir_titulo("REGISTRAR NOTA / ASIGNATURA")
    try:
        id_est = int(input("ID del Estudiante: "))
        materia = input("Materia: ")
        nota = float(input("Nota (0 a 20): "))
    except ValueError:
        imprimir_error("Los campos ID y Nota deben ser numéricos.")
        return pausa()

    exito, mensaje = registrar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


def opcion_materias_ofertadas():
    imprimir_titulo("MATERIAS REGISTRADAS (UNIÓN DE CONJUNTOS)")
    materias = materias_ofertadas()
    if not materias:
        imprimir_info("No hay materias registradas en ningún estudiante.")
    else:
        print("Listado global de materias en el sistema:")
        for idx, mat in enumerate(materias, 1):
            print(f"  {idx}. {mat}")
    pausa()


def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN (INTERSECCIÓN DE CONJUNTOS)")
    try:
        id_a = int(input("ID Estudiante 1: "))
        id_b = int(input("ID Estudiante 2: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números enteros.")
        return pausa()

    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    else:
        print(
            f"\nMaterias compartidas entre '{resultado['estudiante_a']}' y '{resultado['estudiante_b']}':"
        )
        materias = resultado["materias"]
        if not materias:
            imprimir_info("No comparten ninguna materia.")
        else:
            imprimir_exito(f"Comparten {len(materias)} materia(s):")
            for m in materias:
                print(f"  • {m}")
    pausa()


def salir():
    imprimir_info("¡Gracias por utilizar el sistema!")
    return "salir"


OPCIONES = {
    "1": ("Registrar estudiante", opcion_crear),
    "2": ("Ver lista general", opcion_ver_todos),
    "3": ("Buscar estudiante", opcion_buscar),
    "4": ("Consultar por ID", opcion_ver_por_id),
    "5": ("Actualizar datos", opcion_actualizar),
    "6": ("Eliminar estudiante", opcion_eliminar),
    "7": ("Agregar nota / materia", opcion_agregar_nota),
    "8": ("Ver materias ofertadas (Set Union)", opcion_materias_ofertadas),
    "9": (
        "Ver materias en común (Set Intersect)",
        opcion_materias_en_comun,
    ),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA ACADÉMICO - GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:
            imprimir_error("Opción inválida.")
            pausa()
            continue

        _, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nEjecución finalizada por el usuario.")