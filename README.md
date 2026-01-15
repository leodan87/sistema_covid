# Sistema de Registro Médico COVID-19

Sistema profesional de gestión hospitalaria para el registro y seguimiento de pacientes con COVID-19, desarrollado con Python y Tkinter.

## Descripción del Proyecto

Sistema integral de gestión médica que permite:
- Registro completo de pacientes con validación de datos
- Búsqueda rápida por historia laboral
- Registro de consultas médicas con análisis de síntomas
- Diagnóstico automático de COVID-19 con animación de laboratorio
- Sistema de alertas para pacientes con COVID-19
- Consulta de historial de pacientes diagnosticados
- Interfaz gráfica profesional estilo hospitalario

---

## Características Principales

### Módulo de Registro de Pacientes
- Búsqueda de pacientes por historia laboral
- Validación de cédula ecuatoriana (10 dígitos)
- Registro de datos: historia laboral, cédula, nombres completos, teléfono y dirección
- Botón de guardar paciente con confirmación visual profesional
- Alerta automática cuando se busca un paciente con COVID-19 registrado
- Indicador del estado de aislamiento según días transcurridos

### Diagnóstico COVID-19
- Selección de hasta 4 síntomas simultáneos
- Verificación de diagnóstico con animación de análisis de laboratorio
- Lógica de diagnóstico: requiere los 3 síntomas principales (Fiebre, Fatiga, Pérdida de olfato y gusto)
- Ventana de resultados profesional con indicaciones médicas
- Diferenciación visual entre casos positivos (rojo) y negativos (verde)

### Consultas Médicas
- Registro de síntomas con lista desplegable de 12 opciones
- Campo de prescripción médica
- Guardado automático con fecha actual
- Confirmación visual al guardar consulta

### Consulta de Pacientes COVID-19
- Tabla profesional con filas de colores alternados para mejor lectura
- Columnas: Historia Laboral, Cédula, Nombres, Fecha, Diagnóstico, Tratamiento
- Filtrado por fecha específica
- Opción "Ver Todos" para consulta general
- Doble clic en cualquier fila para ver tratamiento completo
- Encabezados con estilo profesional

### Sistema de Alertas
Cuando se busca un paciente con COVID-19, el sistema muestra:
- Fecha de diagnóstico
- Días transcurridos en aislamiento
- Estado automático según período:
  - 0-9 días: EN AISLAMIENTO - RECUPERACIÓN EN PROCESO (rojo)
  - 10-13 días: PERÍODO FINAL DE AISLAMIENTO (naranja)
  - 14+ días: PERÍODO DE AISLAMIENTO CUMPLIDO (verde)
- Recordatorio de protocolos de bioseguridad

---

## Requisitos Previos

1. **Python 3.7 o superior**
2. **MySQL Server 8.0** (instalado y en ejecución)
3. **Librerías Python:**
   - `mysql-connector-python`
   - `tkinter` (incluida con Python)

---

