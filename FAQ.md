# ❓ Preguntas Frecuentes (FAQ)

## General

### ¿Qué es GlintPay?
Es una aplicación educativa que simula pagos bancarios con tecnología NFC. Detecta cuando cierras la tapa del laptop para simular la lectura de una tarjeta inalámbrica.

### ¿Es seguro?
Sí, es completamente seguro. No realiza transacciones reales, no se conecta a internet, y no accede a información bancaria real.

### ¿Para qué edad es apropiado?
Es ideal para niños de 6 años en adelante, con supervisión de un adulto.

## Instalación y Configuración

### ¿Qué necesito para ejecutar la aplicación?
- Windows 7, 8, 10, o 11
- Python 3.6 o superior
- PyQt5 (`pip install PyQt5`)
- Un laptop con tapa (no funciona en desktops)

### ¿Por qué debo cambiar la configuración de energía?
Para que la aplicación pueda detectar el cierre de tapa ANTES de que Windows suspenda el sistema. Con la configuración en "No hacer nada", Windows envía el evento pero no suspende, permitiendo que la aplicación lo intercepte.

### ¿Es permanente el cambio de configuración?
No, puedes restaurar la configuración original cuando termines de usar la aplicación.

### ¿Afecta la batería?
Sí, con la configuración en "No hacer nada", cerrar la tapa no ahorra batería. Por eso se recomienda restaurar la configuración después de usar la aplicación.

## Uso de la Aplicación

### ¿Cómo sé si está funcionando?
Ejecuta `python diagnostico.py` y cierra la tapa. Si ves mensajes como "🔒 EVENTO: Sistema intentando suspender", funciona correctamente.

### La pantalla se apaga al cerrar la tapa
Verifica que:
1. La configuración de Windows esté en "No hacer nada"
2. Hayas seleccionado "Tarjeta Inalámbrica" en la aplicación
3. El monitor de energía esté iniciado (mensaje: "✅ Monitor de energía iniciado correctamente")

### No detecta el cierre de tapa
Posibles causas:
1. La configuración de Windows no está correcta
2. No estás en modo "Tarjeta Inalámbrica"
3. El monitor de energía no se inició correctamente
4. Hay políticas de grupo que fuerzan la suspensión

Solución: Ejecuta `diagnostico.py` para verificar.

### ¿Necesito abrir la tapa después de cerrarla?
No, la aplicación detecta el INTENTO de suspensión cuando cierras la tapa. No necesitas abrirla de nuevo, los datos se autocomple tan inmediatamente.

### ¿Puedo usar la aplicación sin cerrar la tapa?
Sí, usa el modo "Tarjeta Física" donde ingresas todos los datos manualmente.

## Modo Inalámbrico (NFC)

### ¿Qué es NFC?
Near Field Communication (Comunicación de Campo Cercano) es una tecnología que permite la comunicación inalámbrica de corto alcance entre dispositivos.

### ¿La aplicación usa NFC real?
No, simula la tecnología NFC usando el evento de cierre de tapa del laptop como trigger.

### ¿Por qué los datos se autocomple tan?
Para simular que la tarjeta fue "leída" cuando cerraste la tapa. En la vida real, acercar una tarjeta NFC a un lector hace lo mismo.

### ¿Puedo cambiar los datos que se autocomple tan?
Sí, puedes modificar el código en `glintpay.py`, línea ~370 aproximadamente, en el método `on_card_read_success()`.

## Modo Físico

### ¿Qué es el modo físico?
Es el modo tradicional donde ingresas todos los datos manualmente: PIN, cédula, tipo de cuenta, y monto.

### ¿Cuándo usar el modo físico?
- Cuando no quieres cambiar la configuración de Windows
- Para enseñar el proceso completo de ingreso de datos
- Si tienes problemas con la detección de suspensión

## Técnico

### ¿Cómo funciona la detección?
La aplicación crea un thread que monitorea eventos de Windows (`WM_POWERBROADCAST`). Cuando cierras la tapa, Windows envía `PBT_APMSUSPEND`, la aplicación lo intercepta y bloquea la suspensión usando `SetThreadExecutionState`.

