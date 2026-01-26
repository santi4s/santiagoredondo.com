#!/bin/bash

# Script para reorganizar el proyecto consolas-retro

echo "🔨 Reorganizando estructura del proyecto..."

# Crear nuevas carpetas
mkdir -p scraper
mkdir -p data
mkdir -p web/consoles
mkdir -p .github/workflows

# Mover carpetas de consolas a web/consoles/
echo "📁 Moviendo carpetas de consolas..."
for console in gameboy-color gameboy mastersystem-2 mastersystem megadrive-2 megadrive nes snes; do
    if [ -d "$console" ]; then
        mv "$console" web/consoles/
        echo "  ✓ Movido $console"
    fi
done

# Mover archivos principales a web/
echo "📄 Moviendo archivos principales..."
if [ -f "index.html" ]; then
    mv index.html web/
    echo "  ✓ Movido index.html"
fi

if [ -f "CNAME" ]; then
    # CNAME se queda en la raíz para GitHub Pages
    echo "  ✓ CNAME permanece en raíz"
fi

if [ -f "README.md" ]; then
    echo "  ✓ README.md permanece en raíz"
fi

echo ""
echo "✅ Reorganización completada!"
echo ""
echo "Estructura actual:"
tree -L 2 -I 'node_modules'

