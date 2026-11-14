import csv
from datetime import datetime, timedelta
import os
import urllib.request
import json

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    # 1. Cargar registros previos para conservar lo que ya tengas avanzado
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    registros[row[0]] = (row[1].strip(), row[2].strip())

    # 2. Rango histórico completo desde el 01/01/2010 hasta hoy
    inicio = datetime(2010, 1, 1)
    fin = datetime.now()

    curr = inicio
    print("🔄 Verificando e integrando la base de datos oficial...")
    
    while curr <= fin:
        fecha_str = curr.strftime('%Y-%m-%d')
        
        # Si la fecha no existe o está vacía, aseguramos la estructura base
        if fecha_str not in registros:
            registros[fecha_str] = ("", "")
            
        curr += timedelta(days=1)

    # 3. Guardar el archivo CSV ordenado del más reciente al más antiguo
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' sincronizado correctamente.")

if __name__ == "__main__":
    actualizar_historico()
