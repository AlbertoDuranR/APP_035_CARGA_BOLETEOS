import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from tkinter import filedialog
from services.dateService import DateService
from app import processBoleteos, processCuadresCaja, uploadBoleteos, uploadCuadresCaja
from models.dynamics import ModelDynamics
from models.rrhh import ModelRrHh
import os
import threading
from ttkbootstrap.dialogs import Messagebox  # Importa Messagebox correctamente

def create_gui():
    root = ttk.Window(themename="journal")
    root.title("Gestión de Datos")
    root.geometry("600x450")

    # Crear un Notebook para las pestañas
    notebook = ttk.Notebook(root, bootstyle=PRIMARY)
    notebook.pack(fill=BOTH, expand=True)

    # Primera pestaña: Descarga de Datos Dynamics
    frame_download = ttk.Frame(notebook, padding=10)
    notebook.add(frame_download, text="Descarga de Datos Dynamics")

    ttk.Label(frame_download, text="Descarga de Datos Dynamics", font=("Helvetica", 16)).pack(pady=10)

    boleteos_desde, boleteos_hasta = create_date_range_selector(
        frame_download, "Seleccione los rangos de fecha para Boleteos"
    )
    cuadres_desde, cuadres_hasta = create_date_range_selector(
        frame_download, "Seleccione los rangos de fecha para Cuadres de Caja"
    )

    output_folder_var = create_folder_selector(frame_download)

    frame_buttons = ttk.Frame(frame_download)
    frame_buttons.pack(pady=20)

    # Botón de Descargar con threading
    download_button = ttk.Button(frame_buttons, text="Descargar", bootstyle=SUCCESS)
    download_button.grid(row=0, column=0, padx=10)
    download_button.configure(command=lambda: start_thread(
        download_dates,
        args=(
            boleteos_desde.entry.get(),
            boleteos_hasta.entry.get(),
            cuadres_desde.entry.get(),
            cuadres_hasta.entry.get(),
            output_folder_var.get()
        ),
        button=download_button
    ))

    # ---------------------- Contenido de Carga de Datos ----------------------
    frame_upload = ttk.Frame(notebook, padding=10)
    notebook.add(frame_upload, text="Carga de Datos RRHH")

    ttk.Label(frame_upload, text="Carga de Datos RRHH", font=("Helvetica", 16)).pack(pady=10)

    boleteos_var = create_file_selector(frame_upload, "Boleteos")
    cuadres_var = create_file_selector(frame_upload, "Cuadres de Caja")

    # Botón para cargar los archivos con threading
    upload_button = ttk.Button(frame_upload, text="Cargar", bootstyle=SUCCESS)
    upload_button.pack(pady=20)
    upload_button.configure(command=lambda: start_thread(
        upload_files,
        args=(boleteos_var.get(), cuadres_var.get()),
        button=upload_button
    ))

    # Iniciar la aplicación
    root.mainloop()


def create_date_range_selector(parent, label_text):
    ttk.Label(parent, text=label_text).pack(anchor=W, pady=5)
    frame_dates = ttk.Frame(parent)
    frame_dates.pack(anchor=W, pady=5)

    ttk.Label(frame_dates, text="Desde:").grid(row=0, column=0, padx=(20, 0), pady=5)
    desde_entry = DateEntry(frame_dates, width=15)
    desde_entry.grid(row=0, column=1, padx=5, pady=5)
    desde_entry.entry.delete(0, "end")

    ttk.Label(frame_dates, text="Hasta:").grid(row=0, column=2, padx=(80, 0), pady=5)
    hasta_entry = DateEntry(frame_dates, width=15)
    hasta_entry.grid(row=0, column=3, padx=5, pady=5)
    hasta_entry.entry.delete(0, "end")

    return desde_entry, hasta_entry


def create_folder_selector(parent):
    ttk.Label(parent, text="Carpeta de salida:").pack(anchor=W, pady=5)
    frame_folder = ttk.Frame(parent)
    frame_folder.pack(fill=X, pady=10)

    folder_var = ttk.StringVar()
    folder_entry = ttk.Entry(frame_folder, textvariable=folder_var, state=DISABLED)
    folder_entry.pack(side=LEFT, fill=X, expand=YES, padx=5)

    ttk.Button(frame_folder, text="Seleccionar Carpeta", bootstyle=PRIMARY, command=lambda: select_folder(folder_var)).pack(side=LEFT, padx=5)
    return folder_var


