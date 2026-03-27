#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para GlintPay con detección REAL de suspensión
y prevención de apagado de pantalla
"""

import sys
from PyQt5.QtWidgets import QApplication
from glintpay import MainWindow

if __name__ == "__main__":
    print("=" * 70)
    print("GLINTPAY - Simulador Bancario con Detección Real de Suspensión")
    print("=" * 70)
    print("\n📋 INSTRUCCIONES IMPORTANTES:\n")
    
    print("🔧 CONFIGURACIÓN PREVIA:")
    print("   1. Ve a: Panel de Control → Opciones de energía")
    print("   2. Clic en 'Cambiar la configuración del plan'")
    print("   3. En 'Al cerrar la tapa': Selecciona 'No hacer nada'")
    print("   4. Guarda los cambios\n")
    
    print("1️⃣  MODO TARJETA FÍSICA:")
    print("   - Selecciona 'Tarjeta Física'")
    print("   - Ingresa todos los datos manualmente\n")
    
    print("2️⃣  MODO TARJETA INALÁMBRICA (NFC):")
    print("   - Selecciona 'Tarjeta Inalámbrica'")
    print("   - Verás 'Esperando Tarjeta' 📡")
    print("   - 🔒 CIERRA LA TAPA DE TU LAPTOP")
    print("   - ⚡ La pantalla NO se apagará (bloqueado por la app)")
    print("   - ✅ Los datos se autocompletarán inmediatamente")
    print("   - Solo ingresa el monto\n")
    
    print("⚠️  IMPORTANTE:")
    print("   - La app BLOQUEA la suspensión del sistema")
    print("   - La pantalla permanece encendida")
    print("   - Detecta el INTENTO de suspensión (cierre de tapa)")
    print("   - NO necesitas abrir la tapa de nuevo\n")
    
    print("🔍 MENSAJES DE DEBUG EN CONSOLA:")
    print("   - ✅ Monitor de energía iniciado")
    print("   - 📡 Modo NFC activado")
    print("   - 🔒 Evento de suspensión detectado")
    print("   - ⛔ BLOQUEANDO suspensión del sistema")
    print("   - 📡 Leyendo tarjeta NFC...")
    print("   - ✅ Tarjeta detectada - Procesando datos\n")
    
    print("🎯 FLUJO ESPERADO:")
    print("   1. Seleccionar 'Tarjeta Inalámbrica'")
    print("   2. Cerrar tapa del laptop")
    print("   3. Ver mensaje en consola: '🔒 Evento de suspensión detectado'")
    print("   4. Ver mensaje: '⛔ BLOQUEANDO suspensión del sistema'")
    print("   5. Pantalla permanece encendida")
    print("   6. Datos se autocomple tan")
    print("   7. Continuar con el monto\n")
    
    print("=" * 70)
    print("Iniciando aplicación...\n")
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
