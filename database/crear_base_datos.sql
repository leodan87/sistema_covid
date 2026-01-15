-- =====================================================
-- BASE DE DATOS - SISTEMA COVID-19
-- =====================================================

CREATE DATABASE IF NOT EXISTS sistema_covid;
USE sistema_covid;

-- Tabla de pacientes
CREATE TABLE IF NOT EXISTS pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    historia_laboral VARCHAR(20) UNIQUE NOT NULL,
    cedula VARCHAR(10) UNIQUE NOT NULL,
    nombres_completos VARCHAR(100) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de consultas médicas
CREATE TABLE IF NOT EXISTS consultas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    fecha_consulta DATE NOT NULL,
    sintoma_1 VARCHAR(50),
    sintoma_2 VARCHAR(50),
    sintoma_3 VARCHAR(50),
    sintoma_4 VARCHAR(50),
    diagnostico_covid BOOLEAN DEFAULT FALSE,
    prescripcion_medica TEXT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
);

-- Datos de prueba para la tabla de pacientes
INSERT INTO pacientes (historia_laboral, cedula, nombres_completos, telefono, direccion) VALUES
('HL-001', '0912345678', 'Martha Camacho Toledo', '0991234567', 'Av. Principal 123, Guayaquil'),
('HL-002', '0923456789', 'Carlos Jimenez Torres', '0982345678', 'Calle Secundaria 456');