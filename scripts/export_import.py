#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from pathlib import Path

# Añadir el directorio padre al PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import load_config
from config.di_container import DIContainer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("export_import")

def export_data(container: DIContainer, file_path: str, data_type: str = "all") -> None:
    """
    Exporta datos a un archivo JSON.
    
    Args:
        container: Contenedor de inyección de dependencias
        file_path: Ruta donde guardar el archivo JSON
        data_type: Tipo de datos a exportar ("all", "inventory", "events")
    """
    logger.info(f"Exportando datos tipo '{data_type}' a {file_path}...")
    
    if data_type == "all":
        container.data_exporter.export_all_data(file_path)
    elif data_type == "inventory":
        container.data_exporter.export_inventory(file_path)
    elif data_type == "events":
        container.data_exporter.export_events(file_path)
    else:
        logger.error(f"Tipo de datos '{data_type}' no reconocido")
        return
    
    logger.info(f"Datos exportados correctamente a {file_path}")

def import_data(container: DIContainer, file_path: str) -> None:
    """
    Importa datos desde un archivo JSON.
    
    Args:
        container: Contenedor de inyección de dependencias
        file_path: Ruta del archivo JSON a importar
    """
    logger.info(f"Importando datos desde {file_path}...")
    
    container.data_importer.import_all_data(file_path)
    
    logger.info("Datos importados correctamente")

def main():
    """Función principal para exportar/importar datos."""
    parser = argparse.ArgumentParser(description="Exportar/Importar datos del simulador")
    
    # Grupo de argumentos mutuamente excluyentes
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--export", action="store_true", help="Exportar datos")
    group.add_argument("--import", dest="import_data", action="store_true", help="Importar datos")
    
    # Argumentos comunes
    parser.add_argument(
        "--file", "-f", type=str, required=True,
        help="Ruta del archivo JSON para exportar/importar"
    )
    
    # Argumentos específicos para exportar
    parser.add_argument(
        "--type", "-t", type=str, choices=["all", "inventory", "events"],
        default="all", help="Tipo de datos a exportar (solo para --export)"
    )
    
    args = parser.parse_args()
    
    # Cargar configuración
    config = load_config()
    
    # Inicializar contenedor de dependencias
    container = DIContainer(config)
    container.initialize()
    
    if args.export:
        export_data(container, args.file, args.type)
    elif args.import_data:
        import_data(container, args.file)

if __name__ == "__main__":
    main()
