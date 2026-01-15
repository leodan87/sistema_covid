"""
Pestaña de Registro de Pacientes y Síntomas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from config import LISTA_SINTOMAS, SINTOMAS_COVID
import database as db


class PestanaRegistro:
    """Clase que maneja la pestaña de registro"""
    
    def __init__(self, notebook):
        # Crear el frame principal con scrollbar
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="📋 Registro de Pacientes")
        
        # Canvas y scrollbar
        canvas = tk.Canvas(main_frame, bg="#ECF0F1", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        
        # Frame scrolleable
        self.frame = ttk.Frame(canvas, padding=20)
        self.frame.configure(style='TFrame')
        
        # Configurar canvas
        def configurar_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajustar ancho del frame interno al ancho del canvas
            canvas_width = canvas.winfo_width()
            canvas.itemconfig(canvas_window, width=canvas_width)
        
        self.frame.bind("<Configure>", configurar_scroll)
        canvas.bind("<Configure>", configurar_scroll)
        
        canvas_window = canvas.create_window((0, 0), window=self.frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # ID del paciente actual (None si es nuevo)
        self.paciente_id = None
        
        # Crear las secciones
        self.crear_seccion_busqueda()
        self.crear_seccion_datos()
        self.crear_seccion_sintomas()
        self.crear_seccion_prescripcion()
    
    
    def crear_seccion_busqueda(self):
        """Sección para buscar paciente con diseño mejorado"""
        frame = ttk.LabelFrame(self.frame, text="🔍 Buscar Paciente", padding=15)
        frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(frame, text="Historia Laboral:", 
                  font=("Segoe UI", 10)).pack(side="left", padx=5)
        
        self.entrada_buscar = ttk.Entry(frame, width=20, font=("Segoe UI", 10))
        self.entrada_buscar.pack(side="left", padx=5)
        
        btn_buscar = ttk.Button(frame, text="🔍 Buscar", command=self.buscar)
        btn_buscar.pack(side="left", padx=5)
        
        btn_nuevo = ttk.Button(frame, text="➕ Nuevo", command=self.limpiar)
        btn_nuevo.pack(side="left", padx=5)
    
    
    def crear_seccion_datos(self):
        """Sección de datos del paciente con diseño profesional"""
        frame = ttk.LabelFrame(self.frame, text="👤 Datos del Paciente", padding=15)
        frame.pack(fill="x", pady=(0, 10))
        
        # Fila 1: Historia y Cédula
        fila1 = ttk.Frame(frame)
        fila1.pack(fill="x", pady=5)
        
        ttk.Label(fila1, text="Historia Laboral:", font=("Segoe UI", 10)).pack(side="left")
        self.entrada_historia = ttk.Entry(fila1, width=15, font=("Segoe UI", 10))
        self.entrada_historia.pack(side="left", padx=5)
        
        ttk.Label(fila1, text="Cédula:", font=("Segoe UI", 10)).pack(side="left", padx=(20,0))
        self.entrada_cedula = ttk.Entry(fila1, width=12, font=("Segoe UI", 10))
        self.entrada_cedula.pack(side="left", padx=5)
        
        # Fila 2: Nombres
        fila2 = ttk.Frame(frame)
        fila2.pack(fill="x", pady=5)
        
        ttk.Label(fila2, text="Nombres Completos:", font=("Segoe UI", 10)).pack(side="left")
        self.entrada_nombres = ttk.Entry(fila2, width=45, font=("Segoe UI", 10))
        self.entrada_nombres.pack(side="left", padx=5)
        
        # Fila 3: Teléfono
        fila3 = ttk.Frame(frame)
        fila3.pack(fill="x", pady=5)
        
        ttk.Label(fila3, text="Teléfono:", font=("Segoe UI", 10)).pack(side="left")
        self.entrada_telefono = ttk.Entry(fila3, width=15, font=("Segoe UI", 10))
        self.entrada_telefono.pack(side="left", padx=5)
        
        # Fila 4: Dirección
        fila4 = ttk.Frame(frame)
        fila4.pack(fill="x", pady=5)
        
        ttk.Label(fila4, text="Dirección:", font=("Segoe UI", 10)).pack(side="left")
        self.entrada_direccion = ttk.Entry(fila4, width=55, font=("Segoe UI", 10))
        self.entrada_direccion.pack(side="left", padx=5)
        
        # Botón guardar con estilo
        ttk.Button(frame, text="💾 Guardar Paciente", 
                   command=self.guardar_paciente).pack(pady=15)
    
    
    def crear_seccion_sintomas(self):
        """Sección de síntomas"""
        frame = ttk.LabelFrame(self.frame, text="🩺 Síntomas (Máximo 4)", padding=10)
        frame.pack(fill="x", pady=5)
        
        # Crear 4 combos para síntomas
        self.combos_sintomas = []
        opciones = ["-- Sin síntoma --"] + LISTA_SINTOMAS
        
        fila_sintomas = ttk.Frame(frame)
        fila_sintomas.pack(fill="x")
        
        for i in range(4):
            ttk.Label(fila_sintomas, text=f"Síntoma {i+1}:").grid(row=i//2, column=(i%2)*2, padx=5, pady=3)
            combo = ttk.Combobox(fila_sintomas, values=opciones, width=25, state="readonly")
            combo.set("-- Sin síntoma --")
            combo.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=3)
            self.combos_sintomas.append(combo)
        
        # Etiqueta de diagnóstico
        self.etiqueta_diagnostico = ttk.Label(frame, text="", font=("Arial", 11, "bold"))
        self.etiqueta_diagnostico.pack(pady=5)
        
        ttk.Button(frame, text="🔬 Verificar Diagnóstico COVID", 
                   command=self.verificar_covid).pack(pady=5)
    
    
    def crear_seccion_prescripcion(self):
        """Sección de prescripción médica"""
        frame = ttk.LabelFrame(self.frame, text="💊 Prescripción Médica", padding=10)
        frame.pack(fill="x", pady=5)
        
        self.texto_prescripcion = tk.Text(frame, height=3, width=70)
        self.texto_prescripcion.pack(pady=5)
        
        ttk.Button(frame, text="✅ Guardar Consulta", 
                   command=self.guardar_consulta).pack(pady=10)
    
    
    # ─────────────────────────────────────────────
    # FUNCIONES
    # ─────────────────────────────────────────────
    
    def buscar(self):
        """Busca un paciente por historia laboral"""
        historia = self.entrada_buscar.get().strip()
        if not historia:
            messagebox.showwarning("Aviso", "Ingrese la historia laboral")
            return
        
        paciente = db.buscar_paciente_por_historia(historia)
        
        if paciente:
            self.limpiar()
            self.paciente_id = paciente['id']
            self.entrada_historia.insert(0, paciente['historia_laboral'])
            self.entrada_cedula.insert(0, paciente['cedula'])
            self.entrada_nombres.insert(0, paciente['nombres_completos'])
            self.entrada_telefono.insert(0, paciente['telefono'])
            self.entrada_direccion.insert(0, paciente['direccion'])
            
            # Verificar si tiene COVID-19 registrado
            covid_info = db.verificar_covid_paciente(paciente['id'])
            if covid_info:
                self.mostrar_alerta_covid(paciente['nombres_completos'], covid_info)
        else:
            self.mostrar_paciente_no_encontrado(historia)
            self.limpiar()
            self.entrada_historia.insert(0, historia)
    
    
    def mostrar_paciente_no_encontrado(self, historia):
        """Muestra ventana profesional cuando el paciente no existe"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Búsqueda de Paciente")
        ventana.geometry("450x330")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Establecer ícono personalizado del hospital
        try:
            ventana.iconbitmap('assets/hospital_icon.ico')
        except:
            pass
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 450) // 2
        y = (ventana.winfo_screenheight() - 330) // 2
        ventana.geometry(f"450x330+{x}+{y}")
        
        # Encabezado con color azul institucional
        header = tk.Frame(ventana, bg="#3498DB", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text="ℹ️ PACIENTE NO ENCONTRADO", 
              font=("Arial", 14, "bold"), bg="#3498DB", fg="white").pack(pady=18)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=25, pady=12)
        
        # Icono y mensaje principal
        Label(contenido, text="🔍", font=("Arial", 40), 
              bg="#ffffff", fg="#3498DB").pack(pady=5)
        
        Label(contenido, text=f"Historia Laboral: {historia}", 
              font=("Arial", 11, "bold"), bg="#ffffff", fg="#2C3E50").pack(pady=6)
        
        Label(contenido, text="El paciente no está registrado en el sistema.", 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D").pack(pady=4)
        
        Label(contenido, text="Puede proceder a registrarlo con los datos correspondientes.", 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D").pack(pady=1)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=65)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        Button(footer, text="✓ Aceptar", command=ventana.destroy, 
               bg="#3498DB", fg="white", font=("Arial", 10, "bold"), 
               padx=30, pady=8, border=0, cursor="hand2", 
               relief="flat", activebackground="#2980B9", activeforeground="white").pack(pady=13)
    
    
    def mostrar_paciente_guardado(self, nombre_paciente):
        """Muestra ventana profesional cuando se guarda exitosamente un paciente"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Confirmación")
        ventana.geometry("450x300")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Establecer ícono personalizado del hospital
        try:
            ventana.iconbitmap('assets/hospital_icon.ico')
        except:
            pass
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 450) // 2
        y = (ventana.winfo_screenheight() - 300) // 2
        ventana.geometry(f"450x300+{x}+{y}")
        
        # Encabezado con color verde (éxito)
        header = tk.Frame(ventana, bg="#27AE60", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text="✓ REGISTRO EXITOSO", 
              font=("Arial", 14, "bold"), bg="#27AE60", fg="white").pack(pady=18)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Icono de éxito
        Label(contenido, text="✓", font=("Arial", 50), 
              bg="#ffffff", fg="#27AE60").pack(pady=8)
        
        Label(contenido, text="Paciente guardado correctamente", 
              font=("Arial", 11, "bold"), bg="#ffffff", fg="#2C3E50").pack(pady=6)
        
        Label(contenido, text=nombre_paciente, 
              font=("Arial", 10), bg="#ffffff", fg="#7F8C8D").pack(pady=4)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=65)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        Button(footer, text="✓ Aceptar", command=ventana.destroy, 
               bg="#27AE60", fg="white", font=("Arial", 10, "bold"), 
               padx=30, pady=8, border=0, cursor="hand2", 
               relief="flat", activebackground="#229954", activeforeground="white").pack(pady=13)
    
    
    def mostrar_alerta_covid(self, nombre_paciente, covid_info):
        """Muestra alerta profesional cuando el paciente tiene COVID-19 registrado"""
        from tkinter import Toplevel, Label, Button
        from datetime import datetime, timedelta
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Alerta COVID-19")
        ventana.geometry("520x520")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Establecer ícono personalizado del hospital
        try:
            ventana.iconbitmap('assets/hospital_icon.ico')
        except:
            pass
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 520) // 2
        y = (ventana.winfo_screenheight() - 520) // 2
        ventana.geometry(f"520x520+{x}+{y}")
        
        # Encabezado con color rojo de alerta
        header = tk.Frame(ventana, bg="#E74C3C", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text="⚠️ PACIENTE CON COVID-19", 
              font=("Arial", 15, "bold"), bg="#E74C3C", fg="white").pack(pady=20)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Icono de alerta
        Label(contenido, text="🦠", font=("Arial", 50), 
              bg="#ffffff", fg="#E74C3C").pack(pady=8)
        
        # Nombre del paciente
        Label(contenido, text=nombre_paciente, 
              font=("Arial", 12, "bold"), bg="#ffffff", fg="#2C3E50").pack(pady=5)
        
        # Estado
        Label(contenido, text="PACIENTE CON COVID-19 POSITIVO", 
              font=("Arial", 11, "bold"), bg="#ffffff", fg="#E74C3C").pack(pady=5)
        
        # Calcular días desde diagnóstico
        fecha_diagnostico = covid_info['fecha_consulta']
        if isinstance(fecha_diagnostico, str):
            fecha_diagnostico = datetime.strptime(fecha_diagnostico, '%Y-%m-%d').date()
        
        dias_aislamiento = (date.today() - fecha_diagnostico).days
        
        # Información del estado
        Label(contenido, text=f"Fecha de diagnóstico: {fecha_diagnostico.strftime('%d/%m/%Y')}", 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D").pack(pady=3)
        
        Label(contenido, text=f"Días en aislamiento: {dias_aislamiento} días", 
              font=("Arial", 9, "bold"), bg="#ffffff", fg="#E67E22").pack(pady=3)
        
        # Estado según días
        if dias_aislamiento < 10:
            estado = "🔴 EN AISLAMIENTO - RECUPERACIÓN EN PROCESO"
            color_estado = "#E74C3C"
        elif dias_aislamiento < 14:
            estado = "🟡 PERÍODO FINAL DE AISLAMIENTO"
            color_estado = "#F39C12"
        else:
            estado = "🟢 PERÍODO DE AISLAMIENTO CUMPLIDO"
            color_estado = "#27AE60"
        
        Label(contenido, text=estado, 
              font=("Arial", 10, "bold"), bg="#ffffff", fg=color_estado, 
              wraplength=450).pack(pady=8)
        
        # Advertencia
        Label(contenido, text="⚠️ Seguir protocolos de bioseguridad", 
              font=("Arial", 9), bg="#ffffff", fg="#95A5A6").pack(pady=3)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=65)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        Button(footer, text="✓ Entendido", command=ventana.destroy, 
               bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), 
               padx=35, pady=10, border=0, cursor="hand2", 
               relief="flat", activebackground="#C0392B", activeforeground="white").pack(pady=13)
    
    
    def mostrar_consulta_guardada(self):
        """Muestra ventana profesional cuando se guarda exitosamente una consulta"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Confirmación")
        ventana.geometry("450x280")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Establecer ícono personalizado del hospital
        try:
            ventana.iconbitmap('assets/hospital_icon.ico')
        except:
            pass
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 450) // 2
        y = (ventana.winfo_screenheight() - 280) // 2
        ventana.geometry(f"450x280+{x}+{y}")
        
        # Encabezado con color azul
        header = tk.Frame(ventana, bg="#3498DB", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text="✓ CONSULTA REGISTRADA", 
              font=("Arial", 14, "bold"), bg="#3498DB", fg="white").pack(pady=18)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=25, pady=15)
        
        # Icono de éxito
        Label(contenido, text="📋", font=("Arial", 50), 
              bg="#ffffff", fg="#3498DB").pack(pady=8)
        
        Label(contenido, text="Consulta guardada correctamente", 
              font=("Arial", 11, "bold"), bg="#ffffff", fg="#2C3E50").pack(pady=6)
        
        Label(contenido, text="Los datos han sido registrados en el sistema", 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D").pack(pady=4)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=65)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        Button(footer, text="✓ Aceptar", command=ventana.destroy, 
               bg="#3498DB", fg="white", font=("Arial", 10, "bold"), 
               padx=30, pady=8, border=0, cursor="hand2", 
               relief="flat", activebackground="#2980B9", activeforeground="white").pack(pady=13)
    
    
    def mostrar_analisis_laboratorio(self, tiene_covid):
        """Muestra animación de análisis de laboratorio y luego el resultado"""
        from tkinter import Toplevel, Label
        import time
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Análisis COVID-19")
        ventana.geometry("500x280")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        ventana.overrideredirect(True)  # Sin bordes para efecto profesional
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 500) // 2
        y = (ventana.winfo_screenheight() - 280) // 2
        ventana.geometry(f"500x280+{x}+{y}")
        
        # Borde de la ventana
        ventana.configure(bg="#3498DB", highlightthickness=2, highlightbackground="#2980B9")
        
        # Frame interno
        frame_interno = tk.Frame(ventana, bg="#ffffff")
        frame_interno.pack(fill="both", expand=True, padx=3, pady=3)
        
        # Encabezado
        header = tk.Frame(frame_interno, bg="#3498DB", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text="🔬 ANÁLISIS DE LABORATORIO", 
              font=("Arial", 14, "bold"), bg="#3498DB", fg="white").pack(pady=18)
        
        # Contenido
        contenido = tk.Frame(frame_interno, bg="#ffffff")
        contenido.pack(fill="both", expand=True, pady=20)
        
        # Icono de laboratorio
        Label(contenido, text="🧪", font=("Arial", 50), 
              bg="#ffffff", fg="#3498DB").pack(pady=10)
        
        # Texto de análisis
        texto_analisis = Label(contenido, text="Analizando muestras", 
                              font=("Arial", 12, "bold"), bg="#ffffff", fg="#2C3E50")
        texto_analisis.pack(pady=8)
        
        # Puntos animados
        puntos_label = Label(contenido, text="", 
                            font=("Arial", 14, "bold"), bg="#ffffff", fg="#3498DB")
        puntos_label.pack()
        
        # Subtexto
        Label(contenido, text="Procesando resultados del diagnóstico COVID-19", 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D").pack(pady=5)
        
        # Animación de puntos
        def animar_puntos(contador=0):
            puntos = "." * (contador % 4)
            puntos_label.config(text=puntos.ljust(3))
            
            if contador < 12:  # 3 segundos (12 * 250ms)
                ventana.after(250, lambda: animar_puntos(contador + 1))
            else:
                ventana.destroy()
                self.mostrar_resultado_covid(tiene_covid)
        
        # Iniciar animación
        animar_puntos()
        
        # Hacer la ventana modal
        ventana.transient(self.frame.winfo_toplevel())
        ventana.grab_set()
    
    
    def mostrar_resultado_covid(self, tiene_covid):
        """Muestra el resultado del diagnóstico COVID-19"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Resultado COVID-19")
        ventana.geometry("500x420")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Establecer ícono personalizado
        try:
            ventana.iconbitmap('assets/hospital_icon.ico')
        except:
            pass
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 500) // 2
        y = (ventana.winfo_screenheight() - 420) // 2
        ventana.geometry(f"500x420+{x}+{y}")
        
        if tiene_covid:
            # POSITIVO - Rojo
            color_header = "#E74C3C"
            color_boton = "#C0392B"
            icono = "🦠"
            titulo = "RESULTADO: POSITIVO COVID-19"
            mensaje = "El paciente presenta los síntomas característicos de COVID-19"
            indicacion = "Se requiere aislamiento inmediato y tratamiento médico"
            
            # Actualizar etiqueta en el formulario principal
            self.etiqueta_diagnostico.config(text="🔴 POSITIVO COVID-19", foreground="red")
        else:
            # NEGATIVO - Verde
            color_header = "#27AE60"
            color_boton = "#229954"
            icono = "✓"
            titulo = "RESULTADO: NEGATIVO COVID-19"
            mensaje = "El paciente NO presenta síntomas de COVID-19"
            indicacion = "Continuar con las medidas preventivas habituales"
            
            # Actualizar etiqueta en el formulario principal
            self.etiqueta_diagnostico.config(text="🟢 NEGATIVO COVID-19", foreground="green")
        
        # Encabezado
        header = tk.Frame(ventana, bg=color_header, height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        Label(header, text=titulo, 
              font=("Arial", 13, "bold"), bg=color_header, fg="white").pack(pady=20)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Icono grande
        Label(contenido, text=icono, font=("Arial", 60), 
              bg="#ffffff", fg=color_header).pack(pady=12)
        
        # Mensaje principal
        Label(contenido, text=mensaje, 
              font=("Arial", 11, "bold"), bg="#ffffff", fg="#2C3E50", 
              wraplength=400, justify="center").pack(pady=8)
        
        # Indicación
        Label(contenido, text=indicacion, 
              font=("Arial", 9), bg="#ffffff", fg="#7F8C8D",
              wraplength=400, justify="center").pack(pady=5)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=70)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        Button(footer, text="✓ Entendido", command=ventana.destroy, 
               bg=color_header, fg="white", font=("Arial", 10, "bold"), 
               padx=35, pady=10, border=0, cursor="hand2", 
               relief="flat", activebackground=color_boton, activeforeground="white").pack(pady=15)
    
    
    def mostrar_paciente_encontrado(self, paciente):
        """Muestra ventana profesional con información del paciente encontrado"""
        from tkinter import Toplevel, Label, Button
        from datetime import datetime
        
        ventana = Toplevel()
        ventana.title("Sistema Hospitalario - Paciente Encontrado")
        ventana.geometry("500x350")
        ventana.resizable(False, False)
        ventana.configure(bg="#ffffff")
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 500) // 2
        y = (ventana.winfo_screenheight() - 350) // 2
        ventana.geometry(f"500x350+{x}+{y}")
        
        # Encabezado con color institucional
        header = tk.Frame(ventana, bg="#2C3E50", height=80)
        header.pack(fill="x")
        
        Label(header, text="✓ PACIENTE ENCONTRADO", 
              font=("Arial", 18, "bold"), bg="#2C3E50", fg="white").pack(pady=25)
        
        # Contenido
        contenido = tk.Frame(ventana, bg="#ffffff")
        contenido.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Información del paciente con formato profesional
        info = [
            ("📋 Historia Laboral:", paciente['historia_laboral']),
            ("🆔 Cédula:", paciente['cedula']),
            ("👤 Paciente:", paciente['nombres_completos']),
            ("📞 Teléfono:", paciente['telefono']),
            ("📍 Dirección:", paciente['direccion'])
        ]
        
        for i, (etiqueta, valor) in enumerate(info):
            # Etiqueta
            Label(contenido, text=etiqueta, font=("Arial", 10, "bold"), 
                  bg="#ffffff", fg="#2C3E50", anchor="w").grid(row=i, column=0, sticky="w", pady=5, padx=5)
            # Valor
            Label(contenido, text=valor, font=("Arial", 10), 
                  bg="#ffffff", fg="#34495E", anchor="w").grid(row=i, column=1, sticky="w", pady=5, padx=10)
        
        # Pie con botón
        footer = tk.Frame(ventana, bg="#ECF0F1", height=60)
        footer.pack(fill="x", side="bottom")
        
        Button(footer, text="✓ Aceptar", command=ventana.destroy, 
               bg="#27AE60", fg="white", font=("Arial", 11, "bold"), 
               padx=30, pady=8, border=0, cursor="hand2").pack(pady=10)
    
    
    def guardar_paciente(self):
        """Guarda el paciente en la base de datos"""
        # Obtener datos
        historia = self.entrada_historia.get().strip()
        cedula = self.entrada_cedula.get().strip()
        nombres = self.entrada_nombres.get().strip()
        telefono = self.entrada_telefono.get().strip()
        direccion = self.entrada_direccion.get().strip()
        
        # Validar campos
        if not all([historia, cedula, nombres, telefono, direccion]):
            messagebox.showwarning("Aviso", "Complete todos los campos")
            return
        
        if len(cedula) != 10 or not cedula.isdigit():
            messagebox.showwarning("Aviso", "La cédula debe tener 10 dígitos")
            return
        
        # Guardar
        datos = (historia, cedula, nombres, telefono, direccion)
        resultado = db.guardar_paciente(datos, self.paciente_id)
        
        if resultado:
            self.paciente_id = resultado
            self.mostrar_paciente_guardado(nombres)
    
    
    def verificar_covid(self):
        """
        Verifica si tiene COVID según los síntomas seleccionados.
        
        LÓGICA DE DIAGNÓSTICO:
        - Se cuentan cuántos de los 3 síntomas COVID obligatorios están presentes
        - Síntomas COVID: Fiebre, Fatiga, Pérdida de olfato y gusto
        - Si tiene los 3 síntomas → POSITIVO COVID-19
        - Si tiene menos de 3 → NEGATIVO COVID-19
        """
        sintomas = [c.get() for c in self.combos_sintomas if c.get() != "-- Sin síntoma --"]
        
        if not sintomas:
            self.etiqueta_diagnostico.config(text="⚠️ Sin síntomas seleccionados", foreground="orange")
            return False
        
        # Contar cuántos de los 3 síntomas COVID obligatorios tiene el paciente
        # Debe tener los 3 (>= 3) para ser positivo
        tiene_covid = sum(1 for s in SINTOMAS_COVID if s in sintomas) >= 3
        
        # Mostrar ventana de análisis con animación
        self.mostrar_analisis_laboratorio(tiene_covid)
        
        return tiene_covid
    
    
    def guardar_consulta(self):
        """Guarda la consulta médica completa"""
        if not self.paciente_id:
            messagebox.showwarning("Aviso", "Primero busque o registre un paciente")
            return
        
        # Obtener síntomas (4 valores, None si no hay)
        sintomas = []
        for combo in self.combos_sintomas:
            valor = combo.get()
            sintomas.append(valor if valor != "-- Sin síntoma --" else None)
        
        # Verificar diagnóstico (sin mostrar ventana, solo calcular)
        sintomas_seleccionados = [c.get() for c in self.combos_sintomas if c.get() != "-- Sin síntoma --"]
        es_covid = sum(1 for s in SINTOMAS_COVID if s in sintomas_seleccionados) >= 3
        
        # Obtener prescripción
        prescripcion = self.texto_prescripcion.get("1.0", tk.END).strip()
        if not prescripcion:
            messagebox.showwarning("Aviso", "Ingrese la prescripción médica")
            return
        
        # Guardar en BD
        if db.guardar_consulta(self.paciente_id, date.today(), sintomas, es_covid, prescripcion):
            self.mostrar_consulta_guardada()
            # Limpiar síntomas y prescripción
            for combo in self.combos_sintomas:
                combo.set("-- Sin síntoma --")
            self.texto_prescripcion.delete("1.0", tk.END)
            self.etiqueta_diagnostico.config(text="")
    
    
    def limpiar(self):
        """Limpia todos los campos"""
        self.paciente_id = None
        self.entrada_historia.delete(0, tk.END)
        self.entrada_cedula.delete(0, tk.END)
        self.entrada_nombres.delete(0, tk.END)
        self.entrada_telefono.delete(0, tk.END)
        self.entrada_direccion.delete(0, tk.END)
        for combo in self.combos_sintomas:
            combo.set("-- Sin síntoma --")
        self.texto_prescripcion.delete("1.0", tk.END)
        self.etiqueta_diagnostico.config(text="")