# ============================================================
# herramientas.py
# Funciones de ayuda que usa todo el proyecto: limpiar la
# pantalla, imprimir texto con colores, pedir confirmación
# al usuario y validar correos electrónicos.
# ============================================================

import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


def limpiar_pantalla():
    """Borra todo lo que hay escrito en la consola."""
    os.system("clear" if os.name == "posix" else "cls")


def imprimir_color(texto, color):
    """Muestra un texto en pantalla con el color indicado."""
    codigo = COLORES.get(color, COLORES["BLANCO"])
    print(f"{codigo}{texto}{COLORES['RESET']}")


def imprimir_titulo(texto):
    """Limpia la pantalla y muestra un título centrado entre dos líneas de '=' en color azul."""
    limpiar_pantalla()
    imprimir_color("=" * 60, "AZUL")
    print(f"  {texto}".center(60))
    imprimir_color("=" * 60, "AZUL")
    print()


def imprimir_exito(mensaje):
    """Muestra un mensaje de éxito en verde con un check ✓ al inicio."""
    imprimir_color(f"✓ {mensaje}", "VERDE")


def imprimir_error(mensaje):
    """Muestra un mensaje de error en rojo con una ✗ al inicio."""
    imprimir_color(f"✗ {mensaje}", "ROJO")


def imprimir_info(mensaje):
    """Muestra un mensaje informativo en cyan con un ℹ al inicio."""
    imprimir_color(f"ℹ {mensaje}", "CYAN")


def confirmar(pregunta):
    """Solicita confirmación al usuario (si/no) basándose en la tupla RESPUESTAS_SI."""
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    return respuesta in RESPUESTAS_SI


def es_email_valido(texto):
    """Valida si la estructura básica de una cadena corresponde a un e-mail."""
    texto = texto.strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")