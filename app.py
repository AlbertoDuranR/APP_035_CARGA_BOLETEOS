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


