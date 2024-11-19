import requests
import pandas as pd
from datetime import datetime, timedelta
import json


class ModelDynamics:
    """
    Clase para interactuar con la API de Dynamics y obtener datos de boleteos en un rango de fechas.
    """

    def __init__(self):
        """
        Inicializa la clase ModelDynamics y obtiene el token de autenticación necesario
        para interactuar con la API de Dynamics.
        """
        self.token = self._getToken()

    def _getToken(self):
        """
        Obtiene el token de autenticación desde la API de Microsoft.

        Returns:
            str: Token de autenticación en formato Bearer si la solicitud es exitosa.
            None: Si ocurre un error durante la obtención del token.
        """
        try:
            urlToken = "https://mistr.operations.dynamics.com/"
            credentials = {
                "client_id": "53f3c906-9bfc-4a5d-89d8-30ce9a672481",
                "client_secret": "zNA3~9-5wuywwiflFbAP52cgJ_5wQ__Y48",
                "resource": urlToken,
                "grant_type": "client_credentials",
            }

            endpoint = "https://login.microsoftonline.com/ceb88b8e-4e6a-4561-a112-5cf771712517/oauth2/token"
            response = requests.post(endpoint, data=credentials)

            if response.status_code == 200:
                token = response.json().get("access_token")
                return f"Bearer {token}"
            else:
                print(f"Error al obtener el token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error en la función _getToken: {str(e)}")
            return None

    def getBoleteos(self, fechaInicio, fechaFin):
        """
        Obtiene los datos de boleteos desde la API de Dynamics en un rango de fechas.

        Args:
            fechaInicio (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            fechaFin (str): Fecha de fin en formato 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: DataFrame con los datos combinados de boleteos si se encuentran datos.
            None: Si no se encuentran datos o si ocurre un error.
        """
        urlBoleteos = (
            "https://mistr.operations.dynamics.com/api/services/"
            "TRU_BoleteoDataGroupService/TRU_BoleteoDataService/extract"
        )
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

        # Convertir las fechas de inicio y fin en objetos datetime
        desdeDate = datetime.strptime(fechaInicio, "%Y-%m-%d")
        hastaDate = datetime.strptime(fechaFin, "%Y-%m-%d")
        delta = timedelta(days=8)  # Dividir el rango en bloques de 8 días

        allData = []

        # Iterar por el rango de fechas en bloques de 8 días
        while desdeDate <= hastaDate:
            try:
                # Calcular el rango del bloque actual
                toDate = min(desdeDate + delta - timedelta(days=1), hastaDate)
                print(f"Procesando boleteos desde {desdeDate.strftime('%Y-%m-%d')} hasta {toDate.strftime('%Y-%m-%d')}")

                # Crear el payload para la solicitud
                payload = {
                    "DataAreaId": "TRV",
                    "FromDate": desdeDate.strftime("%Y-%m-%d"),
                    "ToDate": toDate.strftime("%Y-%m-%d"),
                }

                # Realizar la solicitud a la API
                response = requests.post(urlBoleteos, headers=headers, json=payload)

                if response.status_code == 200:
                    dataDict = response.json().get("Data", [])
                    if dataDict:
                        df = pd.DataFrame(dataDict)
                        allData.append(df)
                    else:
                        print(f"No se encontraron datos en el rango: {desdeDate} - {toDate}")
                else:
                    print(f"Error en la API: {response.status_code} - {response.text}")
                    return None
            except Exception as e:
                print(f"Error al procesar datos en el rango: {desdeDate} - {toDate}: {str(e)}")
                return None

            # Avanzar al siguiente bloque
            desdeDate = toDate + timedelta(days=1)

        # Combinar todos los bloques en un solo DataFrame
        if allData:
            combinedDf = pd.concat(allData, ignore_index=True)
            return combinedDf
        else:
            print("No se encontraron datos en el rango especificado.")
            return None
    
    def getCuadresCaja(self, fechaInicio, fechaFin):
        """
        Obtiene los datos de cuadres de caja desde la API de Dynamics.

        Args:
            desde (str): Fecha de inicio en formato 'YYYY-MM-DD'.
            hasta (str): Fecha de fin en formato 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: DataFrame con los datos de cuadres de caja.
            None: Si ocurre un error o no se encuentran datos.
        """
        urlCuadresCaja = (
            "https://mistr.operations.dynamics.com/api/services/"
            "TRU_BoleteoDataGroupService/TRU_CuadreCajaDataService/extract"
        )

        # Preparar el payload para la solicitud
        payload ={
            "DataAreaId": "TRV",
            "FromDate": fechaInicio,
            "ToDate": fechaFin,
        }

        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

        # Realizar la solicitud a la API
        response = requests.post(urlCuadresCaja, headers=headers, json=payload)

        if response.status_code == 200:
            # Convertir los datos en un DataFrame
            dataDict = response.json().get("Data", [])
            df = pd.DataFrame.from_dict(dataDict)

            print(f"Datos obtenidos exitosamente desde {fechaInicio} hasta {fechaFin}.")
            return df
        else:
            print(f"Error al obtener los cuadres de caja: {response.status_code} - {response.text}")
            return None

