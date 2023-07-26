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
        datos_json_str = json.dumps(datos_json["contenido"])

        p = '''
        Hola ChatGPT, necesito tu ayuda para identificar las vulnerabilidades en este código. Por favor, analiza el siguiente fragmento y completa el JSON con la información pertinente, responde UNICAMENTE con el json:

        {
        "issue": "*",
        "remediation": "*",
        "vulnerable_line": "*"
        }

        Por favor, completa el JSON con la siguiente información:

        - En el campo "issue", especifica la vulnerabilidad encontrada.
        - En el campo "remediation", sugiere una solución o una forma de corregir la vulnerabilidad.
        - En el campo "vulnerable_line", indica la línea de código donde se encuentra la vulnerabilidad.

        ¡Gracias por tu ayuda!

        Code snippet: """
        
        %s

        """
        ''' % (datos_json_str)

        payload = {
            "model": "text-davinci-003",
            "prompt": p,
            "temperature": 0,
            "max_tokens": 700
        }

        # Enviar la solicitud POST con el JSON al servidor
        response = requests.post(url, json=payload)

        # Verificar la respuesta del servidor
        if response.status_code == 200:
            #print("Archivo enviado correctamente.")
            return response.json()
        else:
            print(f"Error al enviar el archivo. Código de estado: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python script.py <Ruta_del_archivo>")
        print('len:', len(sys.argv))
        print('lista:', str(sys.argv))
        sys.exit(1)

    url_servidor = "http://181.99.179.156:9000/process_json"
    ruta_archivo = sys.argv[1]
    
    print(enviar_archivo(url_servidor, ruta_archivo))

if __name__ == '__main__':
    main()
