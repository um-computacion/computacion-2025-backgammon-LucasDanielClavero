import subprocess
import os
import sys

# --- Configuración ---
SOURCE_DIRS = "core,cli"
TEST_DIR = "tests"
OUTPUT_FILENAME = "coverage_report.txt"

def main():
    """
    Función principal para ejecutar coverage y generar el reporte,
    incluso si las pruebas fallan.
    """
    print("--- Iniciando la generación del reporte de cobertura ---")
    
    python_executable = sys.executable

    # 1. Ejecutar las pruebas con coverage para recolectar datos.
    # Se ignora si las pruebas fallan para poder generar un reporte parcial.
    run_command = [
        python_executable, "-m", "coverage", "run",
        f"--source={SOURCE_DIRS}",
        "-m", "unittest", "discover",
        "-s", TEST_DIR
    ]
    
    print(f"Ejecutando comando: {' '.join(run_command)}")
    # Ejecutamos el comando sin 'check=True' para que no se detenga si hay errores.
    result = subprocess.run(
        run_command,
        capture_output=True,
        text=True,
        encoding='latin-1'
    )

    if result.returncode != 0:
        print("\n⚠️ ADVERTENCIA: Una o más pruebas fallaron. El reporte de cobertura generado será parcial e impreciso.")
        print("   Se recomienda corregir los errores en las pruebas para obtener un resultado válido.")
        print("\n--- Errores de Pruebas ---")
        print(result.stderr)
        print("--------------------------\n")
    else:
        print("Pruebas ejecutadas y datos de cobertura recolectados. ✅")

    # 2. Generar el reporte de texto sin importar el resultado de las pruebas.
    report_command = [python_executable, "-m", "coverage", "report", "-m"]
    
    try:
        print("Generando reporte...")
        report_content = subprocess.run(
            report_command,
            capture_output=True,
            text=True,
            check=True, # Aquí sí se necesita que el comando funcione
            encoding='latin-1'
        ).stdout
        
        # 3. Guardar el reporte en un archivo de texto.
        with open(OUTPUT_FILENAME, "w", encoding='latin-1') as f:
            f.write(report_content)
            
        print(f"Reporte guardado exitosamente en: '{os.path.abspath(OUTPUT_FILENAME)}' 📋")
        print("\n--- Proceso finalizado ---")
        print("\nContenido del Reporte:")
        print("--------------------------------------------------")
        print(report_content)
        print("--------------------------------------------------")

    except subprocess.CalledProcessError as e:
        print("Error crítico al intentar generar el reporte de coverage.")
        print("Esto puede suceder si no se recolectó ningún dato de cobertura,")
        print("posiblemente debido a un error de configuración o a que no se encontró ninguna prueba.")
        print(e.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()