def create_file_selector(parent, label_text):
    frame_file = ttk.Frame(parent)
    frame_file.pack(anchor=W, pady=5)

    ttk.Label(frame_file, text=label_text).grid(row=0, column=0, padx=0, pady=5)
    file_var = ttk.StringVar()
    file_entry = ttk.Entry(frame_file, textvariable=file_var, state=DISABLED, width=50)
    file_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(frame_file, text="Seleccionar Archivo", bootstyle=PRIMARY, command=lambda: select_file(file_var)).grid(row=0, column=2, padx=5, pady=5)

    return file_var


def select_folder(folder_var):
    folder_path = filedialog.askdirectory(title="Seleccionar Carpeta de Salida")
    if folder_path:
        folder_var.set(folder_path)


def select_file(file_var):
    file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
    if file_path:
        file_var.set(file_path)


def start_thread(target, args=(), button=None):
    """
    Inicia un hilo para ejecutar un proceso pesado y desactiva el botón asociado.
    """
    if button:
        button.config(state=DISABLED)

    def thread_target():
        target(*args)
        if button:
            button.after(0, lambda: button.config(state=NORMAL))

    threading.Thread(target=thread_target).start()


def download_dates(boleteos_desde, boleteos_hasta, cuadres_desde, cuadres_hasta, output_folder):
    """
    Realiza el procesamiento de boleteos y cuadres con validación de entradas.
    """
    try:
        # Validar las fechas y la carpeta de salida
        if not boleteos_desde or not boleteos_hasta:
            print("Error: Las fechas de boleteos no están definidas.")
            return
        if not cuadres_desde or not cuadres_hasta:
            print("Error: Las fechas de cuadres de caja no están definidas.")
            return
        if not output_folder:
            print("Error: No se ha seleccionado una carpeta de salida.")
            return
        
        boleteos_desde = DateService.stringToDate(boleteos_desde)
        boleteos_hasta = DateService.stringToDate(boleteos_hasta)
        cuadres_desde = DateService.stringToDate(cuadres_desde)
        cuadres_hasta = DateService.stringToDate(cuadres_hasta)

        

        # Crear rutas para archivos
        rawDataPathBoleteos = os.path.join(output_folder, "boleteos_raw.xlsx")
        processedDataPathBoleteos = os.path.join(output_folder, "boleteos_processed.xlsx")

        rawDataCuadres = os.path.join(output_folder, "cuadres_raw.xlsx")
        processedDataCuadres = os.path.join(output_folder, "cuadres_processed.xlsx")

        # Procesar datos de Dynamics
        dynamicsModel = ModelDynamics()
        
        # Procesar boleteos
        processBoleteos(dynamicsModel, boleteos_desde, boleteos_hasta, rawDataPathBoleteos, processedDataPathBoleteos)
        print("Boleteos procesados y guardados correctamente.")

        # Procesar cuadres de caja
        processCuadresCaja(dynamicsModel, cuadres_desde, cuadres_hasta, rawDataCuadres, processedDataCuadres)
        print("Cuadres de caja procesados y guardados correctamente.")

    except Exception as e:
        print(f"Error inesperado durante el procesamiento: {str(e)}")





def upload_files(boleteos_path, cuadres_path):
    """
    Procesa los archivos seleccionados y muestra los mensajes de resultado en la consola.
    """
    rrhhModel = ModelRrHh()

    try:
        if not boleteos_path and not cuadres_path:
            print("Error: No se seleccionaron archivos para cargar.")
            return
        elif not boleteos_path:
            print("Error: No se seleccionó un archivo de boleteos.")
            return
        elif not cuadres_path:
            print("Error: No se seleccionó un archivo de cuadres de caja.")
            return

        # Procesar cuadres de caja
        uploadCuadresCaja(rrhhModel, cuadres_path)

        # Procesar boleteos
        uploadBoleteos(rrhhModel, boleteos_path)

    except Exception as e:
        print(f"Error inesperado durante la carga de archivos: {str(e)}")



if __name__ == "__main__":
    create_gui()
