import requests, os
from dotenv import load_dotenv

class ModelRrHh:
    def __init__(self):
        load_dotenv()
        self.url_base = os.getenv("BASE_URL")


    def clean(self):
        try:
            url = f"{self.url_base}/cleanData"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "message": "Error al limpiar los datos"}
            
        except Exception as e:
            return {"success": False, "message": f"Error al limpiar los datos: {str(e)}"}

        

    def setBoleteos(self, df):
        """
        Procesa y envía los boletos al endpoint especificado.

        Args:
            df (pd.DataFrame): DataFrame con los datos de los boletos.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            # Validar que las columnas requeridas existan
            required_columns = {"DPNumberDocumId_PE", "Boleto", "InvoiceAmount"}
            if not required_columns.issubset(df.columns):
                raise ValueError("El DataFrame no contiene las columnas requeridas: DPNumberDocumId_PE, Boleto, InvoiceAmount.")

            # Procesar el DataFrame
            df["InvoiceAmount"] = df["InvoiceAmount"].astype(float)  # Asegurar que los montos sean flotantes
            df = df.drop_duplicates()  # Eliminar duplicados si es necesario

            # Convertir DataFrame a JSON
            json_data = df.to_dict(orient="records")

            # Enviar los datos al endpoint
            url = f"{self.url_base}/saveDataBoleteos"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=json_data, headers=headers)

            # Validar respuesta del servidor
            if response.status_code == 200:
                return {"success": True, "message": "Datos enviados correctamente", "response": response.json()}
            else:
                return {"success": False, "message": f"Error al enviar datos: {response.status_code}", "response": response.text}

        except Exception as e:
            return {"success": False, "message": f"Error al procesar y enviar los datos: {str(e)}"}
        
    def setCuadresCaja(self, df):
        """
        Procesa y envía los cuadres de caja al endpoint especificado.

        Args:
            df (pd.DataFrame): DataFrame con los datos de los cuadres de caja.

        Returns:
            dict: Respuesta del servidor.
        """
        try:
            # Validar que las columnas requeridas existan
            required_columns = {"DPNumberDocumId_PE", "Amount"}
            if not required_columns.issubset(df.columns):
                raise ValueError("El DataFrame no contiene las columnas requeridas: DPNumberDocumId_PE, Amount.")

            # Convertir DataFrame a JSON
            json_data = df.to_dict(orient="records")

            # Enviar los datos al endpoint
            url = f"{self.url_base}/saveDataCuadres"
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=json_data, headers=headers)

            # Validar respuesta del servidor
            if response.status_code == 200:
                return {"success": True, "message": "Datos enviados correctamente", "response": response.json()}
            else:
                return {"success": False, "message": f"Error al enviar datos: {response.status_code}", "response": response.text}

        except Exception as e:
            return {"success": False, "message": f"Error al procesar y enviar los datos: {str(e)}"}