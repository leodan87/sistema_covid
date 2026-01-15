# Sistema de Registro Médico COVID-19

Sistema de gestión hospitalaria para registro y seguimiento de pacientes COVID-19, desarrollado con Python, Tkinter y MySQL.

---

## CONFIGURACIÓN INICIAL (IMPORTANTE)

### PASO 1: Configurar contraseña de MySQL

1. Copie el archivo `config.example.py`
2. Renómbrelo como `config.py`
3. Abra `config.py` y en la línea 12 escriba su contraseña de MySQL:
   ```python
   'password': 'su_contraseña_aqui',
   ```
4. Guarde el archivo

### PASO 2: Instalar dependencias

```bash
pip install mysql-connector-python
```

### PASO 3: Crear base de datos

```bash
mysql -u root -p < database/crear_base_datos.sql
```

### PASO 4: Ejecutar sistema

```bash
python main.py
```

---

## GUÍA DE PRUEBAS PARA EVALUACIÓN

### Pacientes de Prueba Disponibles

| Historia | Cédula     | Nombre                |
|----------|------------|-----------------------|
| HL-001   | 0912345678 | Martha Camacho Toledo |
| HL-002   | 0923456789 | Carlos Jimenez Torres |

### Prueba 1: Diagnóstico POSITIVO

1. Pestaña "Registro de Pacientes"
2. Buscar: HL-001
3. Seleccionar síntomas:
   - Fiebre
   - Fatiga
   - Pérdida de olfato y gusto
4. Clic en "Verificar Diagnóstico COVID"
5. Aparece animación de laboratorio (3 segundos)
6. Resultado: Ventana roja "POSITIVO COVID-19"
7. Escribir prescripción médica
8. Guardar consulta

### Prueba 2: Alerta de Paciente COVID

1. Buscar nuevamente: HL-001
2. Aparece alerta mostrando:
   - Fecha de diagnóstico
   - Días en aislamiento
   - Estado (0-9 días rojo, 10-13 naranja, 14+ verde)

### Prueba 3: Consultar Pacientes COVID

1. Pestaña "Consulta COVID-19"
2. Clic en "Ver Todos"
3. Doble clic en fila para ver tratamiento completo

### Prueba 4: Diagnóstico NEGATIVO

1. Buscar: HL-002
2. Seleccionar: Dolor de cabeza + Tos seca
3. Verificar diagnóstico
4. Resultado: Ventana verde "NEGATIVO COVID-19"

---

## CRITERIO DE DIAGNÓSTICO

El sistema diagnostica **POSITIVO** solo cuando el paciente tiene LOS 3 SÍNTOMAS OBLIGATORIOS:

1. Fiebre
2. Fatiga
3. Pérdida de olfato y gusto

Si falta alguno de estos 3 síntomas, el resultado es NEGATIVO.

### Ejemplos de Diagnóstico

| Síntomas Seleccionados                       | Resultado  | Razón                            |
|---------------------------------------------|------------|----------------------------------|
| Fiebre + Fatiga + Pérdida olfato            | POSITIVO   | Tiene los 3 obligatorios         |
| Fiebre + Fatiga + Tos                       | NEGATIVO   | Falta pérdida de olfato          |
| Fiebre + Pérdida olfato                     | NEGATIVO   | Falta fatiga                     |
| Dolor cabeza + Tos + Congestión             | NEGATIVO   | No tiene ninguno de los 3        |

### Síntomas Disponibles (máximo 4 por consulta)

1. Fiebre (obligatorio para COVID+)
2. Fatiga (obligatorio para COVID+)
3. Pérdida de olfato y gusto (obligatorio para COVID+)
4. Tos seca
5. Dolor de cabeza
6. Dolor muscular
7. Dificultad para respirar
8. Escalofríos
9. Congestión nasal
10. Dolor de garganta

---

## CARACTERÍSTICAS PRINCIPALES

### Ventanas Profesionales

- Ventana "Paciente No Encontrado" con diseño hospitalario
- Ventana "Paciente Guardado" con confirmación verde
- Animación de laboratorio (3 segundos) con puntos animados
- Resultado COVID con colores diferenciados (rojo=positivo, verde=negativo)
- Alerta automática mostrando días de aislamiento con estados por color
- Ventana "Consulta Guardada" con diseño consistente

### Tabla COVID-19

- Filas con colores alternados (azul claro/blanco)
- Doble clic para ver tratamiento completo
- Filtro por fecha (formato: AAAA-MM-DD)
- 6 columnas: Historia, Cédula, Nombres, Fecha, Diagnóstico, Tratamiento

