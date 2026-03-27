# 🚀 Inicio Rápido - GlintPay

## Paso 1: Configurar Windows (Solo una vez)

1. Presiona `Windows + R`
2. Escribe: `powercfg.cpl`
3. Presiona Enter
4. Clic en "Cambiar la configuración del plan"
5. En "Al cerrar la tapa": Cambia a **"No hacer nada"** (ambas opciones)
6. Clic en "Guardar cambios"

## Paso 2: Verificar que Funciona

Ejecuta el script de diagnóstico:

```bash
python diagnostico.py
```

Luego:
1. Cierra la tapa de tu laptop
2. Deberías ver en la consola:
   ```
   🔒 EVENTO: Sistema intentando suspender
   ⛔ BLOQUEANDO suspensión del sistema
   ✅ Sistema configurado para mantenerse despierto
   ```
3. Si ves estos mensajes, ¡funciona correctamente!
4. Presiona `Ctrl+C` para salir

## Paso 3: Usar la Aplicación

```bash
python glintpay.py
```

### Para Modo Inalámbrico (NFC):
1. Clic en "Tarjeta Inalámbrica" 📡
2. Cierra la tapa del laptop 🔒
3. Los datos se autocomple tan ✅
4. Ingresa el monto
5. ¡Listo!

### Para Modo Físico:
1. Clic en "Tarjeta Física" 🔲
2. Ingresa PIN, cédula, tipo de cuenta
3. Ingresa el monto
4. ¡Listo!

## ⚠️ Importante

- La pantalla NO se apagará al cerrar la tapa (esto es normal)
- Después de usar, puedes restaurar la configuración de Windows
- Supervisa a los niños durante el uso

## 🐛 Si Algo No Funciona

1. Verifica la configuración de Windows (Paso 1)
2. Ejecuta el diagnóstico (Paso 2)
3. Revisa los mensajes en la consola
4. Lee `CONFIGURACION.md` para más detalles

## 📊 Mensajes Esperados

Al ejecutar la aplicación verás:
```
🚀 GlintPay iniciado
📋 Monitor de energía activo
✅ Monitor de energía iniciado correctamente
```

Al cerrar la tapa en modo NFC verás:
```
📡 Modo NFC activado - Esperando cierre de tapa
🔒 Evento: Sistema intentando suspender
⛔ BLOQUEANDO suspensión del sistema
✅ Sistema configurado para mantenerse despierto
📡 Leyendo tarjeta NFC...
✅ Tarjeta detectada - Procesando datos
```

## ✅ Todo Listo

Si ves estos mensajes, la aplicación funciona perfectamente y está lista para usar con niños.

¡Disfruta enseñando sobre tecnología NFC! 🎓
