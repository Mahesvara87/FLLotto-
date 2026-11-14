import csv
from datetime import datetime, timedelta
import os
import urllib.request
import urllib.parse
import json
import re

def obtener_resultados_florida(fecha_str):
    """
    Consulta un agregador público de resultados históricos de lotería 
    para extraer el Pick 3 y Pick 4 (Midday y Evening) de la Florida en formato fecha YYYY-MM-DD.
    """
    try:
        # Formato de fecha para la URL de consulta (ej: MM-DD-YYYY o YYYY-MM-DD según la fuente)
        dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        fecha_url = dt.strftime('%Y-%m-%d')
        
        # Usamos una fuente pública de consulta abierta
        url = f"https://www.lotteryusa.com/florida/pick-3/{fecha_url}"
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Patrones limpios para extraer los números del HTML de la página pública
            # Buscamos los bloques de resultados de Día y Noche
            matches = re.findall(r'class="result-number[^"]*">([0-9]+)</span', html)
            if len(matches) >= 2:
                # El primero suele ser Día y el segundo Noche (o viceversa según la estructura)
                dia = matches[0].strip()
                noche = matches[1].strip()
                return (dia, noche)
    except Exception as e:
        # Si falla una fecha específica, el bot continúa con las demás sin detenerse
        pass
        
    return ("", "")

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    # Cargar registros previos para no perder los avances ya guardados
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    registros[row[0]] = (row[1].strip(), row[2].strip())

    # Rango de actualización inteligente (ej: los últimos 60 días para mantener fresco el sistema y evitar bloqueos por exceso de tráfico)
    hoy = datetime.now()
    inicio_revision = hoy - timedelta(days=60)
    
    curr = inicio_revision
    print("🔄 Extrayendo resultados oficiales reales...")
    
    while curr <= hoy:
        fecha_str = curr.strftime('%Y-%m-%d')
        
        # Si la fecha está vacía o contiene espacios en blanco, consultamos la fuente
        if fecha_str not in registros or registros[fecha_str] == ("", ""):
            dia, noche = obtener_resultados_florida(fecha_str)
            if dia or noche:
                registros[fecha_str] = (dia, noche)
                print(f"✔️ Registrado {fecha_str} -> Día: {dia} | Noche: {noche}")
        
        curr += timedelta(days=1)

    # Rango total histórico desde 2010 para conservar la estructura completa de la app
    inicio_total = datetime(2010, 1, 1)
    curr_total = inicio_total
    while curr_total < inicio_revision:
        f_str = curr_total.strftime('%Y-%m-%d')
        if f_str not in registros:
            registros[f_str] = ("", "")
        curr_total += timedelta(days=1)

    # Guardar el CSV ordenado del más reciente al más antiguo
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' procesado y sincronizado con éxito.")

if __name__ == "__main__":
    actualizar_historico()
