import os
import pandas as pd


class ExcelService:
    @staticmethod
    def saveRawData(df, filePath):
        """
        Guarda los datos sin procesar en un archivo Excel.

        Args:
            df (pd.DataFrame): DataFrame con los datos a guardar.
            filePath (str): Ruta del archivo Excel.
        """
        df.to_excel(filePath, index=False)
        print(f"Datos sin procesar guardados en: {filePath}")


    @staticmethod
    def saveProcessedData(df, filePath):
        """
        Guarda los datos procesados en un archivo Excel.

        Args:
            df (pd.DataFrame): DataFrame con los datos procesados.
            filePath (str): Ruta del archivo Excel.
        """
        df.to_excel(filePath, index=False)
        print(f"Datos procesados guardados en: {filePath}")
    
    @staticmethod
    def readExcel(filePath):
        """
        Lee un archivo Excel y devuelve un DataFrame.

        Args:
            filePath (str): Ruta del archivo Excel.

        Returns:
            pd.DataFrame: DataFrame con los datos del archivo Excel.
        """
        return pd.read_excel(filePath)
