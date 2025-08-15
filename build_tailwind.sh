#!/bin/bash

# Instalar dependencias de Node.js
npm install

# Compilar Tailwind CSS
npm run build-css

# Asegurar que el directorio estático existe
mkdir -p static