## Instalación y Configuración

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/leodan87/sistema_covid.git
cd sistema_covid
```

### Paso 2: Instalar dependencias

```bash
pip install mysql-connector-python
```

### Paso 3: Configurar MySQL

1. Abre el archivo **`config.py`**
2. Modifica las credenciales de MySQL:

```python
CONFIGURACION_BD = {
    'host': 'localhost',
    'user': 'root',              # Tu usuario de MySQL
    'password': 'TU_CONTRASEÑA', # COLOCA AQUÍ TU CONTRASEÑA
    'database': 'sistema_covid'
}
```

### Paso 4: Crear la base de datos

Ejecuta el script SQL ubicado en `database/crear_base_datos.sql`:

**Opción A - Desde línea de comandos:**
```bash
mysql -u root -p < database/crear_base_datos.sql
```

**Opción B - Desde MySQL Workbench:**
1. Abre MySQL Workbench
2. Abre el archivo `database/crear_base_datos.sql`
3. Ejecuta el script completo

### Paso 5: Ejecutar la aplicación

```bash
python main.py
```

---

## Criterio de Diagnóstico COVID-19

**IMPORTANTE:** El sistema diagnostica **POSITIVO COVID-19** cuando el paciente presenta **LOS 3 SÍNTOMAS OBLIGATORIOS**:

1. Fiebre
2. Fatiga
3. Pérdida de olfato y gusto

**Ejemplos de diagnóstico:**

| Síntomas Seleccionados | Resultado |
|------------------------|-----------|
| Fiebre + Fatiga + Pérdida de olfato y gusto | POSITIVO COVID-19 |
| Fiebre + Fatiga + Tos seca | NEGATIVO COVID-19 |
| Fiebre + Pérdida de olfato y gusto | NEGATIVO COVID-19 |
| Solo Fiebre | NEGATIVO COVID-19 |

---

## Manual de Uso

### Pestaña "Registro de Pacientes"

**1. Buscar paciente existente:**
- Ingresa la Historia Laboral (ejemplo: HL-001)
- Clic en "Buscar"
- Si tiene COVID-19 registrado, aparecerá una alerta con su estado de aislamiento

**2. Registrar nuevo paciente:**
- Clic en "Nuevo" para limpiar formulario
- Completa todos los campos requeridos
- La cédula debe tener exactamente 10 dígitos
- Clic en "Guardar Paciente"

**3. Registrar consulta médica:**
- Con un paciente cargado, selecciona hasta 4 síntomas de las listas desplegables
- Clic en "Verificar Diagnóstico COVID" para ver animación y resultado
- Ingresa la prescripción médica en el campo de texto
- Clic en "Guardar Consulta" para registrar

### Pestaña "Consulta COVID-19"

**1. Ver todos los pacientes COVID:**
- Clic en "Ver Todos" para mostrar todos los casos registrados

**2. Filtrar por fecha:**
- Ingresa fecha en formato AAAA-MM-DD (ejemplo: 2026-01-15)
- Clic en "Consultar"

**3. Ver tratamiento completo:**
- Doble clic en cualquier fila para abrir ventana con tratamiento completo

---

## Estructura del Proyecto

```
sistema_covid/
│
├── main.py                    # Punto de entrada de la aplicación
├── config.py                  # Configuración de BD y síntomas
├── config.example.py          # Ejemplo de configuración
├── database.py                # Funciones de acceso a datos
├── paciente.py                # Módulo de registro de pacientes
├── consulta.py                # Módulo de consulta COVID-19
├── README.md                  # Documentación
├── INSTRUCCIONES.txt          # Instrucciones del proyecto
├── .gitignore                 # Archivos ignorados por Git
│
├── database/
│   └── crear_base_datos.sql  # Script de creación de BD
│
└── assets/
    └── hospital_icon.ico      # Ícono personalizado del sistema
