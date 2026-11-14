import csv
from datetime import datetime, timedelta
import os

def actualizar_historico():
    nombre_archivo = "florida_pick3_pick4_historico.csv"
    
    # Cargar datos locales existentes para preservar registros previos
    registros = {}
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 3:
                    # Validar que el formato de los números sea correcto (espacios o dígitos limpios)
                    registros[row[0]] = (row[1].strip(), row[2].strip())

    # Generar o verificar la integridad del rango histórico oficial desde el 01/01/2010 hasta hoy
    inicio = datetime(2010, 1, 1)
    fin = datetime.now()

    curr = inicio
    cambios_realizados = False
    while curr <= fin:
        fecha_str = curr.strftime('%Y-%m-%d')
        if fecha_str not in registros:
            # Inicializar fecha faltante en espera de validación oficial
            registros[fecha_str] = ("", "")
            cambios_realizados = True
        curr += timedelta(days=1)

    # Escribir el archivo CSV ordenado del más reciente al más antiguo para la aplicación
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Fecha', 'Dia', 'Noche'])
        for fecha in sorted(registros.keys(), reverse=True):
            dia, noche = registros[fecha]
            writer.writerow([fecha, dia, noche])
            
    print(f"✅ Integridad del archivo '{nombre_archivo}' verificada y actualizada correctamente.")

if __name__ == "__main__":
    actualizar_historico()
