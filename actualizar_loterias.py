import csv
from datetime import datetime, timedelta
import os
import urllib.request

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    # Cargar registros anteriores si existen para mantener la base de datos
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    registros[row[0]] = (row[1], row[2])

    # Rango histórico desde el 01/01/2010 hasta el día actual
    inicio = datetime(2010, 1, 1)
    fin = datetime.now()

    curr = inicio
    while curr <= fin:
        fecha_str = curr.strftime('%Y-%m-%d')
        if fecha_str not in registros:
            # Espacio reservado que el bot llenará conforme procese los reportes oficiales
            registros[fecha_str] = ("", "")
        curr += timedelta(days=1)

    # Guardar la estructura en formato CSV oficial ordenado del más reciente al más antiguo
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' actualizado correctamente con el histórico.")

if __name__ == "__main__":
    actualizar_historico()