```

---

## Base de Datos

### Tablas principales:

**pacientes**
- `id` (PK, AUTO_INCREMENT)
- `historia_laboral` (UNIQUE)
- `cedula` (UNIQUE)
- `nombres_completos`
- `telefono`
- `direccion`
- `fecha_registro`

**consultas**
- `id` (PK, AUTO_INCREMENT)
- `paciente_id` (FK -> pacientes)
- `fecha_consulta`
- `sintoma_1`, `sintoma_2`, `sintoma_3`, `sintoma_4`
- `diagnostico_covid` (BOOLEAN)
- `prescripcion_medica` (TEXT)

---

## Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación
- **Tkinter** - Biblioteca para interfaz gráfica
- **MySQL 8.0** - Sistema de gestión de base de datos
- **mysql-connector-python** - Conector Python-MySQL

---

## Características de la Interfaz

### Ventanas Profesionales
- Ventana de paciente no encontrado con diseño hospitalario
- Ventana de confirmación al guardar paciente
- Animación de análisis de laboratorio (3 segundos con puntos animados)
- Ventana de resultado COVID-19 con colores diferenciados
- Alerta de paciente con COVID-19 con estado de aislamiento
- Ventana de confirmación al guardar consulta

### Tabla de Consultas COVID-19
- Filas con colores alternados (azul claro y blanco) para mejor lectura
- Encabezados con fondo oscuro y texto blanco
- Altura de filas ajustada para mostrar tratamientos de varias líneas
- Scrollbars vertical y horizontal
- Columnas con ancho fijo para mejor organización

---

## Autor

**Leodan Garcia**

Universidad Tecnológica Empresarial de Guayaquil  
Programación de Alto Nivel - Unidad 3  
Año: 2026

---

## Licencia

Este proyecto es de uso académico para la Universidad Tecnológica Empresarial de Guayaquil.

---

## Notas Técnicas

### Validaciones implementadas:
- Cédula ecuatoriana: exactamente 10 dígitos numéricos
- Todos los campos son obligatorios al guardar paciente
- Al menos un síntoma requerido para verificar diagnóstico
- Prescripción médica obligatoria al guardar consulta

### Animaciones y efectos:
- Animación de puntos suspensivos durante análisis (250ms por frame)
- Ventanas modales que bloquean interacción hasta cerrar
- Colores diferenciados según estado (rojo: positivo, verde: negativo, naranja: advertencia)
- Cálculo automático de días en aislamiento

### Seguridad:
- Archivo config.py excluido del repositorio Git (.gitignore)
- Se proporciona config.example.py como plantilla
- Manejo de errores en conexiones a base de datos
- Validación de entradas de usuario

---

## Solución de Problemas

**Error de conexión a MySQL:**
- Verifica que MySQL esté ejecutándose
- Revisa las credenciales en config.py
- Confirma que la base de datos sistema_covid exista

**No aparecen datos en la tabla:**
- Verifica que existan consultas con diagnostico_covid = TRUE
- Revisa la fecha de filtro (formato AAAA-MM-DD)
- Usa "Ver Todos" para mostrar todos los registros

**Error al guardar paciente:**
- Verifica que la cédula tenga 10 dígitos
- Asegúrate de que historia laboral y cédula sean únicos
- Completa todos los campos del formulario

---

## Repositorio GitHub

https://github.com/leodan87/sistema_covid

Si este proyecto te fue útil, dale una estrella en GitHub.
└── database/
    └── crear_base_datos.sql   # Script de creación de BD
```

---

### Estructura de la Base de Datos

### Tabla `pacientes`
- `id` - Identificador único (auto-increment)
- `historia_laboral` - Historia laboral (único)
- `cedula` - Cédula de identidad (único, 10 dígitos)
- `nombres_completos` - Nombres completos
- `telefono` - Número de teléfono
- `direccion` - Dirección completa
- `fecha_registro` - Fecha de registro automática

### Tabla `consultas`
- `id` - Identificador único
- `paciente_id` - Referencia al paciente
- `fecha_consulta` - Fecha de la consulta
- `sintoma_1, sintoma_2, sintoma_3, sintoma_4` - Síntomas registrados
- `diagnostico_covid` - TRUE si es positivo, FALSE si es negativo
- `prescripcion_medica` - Tratamiento recetado

---

### Solución de Problemas

### Error: "Access denied for user 'root'@'localhost'"

**Solución:** La contraseña en `config.py` es incorrecta.
1. Verifica tu contraseña de MySQL
2. Actualiza `config.py` con la contraseña correcta

### Error: "Unknown database 'sistema_covid'"

**Solución:** La base de datos no existe.
1. Ejecuta el script `database/crear_base_datos.sql`

### Error: "No module named 'mysql.connector'"

**Solución:** Instala la librería:
```bash
pip install mysql-connector-python
```

---

## 📝 Notas Adicionales

- El sistema incluye 2 pacientes de prueba: HL-001 y HL-002
- Los datos se guardan en MySQL, no en archivos
- La cédula debe tener exactamente 10 dígitos
- La Historia Laboral y Cédula deben ser únicas
