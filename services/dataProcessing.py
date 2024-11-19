import os
import pandas as pd


class DataProcessor:
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
    def processData(df):
        """
        Procesa los datos, agrupándolos por columnas clave y sumando los valores.

        Args:
            df (pd.DataFrame): DataFrame sin procesar.

        Returns:
            pd.DataFrame: DataFrame procesado.
        """
        requiredColumns = {"DPNumberDocumId_PE", "Boleteo", "InvoiceAmount"}
        if not requiredColumns.issubset(df.columns):
            raise ValueError("Faltan columnas requeridas en el DataFrame.")

        groupedDf = df.groupby(["DPNumberDocumId_PE", "Boleteo"], as_index=False)["InvoiceAmount"].sum()
        return groupedDf

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
