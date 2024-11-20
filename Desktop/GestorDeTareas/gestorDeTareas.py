import customtkinter as ctk
from tkinter.ttk import Treeview, Style
import tkinter as Tk
from tkinter import messagebox, filedialog
from datetime import datetime
from PIL import Image, ImageTk

class GestorTareasApp:        
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Gestor de Tareas")
        # Establecer el ícono de la ventana
        try:
            self.raiz.iconbitmap("logo.ico")  
        except Exception as e:
            print(f"No se pudo cargar el ícono: {e}")
        # Tema
        ctk.set_appearance_mode("light")  
        ctk.set_default_color_theme("green")
        self.modo_oscuro = False  
        # Contadores de tareas
        self.total_tareas = 0
        self.tareas_completadas = 0
        # Cargar imágenes de tema
        self.imagen_tema_oscuro = ctk.CTkImage(Image.open("oscuro.png").resize((30, 30)))
        self.imagen_tema_claro = ctk.CTkImage(Image.open("claro.png").resize((30, 30)))
        # Crear frames principales
        self.crear_frames()
        self.crear_widgets()

    # Método para centrar la ventana
    def centrar_ventana(self, ventana, ancho, alto):
        pantalla_ancho = ventana.winfo_screenwidth()
        pantalla_alto = ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        
    # Método de creación de los frames
    def crear_frames(self):
        self.frame_titulo = ctk.CTkFrame(self.raiz, corner_radius=10)
        self.frame_titulo.pack(padx=10, pady=10, fill="x")
        self.frame_superior = ctk.CTkFrame(self.raiz, corner_radius=10)
        self.frame_superior.pack(padx=10, pady=10, fill="x")
        self.frame_principal = ctk.CTkFrame(self.raiz, corner_radius=10)
        self.frame_principal.pack(padx=10, pady=10, fill="both", expand=True)
        self.frame_inferior = ctk.CTkFrame(self.raiz, corner_radius=10)
        self.frame_inferior.pack(padx=10, pady=10, fill="x")

    # Método de creación y personalización de los widgets
    def crear_widgets(self):
        # Título
        ctk.CTkLabel(self.frame_titulo, text="GESTOR DE TAREAS DE RUBÉN", 
                     font=("Arial", 20, "bold")).pack(side="left", padx=10, pady=5)
        
        # Imagen en el título
        try:
            imagen_original = Image.open("las-salinas_512.png")
            imagen_redimensionada = imagen_original.resize((50, 50))
            self.imagen = ctk.CTkImage(light_image=imagen_redimensionada, size=(50, 50))
            ctk.CTkLabel(self.frame_titulo, image=self.imagen, text="").pack(side="right", padx=10, pady=5)
        except Exception as e:
            messagebox.showwarning("Advertencia", f"No se pudo cargar la imagen: {e}")
            
        try:
            modo_actual = ctk.get_appearance_mode()
            if modo_actual == "Light":
                imagen_inicial = self.imagen_tema_oscuro
            elif modo_actual == "Dark":
                imagen_inicial = self.imagen_tema_claro
            else:
                raise ValueError("Modo de apariencia desconocido: " + str(modo_actual))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo determinar el modo de apariencia: {e}")
            imagen_inicial = self.imagen_tema_claro  # Fallback
        self.boton_cambiar_tema = ctk.CTkButton(
            self.frame_titulo,
            image=imagen_inicial,
            text="",
            width=30, height=30,
            command=self.cambiar_tema
        )
        self.boton_cambiar_tema.pack(side="right", padx=10, pady=5)

        # Frame superior: agregar tarea
        self.frame_superior.grid_columnconfigure(1, weight=1)  
        self.frame_superior.grid_columnconfigure(3, weight=1)  
        self.frame_superior.grid_columnconfigure(5, weight=1)  

        ctk.CTkLabel(self.frame_superior, text="Tarea:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entrada_tarea = ctk.CTkEntry(self.frame_superior)
        self.entrada_tarea.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame_superior, text="Prioridad:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_prioridad = ctk.CTkComboBox(
            self.frame_superior, values=["Alta", "Media", "Baja"])
        self.combo_prioridad.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.combo_prioridad.set("Media")

        ctk.CTkButton(self.frame_superior, text="Agregar Tarea", command=self.agregar_tarea).grid(
            row=0, column=4, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.frame_superior, text="Filtrar", command=self.abrir_menu_filtro).grid(
            row=0, column=5, padx=5, pady=5, sticky="ew")

        # Frame central: tabla de tareas
        style = Style()
        style.configure("Treeview", rowheight=25)
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)
        
        self.tabla_tareas = Treeview(self.frame_principal, columns=( 
            "Tarea", "Prioridad", "Estado", "Fecha"), show="headings")
        self.tabla_tareas.heading("Tarea", text="Tarea")
        self.tabla_tareas.heading("Prioridad", text="Prioridad")
        self.tabla_tareas.heading("Estado", text="Estado")
        self.tabla_tareas.heading("Fecha", text="Fecha")
        self.tabla_tareas.column("Tarea", width=200)
        self.tabla_tareas.column("Prioridad", width=100)
        self.tabla_tareas.column("Estado", width=100)
        self.tabla_tareas.column("Fecha", width=150)
        self.tabla_tareas.grid(row=0, column=0, sticky="nsew", padx=(50, 50), pady=50)
        self.tabla_tareas.tag_configure("Alta", background="#FFCCCC") 
        self.tabla_tareas.tag_configure("Media", background="#FFFFCC")  
        self.tabla_tareas.tag_configure("Baja", background="#CCFFCC")  

        scrollbar = ctk.CTkScrollbar(self.frame_principal, command=self.tabla_tareas.yview)
        self.tabla_tareas.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=5)

        # Frame inferior: botones
        self.frame_inferior.grid_columnconfigure(0, weight=1)
        self.frame_inferior.grid_columnconfigure(1, weight=1)
        self.frame_inferior.grid_columnconfigure(2, weight=1)
        self.frame_inferior.grid_columnconfigure(3, weight=1)
        self.frame_inferior.grid_columnconfigure(4, weight=1)

        ctk.CTkButton(self.frame_inferior, text="Eliminar Tarea", command=self.eliminar_tarea).grid(
            row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.frame_inferior, text="Marcar como Completada", command=self.marcar_completada).grid(
            row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Botón Editar
        ctk.CTkButton(self.frame_inferior, text="Editar Tarea", command=self.editar_tarea).grid(
            row=0, column=2, padx=5, pady=5, sticky="ew")

        self.etiqueta_contador = ctk.CTkLabel(
            self.frame_inferior, text="Total de tareas: 0    Completadas: 0", anchor="w")
        self.etiqueta_contador.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

    def agregar_tarea(self):
        tarea = self.entrada_tarea.get()
        prioridad = self.combo_prioridad.get()
        if tarea == "":
            messagebox.showwarning("Advertencia", "El campo de tarea no puede estar vacío.")
            return
        fecha_actual = datetime.now().strftime("%d-%m-%Y %H:%M")
        self.tabla_tareas.insert("", "end", values=(tarea, prioridad, "Pendiente", fecha_actual),
                                 tags=(prioridad,))
        self.entrada_tarea.delete(0, "end")
        self.total_tareas += 1
        self.actualizar_contadores()

    def eliminar_tarea(self):
        tarea_seleccionada = self.tabla_tareas.selection()
        if not tarea_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tarea para eliminarla.")
            return
        self.tabla_tareas.delete(tarea_seleccionada)
        self.total_tareas -= 1
        self.actualizar_contadores()

    def marcar_completada(self):
        tarea_seleccionada = self.tabla_tareas.selection()
        if not tarea_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tarea para marcarla como completada.")
            return
        self.tabla_tareas.item(tarea_seleccionada, values=(
            self.tabla_tareas.item(tarea_seleccionada)["values"][0],  # Tarea
            self.tabla_tareas.item(tarea_seleccionada)["values"][1],  # Prioridad
            "Completada", 
            self.tabla_tareas.item(tarea_seleccionada)["values"][3]  # Fecha
        ))
        self.tareas_completadas += 1
        self.actualizar_contadores()

    def actualizar_contadores(self):
        self.etiqueta_contador.configure(
            text=f"Total de tareas: {self.total_tareas}    Completadas: {self.tareas_completadas}"
        )
        
    def cambiar_tema(self):
        if self.modo_oscuro:
            ctk.set_appearance_mode("Light")
            self.boton_cambiar_tema.configure(image=self.imagen_tema_oscuro)
            self.modo_oscuro = False
        else:
            ctk.set_appearance_mode("Dark")
            self.boton_cambiar_tema.configure(image=self.imagen_tema_claro)
            self.modo_oscuro = True

    # Método para editar tareas
    def editar_tarea(self):
        tarea_seleccionada = self.tabla_tareas.selection()
        if not tarea_seleccionada:
            messagebox.showwarning("Advertencia", "Debe seleccionar una tarea para editarla.")
            return
    
        # Obtener valores de la tarea seleccionada
        valores = self.tabla_tareas.item(tarea_seleccionada)["values"]
        tarea_actual = valores[0]
        prioridad_actual = valores[1]
        
        # Crear ventana de edición
        ventana_edicion = ctk.CTkToplevel(self.raiz)
        ventana_edicion.title("Editar Tarea")
        
        ventana_edicion.grid_columnconfigure(0, weight=1, minsize=150)  
        ventana_edicion.grid_columnconfigure(1, weight=3, minsize=200)  
        ventana_edicion.grid_rowconfigure(0, weight=1)  
        ventana_edicion.grid_rowconfigure(1, weight=1)  
        ventana_edicion.grid_rowconfigure(2, weight=1)  
        
        self.centrar_ventana(ventana_edicion, 400, 200)
        
        # Campos de edición
        ctk.CTkLabel(ventana_edicion, text="Tarea:").grid(row=0, column=0, padx=50, pady=5, sticky="w")
        entrada_tarea_edicion = ctk.CTkEntry(ventana_edicion)
        entrada_tarea_edicion.insert(0, tarea_actual)
        entrada_tarea_edicion.grid(row=0, column=1, padx=50, pady=5, sticky="ew")
    
        ctk.CTkLabel(ventana_edicion, text="Prioridad:").grid(row=1, column=0, padx=50, pady=5, sticky="w")
        combo_prioridad_edicion = ctk.CTkComboBox(ventana_edicion, values=["Alta", "Media", "Baja"])
        combo_prioridad_edicion.set(prioridad_actual)
        combo_prioridad_edicion.grid(row=1, column=1, padx=50, pady=5, sticky="ew")
        
        def guardar_edicion():
            nueva_tarea = entrada_tarea_edicion.get()
            nueva_prioridad = combo_prioridad_edicion.get()
            if nueva_tarea == "":
                messagebox.showwarning("Advertencia", "El campo de tarea no puede estar vacío.")
                return
            
            # Actualizar la tarea en la tabla y cambiar el tag
            self.tabla_tareas.item(tarea_seleccionada, values=(
                nueva_tarea + " (editada)",
                nueva_prioridad,
                "Pendiente",
                valores[3]
            ), tags=(nueva_prioridad,))  # Actualiza el tag con la nueva prioridad
            
            ventana_edicion.destroy()
    
        ctk.CTkButton(ventana_edicion, text="Guardar cambios", command=guardar_edicion).grid(
            row=2, column=0, columnspan=2, padx=5, pady=10, sticky="ew")


    # Método para crear la ventana de filtrado
    def abrir_menu_filtro(self):
        menu_filtro = ctk.CTkToplevel(self.raiz)  # Ventana emergente
        menu_filtro.title("Ordenar Tareas")
        # Define el tamaño de la ventana emergente
        menu_filtro.geometry("250x200")
        # Crear un título dentro del menú emergente
        ctk.CTkLabel(menu_filtro, text="Seleccione el criterio de ordenamiento:", font=(
            "Arial", 12)).pack(pady=10)
        # Botones de ordenamiento dentro del menú
        ctk.CTkButton(menu_filtro, text="Ordenar por Nombre (A-Z)",
                      command=self.ordenar_por_nombre).pack(padx=10, pady=10, fill="x")
        ctk.CTkButton(menu_filtro, text="Ordenar por Fecha (Más Nuevo a Más Antiguo)",
                      command=self.ordenar_por_fecha).pack(padx=10, pady=10, fill="x")
        ctk.CTkButton(menu_filtro, text="Ordenar por Prioridad",
                      command=self.ordenar_por_prioridad).pack(padx=10, pady=10, fill="x")
        # Botón de cerrar
        ctk.CTkButton(menu_filtro, text="Cerrar", command=menu_filtro.destroy).pack(
            padx=10, pady=10, fill="x")

    # Método para ordenar por nombre, alfabéticamente
    def ordenar_por_nombre(self):
        tareas = [(self.tabla_tareas.item(item, "values"), item)
                  for item in self.tabla_tareas.get_children()]
        # Ordenar por el nombre de la tarea
        tareas.sort(key=lambda x: x[0][0].lower())
        for idx, (_, item) in enumerate(tareas):
            self.tabla_tareas.move(item, '', idx)
            
    # Método para ordenar por fecha, de más nuevo a más antiguo
    def ordenar_por_fecha(self):
        tareas = [(self.tabla_tareas.item(item, "values"), item)
                  for item in self.tabla_tareas.get_children()]
        tareas.sort(key=lambda x: datetime.strptime(
            x[0][3], "%Y-%m-%d %H:%M:%S"), reverse=True)  # Ordenar por fecha
        for idx, (_, item) in enumerate(tareas):
            self.tabla_tareas.move(item, '', idx)

    # Método para ordenar por prioridad, alta > media > baja
    def ordenar_por_prioridad(self):
        prioridad_orden = {"Alta": 0, "Media": 1, "Baja": 2}
        tareas = [(self.tabla_tareas.item(item, "values"), item)
                  for item in self.tabla_tareas.get_children()]
        # Ordenar por prioridad
        tareas.sort(key=lambda x: prioridad_orden[x[0][1]])
        for idx, (_, item) in enumerate(tareas):
            self.tabla_tareas.move(item, '', idx)

# Ejecución de la aplicación
root = ctk.CTk()
app = GestorTareasApp(root)
root.geometry("800x600")
ancho = 800
alto = 600
app.centrar_ventana(root, ancho, alto)
root.mainloop()