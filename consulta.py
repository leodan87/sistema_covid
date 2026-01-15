"""
Pestaña de Consulta de Pacientes con COVID-19
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import database as db


class PestanaConsulta:
    """Clase que maneja la pestaña de consulta COVID"""
    
    def __init__(self, notebook):
        # Crear el frame de la pestaña
        self.frame = ttk.Frame(notebook, padding=15)
        notebook.add(self.frame, text="📊 Consulta COVID-19")
        
        # Crear las secciones
        self.crear_seccion_filtro()
        self.crear_seccion_tabla()
    
    
    def crear_seccion_filtro(self):
        """Sección para filtrar por fecha"""
        frame = ttk.LabelFrame(self.frame, text="🗓️ Filtrar por Fecha", padding=10)
        frame.pack(fill="x", pady=5)
        
        ttk.Label(frame, text="Fecha (AAAA-MM-DD):").pack(side="left", padx=5)
        
        self.entrada_fecha = ttk.Entry(frame, width=12)
        self.entrada_fecha.insert(0, str(date.today()))
        self.entrada_fecha.pack(side="left", padx=5)
        
        ttk.Button(frame, text="🔍 Consultar", 
                   command=self.consultar_por_fecha).pack(side="left", padx=5)
        
        ttk.Button(frame, text="📋 Ver Todos", 
                   command=self.consultar_todos).pack(side="left", padx=5)
    
    
    def crear_seccion_tabla(self):
        """Sección con la tabla de resultados"""
        frame = ttk.LabelFrame(self.frame, text="📄 Pacientes con COVID-19", padding=10)
        frame.pack(fill="both", expand=True, pady=5)
        
        # Definir columnas
        columnas = ("historia", "cedula", "nombres", "fecha", "diagnostico", "tratamiento")
        
        # Crear estilo personalizado con líneas HORIZONTALES
        style = ttk.Style()
        
        style.configure("Treeview", 
                       rowheight=80,
                       background="#FFFFFF",
                       foreground="#2C3E50",
                       fieldbackground="#FFFFFF")
        
        # Estilo del encabezado
        style.configure("Treeview.Heading",
                       background="#34495E",
                       foreground="white",
                       borderwidth=1,
                       relief="raised",
                       font=('Segoe UI', 10, 'bold'))
        style.map("Treeview.Heading",
                 background=[('active', '#2C3E50')])
        
        style.map('Treeview',
                 background=[('selected', '#3498DB')],
                 foreground=[('selected', 'white')])
        
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=8)
        
        # Configurar encabezados
        self.tabla.heading("historia", text="Historia Lab.")
        self.tabla.heading("cedula", text="Cédula")
        self.tabla.heading("nombres", text="Nombres")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("diagnostico", text="Diagnóstico")
        self.tabla.heading("tratamiento", text="Tratamiento")
        
        # Configurar anchos y alineación centrada
        self.tabla.column("historia", width=100, anchor="center")
        self.tabla.column("cedula", width=100, anchor="center")
        self.tabla.column("nombres", width=200, anchor="center")
        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("diagnostico", width=150, anchor="center")
        self.tabla.column("tratamiento", width=400, anchor="center")
        
        # Tags para filas con colores MÁS CONTRASTANTES para mejor distinción
        self.tabla.tag_configure('fila_par', background='#E8EAF6')  # Azul muy claro
        self.tabla.tag_configure('fila_impar', background='#FFFFFF')  # Blanco
        
        # Scrollbars (vertical y horizontal)
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tabla.pack(side="top", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        
        # Doble clic para ver tratamiento completo
        self.tabla.bind("<Double-1>", self.ver_tratamiento_completo)
    
    
    def consultar_por_fecha(self):
        """Consulta pacientes COVID por fecha específica"""
        fecha = self.entrada_fecha.get().strip()
        if not fecha:
            messagebox.showwarning("Aviso", "Ingrese una fecha")
            return
        
        self.mostrar_resultados(db.obtener_pacientes_covid(fecha))
    
    
    def consultar_todos(self):
        """Consulta todos los pacientes COVID"""
        self.mostrar_resultados(db.obtener_pacientes_covid())
    
    
    def ver_tratamiento_completo(self, event):
        """Muestra el tratamiento completo al hacer doble clic"""
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item['values']
            tratamiento = valores[5]  # Columna de tratamiento
            
            # Crear ventana emergente
            from tkinter import Toplevel, Text, Scrollbar
            ventana = Toplevel()
            ventana.title(f"Tratamiento - {valores[2]}")
            ventana.geometry("600x300")
            
            texto = Text(ventana, wrap="word", font=("Arial", 10))
            scroll = Scrollbar(ventana, command=texto.yview)
            texto.configure(yscrollcommand=scroll.set)
            
            texto.insert("1.0", tratamiento)
            texto.config(state="disabled")  # Solo lectura
            
            texto.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            scroll.pack(side="right", fill="y")
    
    
    def mostrar_resultados(self, resultados):
        """Muestra los resultados en la tabla"""
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        if resultados:
            for idx, r in enumerate(resultados):
                # Dividir tratamiento en líneas de máximo 60 caracteres
                tratamiento = r['prescripcion_medica']
                lineas = []
                palabras = tratamiento.split()
                linea_actual = ""
                
                for palabra in palabras:
                    if len(linea_actual + palabra) < 60:
                        linea_actual += palabra + " "
                    else:
                        lineas.append(linea_actual.strip())
                        linea_actual = palabra + " "
                
                if linea_actual:
                    lineas.append(linea_actual.strip())
                
                # Unir con saltos de línea (máximo 4 líneas)
                tratamiento_formateado = "\n".join(lineas[:4])
                if len(lineas) > 4:
                    tratamiento_formateado += "..."
                
                # Aplicar tag alternado para colores de filas
                tag = 'fila_par' if idx % 2 == 0 else 'fila_impar'
                
                self.tabla.insert("", "end", values=(
                    r['historia_laboral'],
                    r['cedula'],
                    r['nombres_completos'],
                    r['fecha_consulta'],
                    "POSITIVO COVID-19",  # Diagnóstico
                    tratamiento_formateado
                ), tags=(tag,))
    
    
    def mostrar_ventana_resultados(self, cantidad):
        """Muestra ventana profesional con cantidad de resultados"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Resultados")
        ventana.geometry("350x180")
        ventana.resizable(False, False)
        ventana.configure(bg="#27AE60")
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 350) // 2
        y = (ventana.winfo_screenheight() - 180) // 2
        ventana.geometry(f"350x180+{x}+{y}")
        
        # Contenido simple
        Label(ventana, text="✓", font=("Arial", 50), bg="#27AE60", fg="white").pack(pady=15)
        
        Label(ventana, text=f"{cantidad} Paciente(s) Encontrado(s)", 
              font=("Arial", 12, "bold"), bg="#27AE60", fg="white").pack()
        
        # Botón
        Button(ventana, text="Aceptar", command=ventana.destroy, 
               bg="white", fg="#27AE60", font=("Arial", 10, "bold"), 
               padx=25, pady=5).pack(pady=15)
    
    
    def mostrar_ventana_sin_resultados(self):
        """Muestra ventana profesional cuando no hay resultados"""
        from tkinter import Toplevel, Label, Button
        
        ventana = Toplevel()
        ventana.title("Sin Resultados")
        ventana.geometry("350x180")
        ventana.resizable(False, False)
        ventana.configure(bg="#E67E22")
        
        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() - 350) // 2
        y = (ventana.winfo_screenheight() - 180) // 2
        ventana.geometry(f"350x180+{x}+{y}")
        
        # Contenido simple
        Label(ventana, text="⚠", font=("Arial", 50), bg="#E67E22", fg="white").pack(pady=15)
        
        Label(ventana, text="Sin Pacientes COVID-19", 
              font=("Arial", 12, "bold"), bg="#E67E22", fg="white").pack()
        
        # Botón
        Button(ventana, text="Aceptar", command=ventana.destroy, 
               bg="white", fg="#E67E22", font=("Arial", 10, "bold"), 
               padx=25, pady=5).pack(pady=15)