### Funcionalidades

- Registro de pacientes con validaciones
- Búsqueda por historia laboral
- Diagnóstico automático basado en síntomas
- Cálculo de días en aislamiento
- Icono personalizado de hospital

---

## ESTRUCTURA DE LA BASE DE DATOS

### Tabla: pacientes

| Campo              | Tipo         | Descripción                    |
|--------------------|--------------|--------------------------------|
| id                 | INT (PK)     | Identificador único            |
| historia_laboral   | VARCHAR(20)  | Historia laboral (ÚNICO)       |
| cedula             | VARCHAR(10)  | Cédula (ÚNICO)                 |
| nombres_completos  | VARCHAR(100) | Nombres completos              |
| telefono           | VARCHAR(15)  | Teléfono                       |
| direccion          | VARCHAR(200) | Dirección                      |
| fecha_registro     | TIMESTAMP    | Fecha de registro              |

### Tabla: consultas

| Campo               | Tipo        | Descripción                      |
|---------------------|-------------|----------------------------------|
| id                  | INT (PK)    | Identificador único              |
| paciente_id         | INT (FK)    | Referencia a pacientes(id)       |
| fecha_consulta      | DATE        | Fecha de consulta                |
| sintoma_1           | VARCHAR(50) | Primer síntoma                   |
| sintoma_2           | VARCHAR(50) | Segundo síntoma                  |
| sintoma_3           | VARCHAR(50) | Tercer síntoma                   |
| sintoma_4           | VARCHAR(50) | Cuarto síntoma                   |
| diagnostico_covid   | BOOLEAN     | TRUE=Positivo, FALSE=Negativo    |
| prescripcion_medica | TEXT        | Tratamiento recetado             |

---

## SOLUCIÓN DE PROBLEMAS

### Error: "Access denied for user 'root'"
- Verifique que la contraseña en config.py sea correcta

### Error: "Unknown database 'sistema_covid'"
- Ejecute: `mysql -u root -p < database/crear_base_datos.sql`

### Error: "No module named 'mysql.connector'"
- Ejecute: `pip install mysql-connector-python`

### Error: "No such file: 'config.py'"
- Copie config.example.py y renómbrelo como config.py
- Agregue su contraseña de MySQL

### No aparecen datos en tabla COVID-19
- Registre al menos una consulta con diagnóstico positivo
- Use los 3 síntomas obligatorios: Fiebre + Fatiga + Pérdida de olfato

---

## TECNOLOGÍAS

- Python 3.7+
- Tkinter (interfaz gráfica)
- MySQL 8.0
- mysql-connector-python

---

## ESTRUCTURA DEL PROYECTO

```
sistema_covid/
├── main.py                   # Ejecutar este archivo
├── config.py                 # Crear desde config.example.py
├── config.example.py         # Plantilla de configuración
├── database.py               # Funciones de base de datos
├── paciente.py               # Módulo de registro
├── consulta.py               # Módulo de consulta
├── README.md                 # Documentación
├── INSTRUCCIONES.txt         # Instrucciones rápidas
├── .gitignore                # Archivos ignorados
├── database/
│   └── crear_base_datos.sql # Script SQL
└── assets/
    └── hospital_icon.ico    # Icono personalizado
```

---

## REPOSITORIO GITHUB

https://github.com/leodan87/sistema_covid

Para clonar:
```bash
git clone https://github.com/leodan87/sistema_covid.git
cd sistema_covid
```

---

## RESUMEN PARA EVALUACIÓN

### Funcionalidades Implementadas

- Conexión a MySQL con 2 tablas relacionadas
- Interfaz gráfica profesional con 6 ventanas modales
- Diagnóstico automático con criterio médico
- Animación de laboratorio (3 segundos)
- Sistema de alertas por estado de aislamiento
- Tabla con colores alternados y funcionalidad de doble clic
- Validaciones de datos y manejo de errores
- Documentación completa
- Seguridad: config.py excluido de Git

### Pruebas Sugeridas (10 minutos)

1. Buscar paciente HL-001 y ver alerta COVID
2. Diagnosticar POSITIVO con 3 síntomas obligatorios
3. Ver tabla de pacientes COVID con colores alternados
4. Diagnosticar NEGATIVO con otros síntomas
5. Filtrar por fecha en tabla
6. Doble clic en fila para ver tratamiento

---

Desarrollado como proyecto académico de gestión médica COVID-19.
