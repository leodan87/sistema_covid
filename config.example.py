# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CONEXIÓN A MySQL
# ═══════════════════════════════════════════════════════════════
#    IMPORTANTE - ANTES DE EJECUTAR:
# 1. Copia este archivo y renómbralo como 'config.py'
# 2. Cambia 'tu_contraseña' por tu contraseña de MySQL
# 3. Si tu usuario no es 'root', cámbialo también
# 4. Guarda el archivo antes de ejecutar la aplicación
# ═══════════════════════════════════════════════════════════════
CONFIGURACION_BD = {
    'host': 'localhost',
    'user': 'root',              # Usuario de MySQL (normalmente es 'root')
    'password': '',              # ← COLOCA AQUÍ TU CONTRASEÑA DE MySQL
    'database': 'sistema_covid'
}

# ═══════════════════════════════════════════════════════════
# LISTA DE SÍNTOMAS DISPONIBLES
# ═══════════════════════════════════════════════════════════
# Estos son todos los síntomas que el médico puede seleccionar
# para cada paciente (máximo 4 síntomas por consulta)
LISTA_SINTOMAS = [
    "Fiebre",
    "Fatiga",
    "Pérdida de olfato y gusto",
    "Tos seca",
    "Dolor de cabeza",
    "Dolor muscular",
    "Dificultad para respirar",
    "Escalofríos",
    "Congestión nasal",
    "Dolor de garganta"
]

# ═══════════════════════════════════════════════════════════
# CRITERIO DE DIAGNÓSTICO COVID-19
# ═══════════════════════════════════════════════════════════
#    IMPORTANTE PARA EVALUACIÓN:
# Para que el diagnóstico sea POSITIVO COVID-19, el paciente
# DEBE tener los 3 síntomas siguientes:
#   1. Fiebre
#   2. Fatiga
#   3. Pérdida de olfato y gusto
#
# Si tiene menos de 3 de estos síntomas → NEGATIVO COVID-19
# Si tiene los 3 síntomas → POSITIVO COVID-19
# ═══════════════════════════════════════════════════════════
SINTOMAS_COVID = ["Fiebre", "Fatiga", "Pérdida de olfato y gusto"]
