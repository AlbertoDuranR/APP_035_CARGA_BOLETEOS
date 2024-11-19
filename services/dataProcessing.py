import os
import pandas as pd


class DataProcessor:

    @staticmethod
    def processDataBoleteos(df):
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

