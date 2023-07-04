import sys
import requests
import json

def enviar_archivo(url, archivo_ruta):
    try:
        # Leer el contenido del archivo
        with open(archivo_ruta, 'r') as archivo:
            contenido = archivo.read()

        # Crear un objeto JSON con el contenido leído
        datos_json = {
            'contenido': contenido
        }

        # Convertir el objeto JSON en una cadena JSON
        datos_json_str = json.dumps(datos_json)

        # Enviar la solicitud POST con el JSON al servidor
        response = requests.post(url, json=datos_json)

        # Verificar la respuesta del servidor
        if response.status_code == 200:
            print("Archivo enviado correctamente.")
        else:
            print(f"Error al enviar el archivo. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python script.py <Ruta_del_archivo>")
        sys.exit(1)

    url_servidor = "http://181.99.179.156:9000/process_json"
    ruta_archivo = sys.argv[1]
    
    enviar_archivo(url_servidor, ruta_archivo)

if __name__ == '__main__':
    main()
