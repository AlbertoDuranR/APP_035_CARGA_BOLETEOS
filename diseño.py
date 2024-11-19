import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from tkinter import filedialog
from services.dateService import DateService
from app import processBoleteos, processCuadresCaja
from models.dynamics import ModelDynamics
import os

def create_gui():
    # Crear la ventana principal
    root = ttk.Window(themename="journal")
    root.title("Gestión de Datos")
    root.geometry("600x420")

    # Crear un Notebook para las pestañas
    notebook = ttk.Notebook(root, bootstyle=PRIMARY)
    notebook.pack(fill=BOTH, expand=True)

    # Primera pestaña: Descarga de Datos Dynamics
    frame_download = ttk.Frame(notebook, padding=10)
    notebook.add(frame_download, text="Descarga de Datos Dynamics")

    # Segunda pestaña: Carga de Datos RRHH
    frame_upload = ttk.Frame(notebook, padding=10)
    notebook.add(frame_upload, text="Carga de Datos RRHH")

    # ---------------------- Contenido de Descarga de Datos ----------------------
    ttk.Label(frame_download, text="Descarga de Datos Dynamics", font=("Helvetica", 16)).pack(pady=10)

    # Crear selectores de fecha para boleteos y cuadres de caja
    boleteos_desde, boleteos_hasta = create_date_range_selector(
        frame_download, "Seleccione los rangos de fecha para Boleteos"
    )
    cuadres_desde, cuadres_hasta = create_date_range_selector(
        frame_download, "Seleccione los rangos de fecha para Cuadres de Caja"
    )

    # Selector de carpeta de salida
    output_folder_var = create_folder_selector(frame_download)

    # Botones para descargar
    frame_buttons = ttk.Frame(frame_download)
    frame_buttons.pack(pady=20)
    ttk.Button(frame_buttons, text="Descargar", bootstyle=SUCCESS, command=lambda: download_dates(
        DateService.dateToString(boleteos_desde.entry.get()), 
        DateService.dateToString(boleteos_hasta.entry.get()), 
        DateService.dateToString(cuadres_desde.entry.get()), 
        DateService.dateToString(cuadres_hasta.entry.get()),
        output_folder_var.get()
    )).grid(row=0, column=0, padx=10)

    # ---------------------- Contenido de Carga de Datos ----------------------
    ttk.Label(frame_upload, text="Carga de Datos RRHH", font=("Helvetica", 16)).pack(pady=10)

    # Crear selectores de archivo para boleteos y cuadres
    boleteos_var = create_file_selector(frame_upload, "Boleteos")
    cuadres_var = create_file_selector(frame_upload, "Cuadres de Caja")

    # Botón para cargar los archivos
    ttk.Button(frame_upload, text="Cargar", bootstyle=SUCCESS, command=lambda: upload_files(boleteos_var.get(), cuadres_var.get())).pack(pady=20)

    # Iniciar la aplicación
    root.mainloop()


def create_date_range_selector(parent, label_text):
    """
    Crea un selector de rango de fechas con DateEntry para seleccionar "Desde" y "Hasta".

    Args:
        parent (ttk.Frame): El frame donde se añadirá el selector.
        label_text (str): Texto descriptivo para el selector de fecha.

    Returns:
        (DateEntry, DateEntry): Entradas de fecha "Desde" y "Hasta".
    """
    ttk.Label(parent, text=label_text).pack(anchor=W, pady=5)
    frame_dates = ttk.Frame(parent)
    frame_dates.pack(anchor=W, pady=5)

    ttk.Label(frame_dates, text="Desde:").grid(row=0, column=0, padx=(20, 0), pady=5)
    desde_entry = DateEntry(frame_dates, width=15)
    desde_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_dates, text="Hasta:").grid(row=0, column=2, padx=(80, 0), pady=5)
    hasta_entry = DateEntry(frame_dates, width=15)
    hasta_entry.grid(row=0, column=3, padx=5, pady=5)

    return desde_entry, hasta_entry


def create_folder_selector(parent):
    """
    Crea un selector de carpeta para guardar los archivos.

    Args:
        parent (ttk.Frame): El frame donde se añadirá el selector.

    Returns:
        ttk.StringVar: Variable con la ruta seleccionada.
    """
    ttk.Label(parent, text="Carpeta de salida:").pack(anchor=W, pady=5)
    frame_folder = ttk.Frame(parent)
    frame_folder.pack(fill=X, pady=10)

    folder_var = ttk.StringVar()
    folder_entry = ttk.Entry(frame_folder, textvariable=folder_var, state=DISABLED)
    folder_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

    ttk.Button(frame_folder, text="Seleccionar Carpeta", bootstyle=PRIMARY, command=lambda: select_folder(folder_var)).pack(side=LEFT, padx=5)
    return folder_var


def create_file_selector(parent, label_text):
    """
    Crea un selector de archivo para cargar un archivo específico.

    Args:
        parent (ttk.Frame): El frame donde se añadirá el selector.
        label_text (str): Texto descriptivo para el archivo.

    Returns:
        ttk.StringVar: Variable con la ruta seleccionada.
    """
    frame_file = ttk.Frame(parent)
    frame_file.pack(anchor=W, pady=5)

    ttk.Label(frame_file, text=label_text).grid(row=0, column=0, padx=0, pady=5)
    file_var = ttk.StringVar()
    file_entry = ttk.Entry(frame_file, textvariable=file_var, state=DISABLED, width=50)
    file_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(frame_file, text="Seleccionar Archivo", bootstyle=PRIMARY, command=lambda: select_file(file_var)).grid(row=0, column=2, padx=5, pady=5)

    return file_var


def select_folder(folder_var):
    """
    Abre un cuadro de diálogo para seleccionar una carpeta y asigna la ruta al Entry.
    """
    folder_path = filedialog.askdirectory(title="Seleccionar Carpeta de Salida")
    if folder_path:
        folder_var.set(folder_path)


def select_file(file_var):
    """
    Abre un cuadro de diálogo para seleccionar un archivo y asigna la ruta al Entry.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if file_path:
        file_var.set(file_path)


def upload_files(boleteos_path, cuadres_path):
    """
    Simula la carga de archivos seleccionados y muestra las rutas.
    """

    print("Archivos seleccionados para carga:")
    print(f"Boleteos: {boleteos_path}")
    print(f"Cuadres de Caja: {cuadres_path}")


def download_dates(boleteos_desde, boleteos_hasta, cuadres_desde, cuadres_hasta, output_folder):
    """
    Imprime las fechas seleccionadas para boleteos y cuadres de caja en formato YYYY-MM-DD,
    y la carpeta de salida seleccionada.
    """
    print("Fechas seleccionadas:")
    print(f"Boleteos - Desde: {boleteos_desde} Hasta: {boleteos_hasta}")
    print(f"Cuadres de Caja - Desde: {cuadres_desde} Hasta: {cuadres_hasta}")
    print(f"Carpeta de salida: {output_folder}")

    # añadele a la carpeta de salida el nombre de la carpeta de salida
    rawDataPathBoleteos = os.path.join(output_folder, "boleteos_raw.xlsx")
    processedDataPathBoleteos = os.path.join(output_folder, "boleteos_processed.xlsx")

    dynamicsModel = ModelDynamics()
    processBoleteos(dynamicsModel, boleteos_desde, boleteos_hasta, rawDataPathBoleteos, processedDataPathBoleteos)


if __name__ == "__main__":
    create_gui()
