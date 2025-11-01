# generar_reporte.py
import subprocess
import os
import sys

# Define la ruta base del proyecto
project_root = os.path.dirname(os.path.abspath(__file__))

# Carpetas de código fuente a cubrir
source_dirs = "core,cli,pygame_ui"

# Carpeta de tests
tests_dir = os.path.join(project_root, "tests")

# Archivo de salida del reporte
report_file = os.path.join(project_root, "coverage_report.txt")

print("--- Iniciando la generación del reporte de cobertura ---")

# --- 1. Ejecutar Pruebas con Coverage ---
command = [
    sys.executable, "-m", "coverage", "run",
    "--source=" + source_dirs,
    "-m", "unittest", "discover", "-s", tests_dir
]

print(f"Ejecutando comando: {' '.join(command)}")

result = subprocess.run(
    command, 
    capture_output=True, 
    text=True, 
    encoding='latin-1'
)

# --- CORRECCIÓN ---
# Hemos comentado el bloque que imprimía el 'stdout' (los prints de los tests)
# para que la salida sea más limpia.
# 
# if result.stdout:
#     print("\nSalida de Pruebas (stdout):")
#     print(result.stdout)

# Dejamos el 'stderr' porque aquí es donde unittest imprime el "OK" o "FAILED"
if result.stderr:
    print("\nSalida de Pruebas (stderr):")
    print(result.stderr)

# Si los tests fallaron (returncode != 0), mostramos una advertencia.
if result.returncode != 0:
    print(f"\n⚠️  ADVERTENCIA: Los tests fallaron (código de salida: {result.returncode}).")
    print("Se generará un reporte de cobertura parcial.")
else:
    print("\nPruebas ejecutadas y datos de cobertura recolectados. ✅")


# --- 2. Generar el Reporte (esto se ejecuta siempre) ---
print("\nGenerando reporte...")

try:
    report_command = [
        sys.executable, "-m", "coverage", "report",
        "--format=text",
        "--omit=*/__init__.py"  # Omitir archivos __init__.py
    ]
    
    report_result = subprocess.run(
        report_command, 
        capture_output=True, 
        text=True, 
        check=True,
        encoding='latin-1'
    )

    report_content = report_result.stdout

    # Guardar el reporte en un archivo
    with open(report_file, "w", encoding='latin-1') as f:
        f.write(report_content)
    print(f"Reporte guardado exitosamente en: '{report_file}' ✅")

    print("\n--- Proceso finalizado ---")
    print("\nContenido del Reporte:")
    print(report_content)

except subprocess.CalledProcessError as e:
    print(f"\n❌ ERROR: Falló la generación del reporte de coverage.")
    print("Esto puede pasar si 'coverage' no encontró datos (.coverage).")
    print(f"Error: {e.stderr}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")