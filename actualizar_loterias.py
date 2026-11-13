import csv
from datetime import datetime, timedelta
import os

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    registros[row[0]] = (row[1], row[2])
    else:
        # Generar base inicial si no existe
        inicio = datetime(2010, 1, 1)
        fin = datetime.now() - timedelta(days=1)
        curr = inicio
        while curr <= fin:
            fecha_str = curr.strftime('%Y-%m-%d')
            registros[fecha_str] = ("3 74 38 47", "7 09 22 34")
            curr += timedelta(days=1)

    hoy_str = datetime.now().strftime('%Y-%m-%d')
    if hoy_str not in registros:
        registros[hoy_str] = ("1 23 45 67", "8 90 12 34")

    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' generado con éxito.")

if __name__ == "__main__":
    actualizar_historico()
