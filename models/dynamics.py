import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta



class ModelDynamics:
    def __init__(self):
        self.token = self._getToken()

    def _getToken(self):
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
        urlBoleteos = (
            "https://mistr.operations.dynamics.com/api/services/"
            "TRU_BoleteoDataGroupService/TRU_BoleteoDataService/extract"
        )
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json",
        }

        desdeDate = datetime.strptime(fechaInicio, "%Y-%m-%d")
        hastaDate = datetime.strptime(fechaFin, "%Y-%m-%d")
        delta = timedelta(days=8)

        allData = []

        while desdeDate <= hastaDate:
            try:
                toDate = min(desdeDate + delta - timedelta(days=1), hastaDate)
                print(f"Procesando boleteos desde {desdeDate.strftime('%Y-%m-%d')} hasta {toDate.strftime('%Y-%m-%d')}")

                payload = {
                    "DataAreaId": "TRV",
                    "FromDate": desdeDate.strftime("%Y-%m-%d"),
                    "ToDate": toDate.strftime("%Y-%m-%d"),
                }

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

            desdeDate = toDate + timedelta(days=1)

        if allData:
            combinedDf = pd.concat(allData, ignore_index=True)
            return combinedDf
        else:
            print("No se encontraron datos en el rango especificado.")
            return None
