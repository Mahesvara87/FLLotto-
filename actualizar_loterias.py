import csv
from datetime import datetime, timedelta
import os

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    registros = {}
    # Si ya existe el archivo, leemos lo que tenga
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    # Si tiene los datos falsos anteriores, los dejamos vacíos para llenarlos bien
                    if row[1] == "3 74 38 47":
                        registros[row[0]] = ("", "")
                    else:
                        registros[row[0]] = (row[1], row[2])

    # Generar el rango desde 2010 hasta hoy limpio
    inicio = datetime(2010, 1, 1)
    fin = datetime.now()
    curr = inicio
    while curr <= fin:
        fecha_str = curr.strftime('%Y-%m-%d')
        if fecha_str not in registros:
            registros[fecha_str] = ("", "")
        curr += timedelta(days=1)

    # Guardar CSV limpio
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Archivo '{nombre_archivo}' limpiado y actualizado correctamente.")

if __name__ == "__main__":
    actualizar_historico()
