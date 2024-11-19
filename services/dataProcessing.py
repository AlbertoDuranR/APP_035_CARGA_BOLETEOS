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


    @staticmethod
    def processDataCuadresCaja(df):
        """
        Procesa los datos de cuadres de caja, aplicando filtros y transformaciones.

        Args:
            df (pd.DataFrame): DataFrame con los datos sin procesar.

        Returns:
            pd.DataFrame: DataFrame con los datos procesados.

        Raises:
            ValueError: Si alguna columna requerida no está presente en el DataFrame.
        """
        requiredColumns = {'DPNumberDocumId_PE', 'Description', 'Amount'}

        # Validar la existencia de las columnas necesarias
        missingColumns = requiredColumns - set(df.columns)
        if missingColumns:
            raise ValueError(f"Faltan columnas requeridas: {', '.join(missingColumns)}")

        # Filtrar filas por descripción
        df = df[~df['Description'].str.contains(
            'POR LOS DESCUENTOS APLICADOS EN LA PLANILLA DE SUELDOS', na=False)]

        # Multiplicar valores de 'Amount' por -1
        df['Amount'] = -df['Amount']

        # Eliminar duplicados
        df = df.drop_duplicates()

        # Agrupar por DPNumberDocumId_PE y sumar Amount
        groupedDf = df.groupby('DPNumberDocumId_PE', as_index=False)['Amount'].sum()

        # Filtrar valores negativos y tomar su valor absoluto usando .loc
        groupedDf = groupedDf.loc[groupedDf['Amount'] < 0]
        groupedDf.loc[:, 'Amount'] = groupedDf['Amount'].abs()

        return groupedDf



