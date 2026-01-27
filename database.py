"""
Funciones para interactuar con la base de datos MySQL
"""

import mysql.connector
from tkinter import messagebox
from config import CONFIGURACION_BD


def conectar():
    """Conecta a la base de datos MySQL"""
    try:
        conexion = mysql.connector.connect(**CONFIGURACION_BD)
        return conexion
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"No se pudo conectar a MySQL:\n{error}")
        return None


def buscar_paciente_por_historia(historia_laboral):
    """Busca un paciente por su historia clínica"""
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM pacientes WHERE historia_laboral = %s",
            (historia_laboral,)
        )
        paciente = cursor.fetchone()
        return paciente
    finally:
        cursor.close()
        conexion.close()


def verificar_covid_paciente(paciente_id):
    """Verifica si un paciente tiene diagnóstico COVID-19 activo"""
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT fecha_consulta, prescripcion_medica
            FROM consultas
            WHERE paciente_id = %s AND diagnostico_covid = TRUE
            ORDER BY fecha_consulta DESC
            LIMIT 1
        """, (paciente_id,))
        resultado = cursor.fetchone()
        return resultado
    finally:
        cursor.close()
        conexion.close()


def guardar_paciente(datos, paciente_id=None):
    """
    Guarda un paciente nuevo o actualiza uno existente.
    datos = (historia, cedula, nombres, telefono, direccion)
    """
    conexion = conectar()
    if not conexion:
        return None

    try:
        cursor = conexion.cursor()

        if paciente_id:
            # Actualizar existente
            cursor.execute("""
                UPDATE pacientes SET
                    historia_laboral=%s, cedula=%s, nombres_completos=%s,
                    telefono=%s, direccion=%s
                WHERE id=%s
            """, (*datos, paciente_id))
        else:
            # Insertar nuevo
            cursor.execute("""
                INSERT INTO pacientes
                (historia_laboral, cedula, nombres_completos, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s)
            """, datos)
            paciente_id = cursor.lastrowid

        conexion.commit()
        return paciente_id

    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Ya existe un paciente con esa historia o cédula.")
        return None
    finally:
        cursor.close()
        conexion.close()


def guardar_consulta(paciente_id, fecha, sintomas, es_covid, prescripcion):
    """Guarda una consulta médica"""
    conexion = conectar()
    if not conexion:
        return False

    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO consultas
            (paciente_id, fecha_consulta, sintoma_1, sintoma_2, sintoma_3, sintoma_4,
             diagnostico_covid, prescripcion_medica)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (paciente_id, fecha, *sintomas, es_covid, prescripcion))

        conexion.commit()
        return True
    finally:
        cursor.close()
        conexion.close()


def obtener_pacientes_covid(fecha=None):
    """Obtiene pacientes con COVID, opcionalmente filtrados por fecha"""
    conexion = conectar()
    if not conexion:
        return []

    try:
        cursor = conexion.cursor(dictionary=True)

        if fecha:
            cursor.execute("""
                SELECT p.historia_laboral, p.cedula, p.nombres_completos,
                       c.fecha_consulta, c.prescripcion_medica
                FROM consultas c
                JOIN pacientes p ON c.paciente_id = p.id
                WHERE c.diagnostico_covid = TRUE AND c.fecha_consulta = %s
                ORDER BY c.fecha_consulta DESC
            """, (fecha,))
        else:
            cursor.execute("""
                SELECT p.historia_laboral, p.cedula, p.nombres_completos,
                       c.fecha_consulta, c.prescripcion_medica
                FROM consultas c
                JOIN pacientes p ON c.paciente_id = p.id
                WHERE c.diagnostico_covid = TRUE
                ORDER BY c.fecha_consulta DESC
            """)

        return cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()
