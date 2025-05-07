#!/usr/bin/env python3

import os
import sys
import logging
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

logger = logging.getLogger("init_db")

def main():
    """Inicializa la base de datos con datos iniciales."""
    logger.info("Iniciando la configuración de la base de datos...")
    
    # Cargar configuración
    config = load_config()
    
    # Inicializar contenedor de dependencias
    container = DIContainer(config)
    container.initialize()
    
    # Poblar la base de datos
    logger.info("Poblando la base de datos con datos iniciales...")
    container.seed_database()
    
    logger.info("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    main()