### ¿Por qué usa un thread separado?
Para no bloquear la interfaz gráfica mientras espera eventos de Windows.

### ¿Qué es `SetThreadExecutionState`?
Es una función de la API de Windows que permite a las aplicaciones indicar que el sistema debe permanecer despierto.

### ¿Qué es `BROADCAST_QUERY_DENY`?
Es un valor que se devuelve para indicar a Windows que NO debe proceder con la suspensión.

### ¿Funciona en macOS o Linux?
No, usa APIs específicas de Windows. Para otros sistemas operativos se necesitaría una implementación diferente.

## Educativo

### ¿Qué aprenden los niños?
- Cómo funcionan los pagos contactless
- Tecnología NFC de forma visual
- Seguridad en transacciones bancarias
- Conceptos básicos de eventos del sistema

### ¿Cómo explicar NFC a un niño?
"Es como magia, pero es tecnología. Cuando acercas tu tarjeta al lector, hablan entre ellos muy rápido y sin cables. En esta aplicación, cerrar la tapa es como acercar la tarjeta."

### ¿Es realista la simulación?
Sí, simula el flujo real de un pago con tarjeta NFC:
1. Seleccionar método de pago
2. Acercar tarjeta (cerrar tapa)
3. Lectura automática de datos
4. Ingresar monto
5. Confirmar transacción

## Problemas Comunes

### Error: "module 'ctypes.wintypes' has no attribute 'WNDCLASS'"
Este error ya está corregido en la versión actual. Asegúrate de tener la última versión del código.

### Error: "argument 11: OverflowError: int too long to convert"
Este error ya está corregido. Asegúrate de usar `0` en lugar de `None` para los parámetros NULL.

### La aplicación se cierra inmediatamente
Verifica que:
1. PyQt5 esté instalado: `pip install PyQt5`
2. Estés ejecutando con Python 3.6+
3. No haya errores en la consola

### No veo mensajes en la consola
Asegúrate de ejecutar desde la terminal/cmd, no haciendo doble clic en el archivo.

### El monitor de energía no se inicia
Ejecuta como administrador:
```bash
python glintpay.py
```
Click derecho → "Ejecutar como administrador"

## Restaurar Configuración

### ¿Cómo restauro la configuración de Windows?
1. Panel de Control → Opciones de energía
2. Cambiar configuración del plan
3. "Al cerrar la tapa" → **"Suspender"**
4. Guardar cambios

### ¿Puedo automatizar la restauración?
Sí, ejecuta en PowerShell (como administrador):
```powershell
powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 1
powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 1
powercfg /setactive SCHEME_CURRENT
```

## Soporte

### ¿Dónde encuentro más información?
- `README.md` - Guía rápida
- `INICIO_RAPIDO.md` - Pasos para empezar
- `CONFIGURACION.md` - Configuración detallada
- `TECNICO.md` - Documentación técnica
- `INSTRUCCIONES.md` - Manual completo

### ¿Cómo reporto un problema?
Revisa primero:
1. Los mensajes en la consola
2. La configuración de Windows
3. Ejecuta `diagnostico.py`
4. Lee esta FAQ

### ¿Puedo modificar el código?
Sí, el código es abierto y puedes modificarlo para tus necesidades educativas.

## Consejos

### Para Padres/Educadores
- Supervisa siempre el uso con niños
- Explica que es una simulación, no es real
- Usa el modo físico primero para enseñar el proceso completo
- Luego usa el modo inalámbrico para mostrar la "magia" de NFC

### Para Desarrolladores
- Lee `TECNICO.md` para entender la arquitectura
- El código está bien comentado
- Puedes extender la funcionalidad fácilmente
- Considera agregar más mensajes de transacción

### Para Usuarios
- Ejecuta `diagnostico.py` primero para verificar
- Lee los mensajes en la consola, son informativos
- No dejes el laptop cerrado mucho tiempo
- Restaura la configuración después de usar

## Contacto

Si tienes más preguntas que no están aquí, revisa la documentación técnica o los comentarios en el código.

¡Disfruta enseñando sobre tecnología NFC! 🎓
