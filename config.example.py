"""
Configuración de ejemplo para el Sistema de Registro Médico COVID-19
IMPORTANTE: Copia este archivo como 'config.py' y configura tus credenciales
"""

# Configuración de la base de datos MySQL
CONFIGURACION_BD = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'database': 'sistema_covid'
}

# Síntomas disponibles en el sistema
LISTA_SINTOMAS = [
    "Fiebre",
    "Tos seca",
    "Fatiga",
    "Pérdida de olfato y gusto",
    "Dolor de garganta",
    "Dolor de cabeza",
    "Dolor muscular",
    "Dificultad para respirar",
    "Escalofríos",
    "Náuseas",
    "Diarrea",
    "Congestión nasal"
]

# Síntomas principales de COVID-19 (se requieren los 3 para diagnóstico positivo)
SINTOMAS_COVID = ["Fiebre", "Fatiga", "Pérdida de olfato y gusto"]
