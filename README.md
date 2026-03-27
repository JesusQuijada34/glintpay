# GlintPay - Simulador Bancario con Detección Real de Suspensión

Aplicación educativa que simula pagos bancarios con tecnología NFC, detectando el cierre de tapa del laptop para simular la lectura de tarjeta inalámbrica.

## 🚀 Inicio Rápido

### 1. Instalar Dependencias
```bash
pip install PyQt5
```

### 2. Configurar Windows
**IMPORTANTE**: Debes configurar Windows para que NO suspenda al cerrar la tapa:

1. Abre: `Panel de Control` → `Opciones de energía`
2. Clic en `Cambiar la configuración del plan`
3. En `Al cerrar la tapa`: Selecciona **"No hacer nada"** (ambas opciones)
4. Guarda los cambios

### 3. Ejecutar la Aplicación
```bash
python glintpay.py
```

O con instrucciones:
```bash
python test_suspend.py
```

### 4. Probar la Detección (Opcional)
```bash
python diagnostico.py
```

## 🎮 Cómo Usar

### Modo Tarjeta Física
1. Selecciona "Tarjeta Física"
2. Ingresa PIN (4 dígitos)
3. Ingresa cédula
4. Selecciona tipo de cuenta
5. Ingresa monto
6. Procesa la transacción

### Modo Tarjeta Inalámbrica (NFC)
1. Selecciona "Tarjeta Inalámbrica"
2. Verás "Esperando Tarjeta" 📡
3. **Cierra la tapa del laptop** 🔒
4. La pantalla permanece encendida
5. Los datos se autocomple tan ✅
6. Ingresa el monto
7. Procesa la transacción

## 🔍 Verificar que Funciona

Ejecuta el script de diagnóstico:
```bash
python diagnostico.py
```

Luego cierra la tapa del laptop. Deberías ver:
```
🔒 EVENTO: Sistema intentando suspender
⛔ BLOQUEANDO suspensión del sistema
✅ Sistema configurado para mantenerse despierto
📺 Pantalla permanecerá encendida
```

Si ves estos mensajes, ¡todo funciona correctamente!

## 📁 Archivos

- `glintpay.py` - Aplicación principal
- `test_suspend.py` - Script de prueba con instrucciones
- `diagnostico.py` - Verificar detección de eventos
- `CONFIGURACION.md` - Guía detallada de configuración
- `INSTRUCCIONES.md` - Manual de usuario completo
- `TECNICO.md` - Documentación técnica

## ⚙️ Cómo Funciona

1. La aplicación crea un thread que monitorea eventos de Windows
2. Cuando cierras la tapa, Windows envía `WM_POWERBROADCAST` con `PBT_APMSUSPEND`
3. La aplicación intercepta este evento
4. Usa `SetThreadExecutionState` para mantener el sistema despierto
5. Devuelve `BROADCAST_QUERY_DENY` para bloquear la suspensión
6. La pantalla permanece encendida
7. Simula la lectura NFC y autocompleta los datos

## 🎓 Uso Educativo

Perfecto para enseñar a niños sobre:
- Tecnología NFC y pagos contactless
- Cómo funcionan las tarjetas inalámbricas
- Seguridad en transacciones bancarias
- Eventos del sistema operativo

## ⚠️ Notas Importantes

1. **Solo Windows**: Usa APIs específicas de Windows
2. **Configuración temporal**: Restaura la configuración de energía después de usar
3. **Supervisión**: Supervisa a los niños durante el uso
4. **No es real**: No realiza transacciones bancarias reales

## 🐛 Solución de Problemas

### La pantalla se apaga al cerrar la tapa
- Verifica la configuración de energía de Windows
- Asegúrate de que esté en "No hacer nada"

### No detecta el cierre de tapa
- Ejecuta `diagnostico.py` para verificar
- Revisa los mensajes en la consola
- Asegúrate de estar en modo "Tarjeta Inalámbrica"

### Error al iniciar
- Verifica que PyQt5 esté instalado: `pip install PyQt5`
- Ejecuta como administrador si es necesario

## 📊 Mensajes de Debug

La aplicación muestra mensajes en consola:

- `✅ Monitor de energía iniciado correctamente`
- `📡 Modo NFC activado - Esperando cierre de tapa`
- `🔒 Evento: Sistema intentando suspender`
- `⛔ BLOQUEANDO suspensión del sistema`
- `✅ Sistema configurado para mantenerse despierto`
- `📡 Leyendo tarjeta NFC...`
- `✅ Tarjeta detectada - Procesando datos`

## 🔧 Requisitos del Sistema

- Windows 7, 8, 10, o 11
- Python 3.6 o superior
- PyQt5
- Laptop con tapa (no funciona en desktops)

## 📞 Soporte

Si tienes problemas:
1. Lee `CONFIGURACION.md` para configuración detallada
2. Ejecuta `diagnostico.py` para verificar la detección
3. Revisa `TECNICO.md` para detalles técnicos
4. Verifica los mensajes en la consola

## 📝 Licencia

Este es un proyecto educativo para demostración de tecnología NFC.

## 🙏 Créditos

Desarrollado para uso educativo con niños, demostrando tecnología de pagos contactless de forma segura y visual.
