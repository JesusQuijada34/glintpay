# Configuración de Windows para GlintPay

## ⚙️ Configuración Requerida

Para que la aplicación funcione correctamente, debes configurar Windows para que NO suspenda el sistema al cerrar la tapa.

### Paso 1: Abrir Opciones de Energía

1. Presiona `Windows + R`
2. Escribe: `powercfg.cpl`
3. Presiona Enter

O también:
1. Panel de Control
2. Hardware y sonido
3. Opciones de energía

### Paso 2: Cambiar Configuración del Plan

1. Busca tu plan de energía activo (tiene un punto seleccionado)
2. Haz clic en "Cambiar la configuración del plan"

### Paso 3: Configurar Acción al Cerrar la Tapa

1. Busca la opción "Al cerrar la tapa:"
2. Cambia ambas opciones (Con batería y Conectado) a: **"No hacer nada"**
3. Haz clic en "Guardar cambios"

```
┌─────────────────────────────────────────────┐
│ Al cerrar la tapa:                          │
│                                             │
│ Con batería:    [No hacer nada ▼]          │
│ Conectado:      [No hacer nada ▼]          │
└─────────────────────────────────────────────┘
```

## 🎯 ¿Por Qué Esta Configuración?

La aplicación necesita interceptar el evento de cierre de tapa ANTES de que Windows suspenda el sistema. Con esta configuración:

1. Windows detecta que cerraste la tapa
2. Envía un mensaje `WM_POWERBROADCAST` con `PBT_APMSUSPEND`
3. La aplicación intercepta este mensaje
4. La aplicación BLOQUEA la suspensión usando `SetThreadExecutionState`
5. La pantalla permanece encendida
6. La aplicación simula la lectura NFC
7. Los datos se autocomple tan

## 🔍 Verificar Configuración

Para verificar que la configuración está correcta:

1. Cierra la tapa del laptop
2. La pantalla debe permanecer encendida
3. El sistema NO debe entrar en suspensión
4. Puedes abrir la tapa y seguir trabajando normalmente

## 🔄 Restaurar Configuración Original

Después de usar la aplicación, puedes restaurar la configuración:

1. Ve a Opciones de energía
2. Cambia "Al cerrar la tapa" a: **"Suspender"** (valor por defecto)
3. Guarda los cambios

## 🛡️ Seguridad

Esta configuración es segura porque:
- Solo afecta cuando la aplicación está ejecutándose
- La aplicación usa `SetThreadExecutionState` para mantener el sistema despierto
- Cuando cierras la aplicación, el sistema vuelve a su comportamiento normal
- No modifica permanentemente la configuración de energía

## 📱 Configuración Alternativa (Avanzada)

Si no quieres cambiar la configuración global, puedes usar PowerShell:

```powershell
# Ejecutar ANTES de abrir la aplicación
powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 0
powercfg /setactive SCHEME_CURRENT

# Ejecutar DESPUÉS de cerrar la aplicación (restaurar)
powercfg /setacvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 1
powercfg /setdcvalueindex SCHEME_CURRENT SUB_BUTTONS LIDACTION 1
powercfg /setactive SCHEME_CURRENT
```

Donde:
- `0` = No hacer nada
- `1` = Suspender
- `2` = Hibernar
- `3` = Apagar

## 🎮 Uso con Niños

Para uso educativo con niños:

1. Configura Windows una sola vez (No hacer nada al cerrar tapa)
2. Ejecuta la aplicación
3. Los niños pueden cerrar la tapa y ver la "magia" de la lectura NFC
4. La pantalla permanece encendida para que vean el proceso
5. Cuando terminen, restaura la configuración

## ⚠️ Notas Importantes

1. **Batería**: Con esta configuración, cerrar la tapa NO ahorra batería
2. **Temporal**: Solo usa esta configuración mientras usas la aplicación
3. **Supervisión**: Supervisa a los niños para que no dejen el laptop cerrado mucho tiempo
4. **Ventilación**: Asegúrate de que el laptop tenga buena ventilación

## 🔧 Troubleshooting

### La pantalla se apaga al cerrar la tapa
**Solución**: Verifica que la configuración esté en "No hacer nada"

### El sistema entra en suspensión
**Solución**: 
1. Verifica la configuración de energía
2. Ejecuta la aplicación como administrador
3. Verifica que no haya políticas de grupo que fuercen la suspensión

### La aplicación no detecta el cierre de tapa
**Solución**:
1. Verifica que estés en modo "Tarjeta Inalámbrica"
2. Revisa la consola para ver mensajes de debug
3. Asegúrate de que el monitor de energía esté iniciado (mensaje: "✅ Monitor de energía iniciado")

## 📞 Soporte

Si tienes problemas:
1. Revisa los mensajes en la consola
2. Verifica la configuración de energía de Windows
3. Ejecuta como administrador si es necesario
4. Revisa el archivo TECNICO.md para más detalles
