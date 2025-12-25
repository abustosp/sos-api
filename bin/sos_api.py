import requests
import json
import os
import csv
import concurrent.futures
import datetime
from tkinter.messagebox import showinfo


def login_usuario(credenciales:str = "bin/Login.json"):
  '''
  Funcion para realizar el login en la API de SOS-Contador y obtener el token de acceso a la API

  '''
  # Pagina de login de la API
  url = "https://api.sos-contador.com/api-comunidad/login"

  # Cargar el archivo JSON con las credenciales
  payload = json.dumps(json.load(open(rf"{credenciales}")))

 # Crear el encabezado de la peticion
  headers = {'Content-Type' : 'application/json'}

  # Se realiza la peticion POST
  response = requests.request("POST", url, headers=headers, data=payload)

  # Exportar el resultado a un archivo JSON
  with open('response.json', 'w') as f:
    json.dump(response.json(), f, indent=4)

  # Exportar los datos de login a CSV
  response_data = response.json()
  with open('login_usuario.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['jwt', 'usuario', 'nombre', 'apellido', 'email', 'cantidad_cuits']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')
    writer.writeheader()
    writer.writerow({
      'jwt': response_data.get('jwt', ''),
      'usuario': response_data.get('usuario', ''),
      'nombre': response_data.get('nombre', ''),
      'apellido': response_data.get('apellido', ''),
      'email': response_data.get('email', ''),
      'cantidad_cuits': len(response_data.get('cuits', []))
    })

  return response.json(), response.json()['jwt'] , payload , headers


def login_cuit():
  '''
  Funcion para obtener los bearer token de la API de SOS-Contador por cada contribuyente

  ---
  - pd: las claves se deben reiniciar todos los lunes
  '''

  # se crea la carpeta Token si no existe
  if not os.path.exists('Token'):
    os.makedirs('Token')

  # Se obtiene el response del login, el jwt y el payload
  responseLogin, jwt, payload , header = login_usuario()

  url = 'https://api.sos-contador.com/api-comunidad/cuit/credentials/'
  
  # Obter el mes y año del período anterior
  mes_anterior = (datetime.datetime.now() - datetime.timedelta(days=30)).month
  año_anterior = (datetime.datetime.now() - datetime.timedelta(days=30)).year

  # Abrir el archivo CSV para escribir los datos
  with open('contribuyentes.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'cuit', 'razon_social', 'año', 'mes', 'F2002', 'jwt']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames , delimiter='|')
    writer.writeheader()


    def fetch_token(i):
      payload = ""
      id = i['id']
      cuit = i['cuit']
      razon_social = i['razonsocial']

      url2 = url + str(id)
      header = {'Content-Type': 'application/json'}
      header['Authorization'] = f"Bearer {jwt}"

      # Se realiza la peticion GET
      response = requests.request("GET", url2, headers=header, data=payload)
      
      # Exportar el resultado a un archivo JSON por cada contribuyente
      with open(f'Token/response_{cuit}_{id}_{razon_social}.json', 'w') as f:
        json.dump(response.json(), f, indent=4)
      
      # Escribir los datos en el archivo CSV
      return {'id': id, 'cuit': cuit, 'razon_social': razon_social, 'año': año_anterior, 'mes': mes_anterior, 'F2002': 'SI', 'jwt': response.json()['jwt']}

    # por cada 'id' en 'cuits' del response se obtiene el bearer token concurrentemente
    with concurrent.futures.ThreadPoolExecutor() as executor:
      results = list(executor.map(fetch_token, responseLogin['cuits']))

    # Escribir los datos en el archivo CSV
    for result in results:
      writer.writerow(result)
      
  showinfo(title="Termimando", message="Credenciales Obtenidas")
      
def consulta_f2002():
  
  # Abrir el csv de "contribuyentes.csv" que posee los datos necesarios para hacer la consulta ("cuit"|"razon_social"|"jwt"|"año"|"mes"|"F2002")
  
  url = "https://api.sos-contador.com/api-comunidad/iva/listado/:ejercicio?anio=AAAA&mes=MM"
  
  archivo = "contribuyentes.csv"
  with open(archivo, 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='|')
    def fetch_f2002(row):
      if row['F2002'] == 'SI':
        cuit = row['cuit']
        razon_social = row['razon_social']
        jwt = row['jwt']
        año = row['año']
        mes = row['mes']
        url_f2002 = url.replace('AAAA', año).replace('MM', mes)
        header = {'Content-Type': 'application/json'}
        header['Authorization'] = f"Bearer {jwt}"
        response = requests.request("GET", url_f2002, headers=header)
        
        # se crea la carpeta F2002 si no existe
        if not os.path.exists('F2002'):
          os.makedirs('F2002')
      
        with open(f'F2002/F2002_{cuit}_{razon_social}_{año}_{mes}.json', 'w') as f:
          json.dump(response.json(), f, indent=4)

    # Ejecutar las consultas de forma concurrente
    with concurrent.futures.ThreadPoolExecutor() as executor:
      executor.map(fetch_f2002, reader)
      
  showinfo(title="Terminado" , message="Papeles de trabajo descargados en la carpeta F2002")


if __name__=="__main__":
  login_cuit()
  #consulta_f2002()