from models.dynamics import ModelDynamics
from services.dataProcessing import DataProcessor
from services.excelService import ExcelService
import os


def processBoleteos(dynamicsModel, fechaInicio, fechaFin, rawDataPath, processedDataPath):
    """
    Procesa los datos de boleteos desde Dynamics, guardando los datos sin procesar y procesados.

    Args:
        dynamicsModel (ModelDynamics): Instancia del modelo Dynamics.
        fechaInicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        fechaFin (str): Fecha de fin en formato 'YYYY-MM-DD'.
        rawDataPath (str): Ruta para guardar los datos sin procesar.
        processedDataPath (str): Ruta para guardar los datos procesados.
    """
    rawData = dynamicsModel.getBoleteos(fechaInicio, fechaFin)

    if rawData is not None:
        # Guardar datos sin procesar
        ExcelService.saveRawData(rawData, rawDataPath)

        # Procesar datos
        try:
            processedData = DataProcessor.processDataBoleteos(rawData)

            # Guardar datos procesados
            ExcelService.saveProcessedData(processedData, processedDataPath)
            print("Boleteos procesados correctamente.")
        except ValueError as e:
            print(f"Error al procesar los datos de boleteos: {str(e)}")
    else:
        print("No se pudieron obtener datos de boleteos.")


def processCuadresCaja(dynamicsModel, fechaInicio, fechaFin, rawDataPath, processedDataPath):
    """
    Procesa los datos de cuadres de caja desde Dynamics, guardando los datos sin procesar y procesados.

    Args:
        dynamicsModel (ModelDynamics): Instancia del modelo Dynamics.
        fechaInicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
        fechaFin (str): Fecha de fin en formato 'YYYY-MM-DD'.
        rawDataPath (str): Ruta para guardar los datos sin procesar.
        processedDataPath (str): Ruta para guardar los datos procesados.
    """
    rawData = dynamicsModel.getCuadresCaja(fechaInicio, fechaFin)

    if rawData is not None:
        # Guardar datos sin procesar
        ExcelService.saveRawData(rawData, rawDataPath)

        # Procesar datos
        try:
            processedData = DataProcessor.processDataCuadresCaja(rawData)

            # Guardar datos procesados
            ExcelService.saveProcessedData(processedData, processedDataPath)
            print("Cuadres de caja procesados correctamente.")
        except ValueError as e:
            print(f"Error al procesar los datos de cuadres de caja: {str(e)}")
    else:
        print("No se pudieron obtener datos de cuadres de caja.")


if __name__ == "__main__":
    # Configuración de fechas
    fechaInicio = "2024-01-01"
    fechaFin = "2024-01-03"

    # Directorios de salida Boleteos
    rawDataPathBoleteos = os.path.join("excel", "original", "boleteos_raw.xlsx")
    processedDataPathBoleteos = os.path.join("excel", "procesados", "boleteos_processed.xlsx")

    # Directorios de salida Cuadres de caja
    rawDataPathCuadres = os.path.join("excel", "original", "cuadres_raw.xlsx")
    processedDataPathCuadres = os.path.join("excel", "procesados", "cuadres_processed.xlsx")

    # Instanciar el modelo de Dynamics
    dynamicsModel = ModelDynamics()

    # Procesar Boleteos
    # processBoleteos(dynamicsModel, fechaInicio, fechaFin, rawDataPathBoleteos, processedDataPathBoleteos)

    # # Procesar Cuadres de Caja
    processCuadresCaja(dynamicsModel, fechaInicio, fechaFin, rawDataPathCuadres, processedDataPathCuadres)
