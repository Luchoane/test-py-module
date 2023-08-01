import sys
import requests
import json

def analizar_prompt_openai(api_key, archivo_ruta):
    try:
        # URL de la API de OpenAI
        url = "https://api.openai.com/v1/completions"
        
        # Configurar los encabezados de la solicitud con la clave de la API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        with open(archivo_ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        datos_json = {
            'contenido': contenido
        }

        # Convertir el objeto JSON en una cadena JSON
        datos_json_str = json.dumps(datos_json["contenido"])

        p = '''
        Hola ChatGPT, necesito tu ayuda para identificar las POTENCIALES vulnerabilidades CRITICAS en este código. Por favor, analiza el siguiente fragmento (recuerda que no es el código completo, sólo un fragmento) y completa el JSON con la información pertinente, responde UNICAMENTE con el json. En caso de que la POTENCIAL vulnerabilidad no sea lo suficientemente crítica, rellena los campos del json con "NO CRITICAMENTE VULNERABLE":

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

        # Configurar el payload con el prompt
        payload = {
            "model": "text-davinci-003",
            "prompt": p,
            "temperature": 0,
            "max_tokens": 700
        }
        
        # print(payload)
        
        # Enviar la solicitud POST con el prompt a la API de OpenAI
        response = requests.post(url, headers=headers, json=payload)
        
        # Verificar la respuesta del servidor
        if response.status_code == 200:
            respuesta_json = response.json()
            # print("Respuesta de OpenAI:")
            print(respuesta_json["choices"][0]["text"])
            # print('\n----------------------\n')
            # print(respuesta_json)
            return respuesta_json["choices"][0]["text"]
        else:
            print(f"Error al enviar el prompt. Código de estado: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python enviar2.py <Ruta_del_archivo> <api_key>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    api_key = sys.argv[2]

    try:
        # Leer el contenido del archivo
        #with open(ruta_archivo, 'r') as archivo:
        #   contenido = archivo.read()

        # Enviar el contenido del archivo como prompt a OpenAI para analizarlo
        analizar_prompt_openai(api_key, ruta_archivo)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == '__main__':
    main()
