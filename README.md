## Sistema de Registro Médico COVID-19
### Descripción del Proyecto

Sistema de gestión médica para registro de pacientes y diagnóstico de COVID-19 basado en síntomas. Permite:
- Registrar pacientes con sus datos personales
- Registrar consultas médicas con síntomas
- Diagnosticar COVID-19 según criterios médicos
- Consultar historial de pacientes con COVID-19

---

### Requisitos Previos

1. **Python 3.7 o superior**
2. **MySQL Server 8.0** (instalado y corriendo)
3. **Librerías Python:**
   - `mysql-connector-python`
   - `tkinter` (incluida con Python)

---

### Instalación y Configuración

### Paso 1: Instalar dependencias

```bash
pip install mysql-connector-python
```

### Paso 2: Configurar MySQL

1. Abre el archivo **`config.py`**
2. Modifica la contraseña de MySQL:

```python
CONFIGURACION_BD = {
    'host': 'localhost',
    'user': 'root',              # Tu usuario de MySQL
    'password': 'TU_CONTRASEÑA', # COLOCA AQUÍ TU CONTRASEÑA
    'database': 'sistema_covid'
}
```

### Paso 3: Crear la base de datos

Ejecuta el script SQL ubicado en `database/crear_base_datos.sql`:

**Opción A - Desde línea de comandos:**
```bash
mysql -u root -p < database/crear_base_datos.sql
```

**Opción B - Desde MySQL Workbench:**
1. Abre MySQL Workbench
2. Abre el archivo `database/crear_base_datos.sql`
3. Ejecuta el script completo

### Paso 4: Ejecutar la aplicación

```bash
python main.py
```

---

###  Criterio de Diagnóstico COVID-19

###  IMPORTANTE PARA EVALUACIÓN:

El sistema diagnostica **POSITIVO COVID-19** cuando el paciente presenta **LOS 3 SÍNTOMAS OBLIGATORIOS**:

1. ✅ **Fiebre**
2. ✅ **Fatiga**
3. ✅ **Pérdida de olfato y gusto**

**Ejemplos:**

| Síntomas Seleccionados | Diagnóstico |
|------------------------|-------------|
| Fiebre + Fatiga + Pérdida de olfato y gusto | 🔴 POSITIVO COVID-19 |
| Fiebre + Fatiga + Tos seca | 🟢 NEGATIVO COVID-19 |
| Fiebre + Pérdida de olfato y gusto | 🟢 NEGATIVO COVID-19 |
| Solo Fiebre | 🟢 NEGATIVO COVID-19 |

---

### Manual de Uso

### Pestaña "Registro de Pacientes"

1. **Buscar paciente existente:**
   - Ingresa la Historia Laboral (ej: HL-001)
   - Clic en "Buscar"

2. **Registrar nuevo paciente:**
   - Clic en "Nuevo"
   - Completa todos los campos
   - Clic en "💾 Guardar Paciente"

3. **Registrar consulta médica:**
   - Con un paciente seleccionado
   - Selecciona hasta 4 síntomas
   - Clic en "🔬 Verificar Diagnóstico COVID"
   - Ingresa la prescripción médica
   - Clic en "✅ Guardar Consulta"

### Pestaña "Consulta COVID-19"

1. **Ver todos los pacientes COVID:**
   - Clic en "📋 Ver Todos"

2. **Filtrar por fecha:**
   - Ingresa fecha (formato: AAAA-MM-DD)
   - Clic en "🔍 Consultar"

---

### Estructura del Proyecto

```
sistema_covid/
│
├── main.py                    # Punto de entrada de la aplicación
├── config.py                  # Configuración de BD y síntomas
├── database.py                # Funciones de acceso a datos
├── paciente.py                # Pestaña de registro de pacientes
├── consulta.py                # Pestaña de consulta COVID
├── README.md                  # Este archivo
│
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
