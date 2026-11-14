import csv
from datetime import datetime, timedelta
import urllib.request
import json
import os

API_KEY = 'HbtlKhy5YfyKBn3bKkxhtAfgtMS8aAXIl7Y6j6ql'
API_BASE_URL = 'https://api.api-ninjas.com/v1/lottery'

def formatear_numeros(winning_numbers):
    if not winning_numbers:
        return ""
    if isinstance(winning_numbers, list):
        return " ".join(str(n) for n in winning_numbers)
    return str(winning_numbers)

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    # 1. Cargar registros existentes para no perder modificaciones previas
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    registros[row[0]] = (row[1].strip(), row[2].strip())

    # 2. Definir rango a revisar (ej: los últimos 30 días para asegurar actualización fresca y precisa)
    hoy = datetime.now()
    inicio_revision = hoy - timedelta(days=30)
    
    curr = inicio_revision
    print("🔄 Consultando resultados oficiales en la red...")
    
    while curr <= hoy:
        fecha_str = curr.strftime('%Y-%m-%d')
        
        # Si la fecha no tiene datos o tiene datos vacíos/de prueba, los consultamos
        if fecha_str not in registros or registros[fecha_str] == ("", "") or registros[fecha_str][0] == "1 23 45 67":
            dia_str = ""
            noche_str = ""
            try:
                # Consultar Pick 3
                url_p3 = f"{API_BASE_URL}?game=us-fl-pick3&date={fecha_str}"
                req_p3 = urllib.request.Request(url_p3, headers={'X-Api-Key': API_KEY})
                with urllib.request.urlopen(req_p3) as response:
                    data_p3 = json.loads(response.read().decode('utf-8'))
                    if data_p3 and len(data_p3) > 0:
                        dia_str = formatear_numeros(data_p3[0].get('winning_numbers'))

                # Consultar Pick 4
                url_p4 = f"{API_BASE_URL}?game=us-fl-pick4&date={fecha_str}"
                req_p4 = urllib.request.Request(url_p4, headers={'X-Api-Key': API_KEY})
                with urllib.request.urlopen(req_p4) as response:
                    data_p4 = json.loads(response.read().decode('utf-8'))
                    if data_p4 and len(data_p4) > 0:
                        noche_str = formatear_numeros(data_p4[0].get('winning_numbers'))
            except Exception as e:
                print(f"⚠️ Nota en fecha {fecha_str}: {e}")

            registros[fecha_str] = (dia_str, noche_str)
        
        curr += timedelta(days=1)

    # Asegurar que existan registros desde 2010 en adelante en la estructura
    inicio_total = datetime(2010, 1, 1)
    curr_total = inicio_total
    while curr_total < inicio_revision:
        f_str = curr_total.strftime('%Y-%m-%d')
        if f_str not in registros:
            registros[f_str] = ("", "")
        curr_total += timedelta(days=1)

    # 3. Guardar el archivo CSV ordenado del más reciente al más antiguo
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' actualizado con éxito con los datos reales.")

if __name__ == "__main__":
    actualizar_historico()
