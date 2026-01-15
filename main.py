"""
===========================================
SISTEMA DE REGISTRO MÉDICO COVID-19
===========================================
Universidad Tecnológica Empresarial de Guayaquil
Programación de Alto Nivel - Unidad 3

Autor: Leodan Garcia

===========================================
INSTRUCCIONES DE USO:
===========================================
1. Pestaña "Registro de Pacientes":
   - Buscar paciente por Historia Laboral
   - Registrar nuevos pacientes
   - Seleccionar síntomas (máximo 4)
   - Verificar diagnóstico COVID-19
   - Guardar consulta médica

2. Criterio de Diagnóstico COVID-19:
   ⚠️ El paciente debe tener LOS 3 SÍNTOMAS:
      • Fiebre
      • Fatiga
      • Pérdida de olfato y gusto
   
   Si tiene los 3 → POSITIVO COVID-19
   Si tiene menos → NEGATIVO COVID-19

3. Pestaña "Consulta COVID-19":
   - Ver pacientes diagnosticados con COVID
   - Filtrar por fecha o ver todos
===========================================
"""

import tkinter as tk
from tkinter import ttk
from paciente import PestanaRegistro
from consulta import PestanaConsulta


def main():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Registro Médico COVID-19")
    ventana.geometry("1100x800")
    
    # Establecer ícono personalizado del hospital
    try:
        ventana.iconbitmap('assets/hospital_icon.ico')
    except:
        pass
    
    # Centrar ventana
    ancho = 1100
    alto = 800
    x = (ventana.winfo_screenwidth() - ancho) // 2
    y = (ventana.winfo_screenheight() - alto) // 2
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    # Título con degradado profesional
    titulo_frame = tk.Frame(ventana, bg="#1A252F", height=70)
    titulo_frame.pack(fill="x")
    titulo_frame.pack_propagate(False)
    
    titulo = tk.Label(
        titulo_frame,
        text="🏥 Sistema de Registro Médico COVID-19",
        font=("Segoe UI", 18, "bold"),
        bg="#1A252F",
        fg="#FFFFFF",
        pady=20
    )
    titulo.pack()
    
    subtitulo = tk.Label(
        titulo_frame,
        text="Universidad Tecnológica Empresarial de Guayaquil | Sistema Hospitalario",
        font=("Segoe UI", 9),
        bg="#1A252F",
        fg="#95A5A6"
    )
    subtitulo.pack(pady=(0, 10))
    
    # Crear notebook (pestañas) con estilo profesional
    style = ttk.Style()
    style.theme_use('clam')
    
    # Estilo para las pestañas
    style.configure('TNotebook', background='#ECF0F1', borderwidth=0)
    style.configure('TNotebook.Tab', 
                    background='#BDC3C7',
                    foreground='#2C3E50',
                    padding=[20, 10],
                    font=('Segoe UI', 10, 'bold'))
    style.map('TNotebook.Tab',
              background=[('selected', '#3498DB')],
              foreground=[('selected', '#FFFFFF')])
    
    # Estilo para los frames
    style.configure('TFrame', background='#ECF0F1')
    style.configure('TLabelframe', background='#FFFFFF', borderwidth=2, relief='solid')
    style.configure('TLabelframe.Label', 
                    background='#FFFFFF',
                    foreground='#2C3E50',
                    font=('Segoe UI', 11, 'bold'))
    
    # Estilo para botones
    style.configure('TButton',
                    background='#3498DB',
                    foreground='#FFFFFF',
                    borderwidth=0,
                    focuscolor='none',
                    font=('Segoe UI', 10))
    style.map('TButton',
              background=[('active', '#2980B9')])
    
    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Agregar las pestañas (importadas de otros archivos)
    PestanaRegistro(notebook)
    PestanaConsulta(notebook)
    
    # Iniciar aplicación
    ventana.mainloop()


# Punto de entrada
if __name__ == "__main__":
    main()