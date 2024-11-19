import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from datetime import datetime
from services.dateService import DateService

def create_gui():
    # Crear la ventana principal
    root = ttk.Window(themename="journal")
    root.title("Gestión de Datos")
    root.geometry("500x400")

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
    # Etiqueta principal
    ttk.Label(frame_download, text="Descarga de Datos Dynamics", font=("Helvetica", 16)).pack(pady=10)

    # Sección de boleteos
    ttk.Label(frame_download, text="Seleccione los rangos de fecha para Boleteos").pack(anchor=W, pady=5)
    frame_boleteos = ttk.Frame(frame_download)
    frame_boleteos.pack(anchor=W, pady=5)
    ttk.Label(frame_boleteos, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
    boleteos_desde = DateEntry(frame_boleteos, width=15)
    boleteos_desde.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame_boleteos, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
    boleteos_hasta = DateEntry(frame_boleteos, width=15)
    boleteos_hasta.grid(row=0, column=3, padx=5, pady=5)

    # Sección de cuadres de caja
    ttk.Label(frame_download, text="Seleccione los rangos de fecha para Cuadres de Caja").pack(anchor=W, pady=5)
    frame_cuadres = ttk.Frame(frame_download)
    frame_cuadres.pack(anchor=W, pady=5)
    ttk.Label(frame_cuadres, text="Desde:").grid(row=0, column=0, padx=5, pady=5)
    cuadres_desde = DateEntry(frame_cuadres, width=15)
    cuadres_desde.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame_cuadres, text="Hasta:").grid(row=0, column=2, padx=5, pady=5)
    cuadres_hasta = DateEntry(frame_cuadres, width=15)
    cuadres_hasta.grid(row=0, column=3, padx=5, pady=5)

    # Botones para descargar y abrir carpeta de salida
    frame_buttons = ttk.Frame(frame_download)
    frame_buttons.pack(pady=20)
    ttk.Button(frame_buttons, text="Descargar", bootstyle=SUCCESS, command=lambda: download_dates(
        DateService.dateToString(boleteos_desde.entry.get()), 
        DateService.dateToString(boleteos_hasta.entry.get()), 
        DateService.dateToString(cuadres_desde.entry.get()), 
        DateService.dateToString(cuadres_hasta.entry.get())
    )).grid(row=0, column=0, padx=10)
    ttk.Button(frame_buttons, text="Abrir carpeta de salida", bootstyle=INFO).grid(row=0, column=1, padx=10)

    # ---------------------- Contenido de Carga de Datos ----------------------
    # Etiqueta principal
    ttk.Label(frame_upload, text="Carga de Datos RRHH", font=("Helvetica", 16)).pack(pady=10)

    # Sección de carga de archivos
    frame_upload_files = ttk.Frame(frame_upload)
    frame_upload_files.pack(pady=10)
    ttk.Label(frame_upload_files, text="Boleteos").grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(frame_upload_files, text="Seleccionar Archivo", bootstyle=PRIMARY).grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(frame_upload_files, text="Cuadres de Caja").grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(frame_upload_files, text="Seleccionar Archivo", bootstyle=PRIMARY).grid(row=1, column=1, padx=5, pady=5)

    # Botón para cargar los archivos
    ttk.Button(frame_upload, text="Cargar", bootstyle=SUCCESS).pack(pady=20)

    # Iniciar la aplicación
    root.mainloop()


def download_dates(boleteos_desde, boleteos_hasta, cuadres_desde, cuadres_hasta):
    """
    Imprime las fechas seleccionadas para boleteos y cuadres de caja en formato YYYY-MM-DD.

    Args:
        boleteos_desde (str): Fecha de inicio para boleteos.
        boleteos_hasta (str): Fecha de fin para boleteos.
        cuadres_desde (str): Fecha de inicio para cuadres de caja.
        cuadres_hasta (str): Fecha de fin para cuadres de caja.
    """
    # Imprimir las fechas seleccionadas
    print("Fechas seleccionadas:")
    print(f"Boleteos - Desde: {boleteos_desde} Hasta: {boleteos_hasta}")
    print(f"Cuadres de Caja - Desde: {cuadres_desde} Hasta: {cuadres_hasta}")


if __name__ == "__main__":
    create_gui()
