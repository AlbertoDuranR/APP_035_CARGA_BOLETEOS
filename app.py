from models.dynamics import ModelDynamics
from services.dataProcessing import DataProcessor
from services.excelService import ExcelService
import os

if __name__ == "__main__":
    fechaInicio = "2024-01-01"
    fechaFin = "2024-01-03"

    # Directorios de salida
    rawDataPath = os.path.join("excel", "original", "boleteos_raw.xlsx")
    processedDataPath = os.path.join("excel", "procesados", "boleteos_processed.xlsx")

    dynamicsModel = ModelDynamics()
    rawData = dynamicsModel.getBoleteos(fechaInicio, fechaFin)

    if rawData is not None:
        # Guardar datos sin procesar
        ExcelService.saveRawData(rawData, rawDataPath)

        # Procesar datos
        try:
            processedData = DataProcessor.processDataBoleteos(rawData)

            # Guardar datos procesados
            ExcelService.saveProcessedData(processedData, processedDataPath)
        except ValueError as e:
            print(f"Error al procesar los datos: {str(e)}")
    else:
        print("No se pudo obtener datos de Dynamics.")
