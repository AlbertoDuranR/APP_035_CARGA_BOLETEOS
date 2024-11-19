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
            DateService.dateToString(boleteos_desde.entry.get()),
            DateService.dateToString(boleteos_hasta.entry.get()),
            DateService.dateToString(cuadres_desde.entry.get()),
            DateService.dateToString(cuadres_hasta.entry.get()),
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

    ttk.Label(frame_dates, text="Hasta:").grid(row=0, column=2, padx=(80, 0), pady=5)
    hasta_entry = DateEntry(frame_dates, width=15)
    hasta_entry.grid(row=0, column=3, padx=5, pady=5)

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
    Realiza el procesamiento de boleteos y cuadres en un hilo separado.
    """
    rawDataPathBoleteos = os.path.join(output_folder, "boleteos_raw.xlsx")
    processedDataPathBoleteos = os.path.join(output_folder, "boleteos_processed.xlsx")

    rawDataCuadres = os.path.join(output_folder, "cuadres_raw.xlsx")
    processedDataCuadres = os.path.join(output_folder, "cuadres_processed.xlsx")

    dynamicsModel = ModelDynamics()
    processBoleteos(dynamicsModel, boleteos_desde, boleteos_hasta, rawDataPathBoleteos, processedDataPathBoleteos)
    processCuadresCaja(dynamicsModel, cuadres_desde, cuadres_hasta, rawDataCuadres, processedDataCuadres)


def upload_files(boleteos_path, cuadres_path):
    """
    Simula la carga de archivos seleccionados y muestra las rutas.
    """
    print("Archivos seleccionados para carga:")
    print(f"Boleteos: {boleteos_path}")
    print(f"Cuadres de Caja: {cuadres_path}")

    rrhhModel = ModelRrHh()

    uploadCuadresCaja(rrhhModel, cuadres_path)




if __name__ == "__main__":
    create_gui()
