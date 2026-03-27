# Documentación Técnica - GlintPay

## Arquitectura de Detección de Suspensión

### Eventos de Windows

La aplicación utiliza la API nativa de Windows para detectar eventos de energía:

```python
# Constantes de Windows
WM_POWERBROADCAST = 0x0218      # Mensaje de broadcast de energía
PBT_APMSUSPEND = 0x0004         # Sistema entrando en suspensión
PBT_APMRESUMESUSPEND = 0x0007   # Sistema reanudando desde suspensión
```

### Filtro de Eventos Nativos

```python
class PowerEventFilter(QAbstractNativeEventFilter):
    """
    Filtro que intercepta mensajes nativos de Windows
    antes de que lleguen a la cola de eventos de Qt
    """
    def nativeEventFilter(self, eventType, message):
        # Convierte el mensaje a estructura MSG de Windows
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        
        # Verifica si es un mensaje de energía
        if msg.message == WM_POWERBROADCAST:
            if msg.wParam == PBT_APMSUSPEND:
                # Tapa cerrada
                self.callback_suspend()
            elif msg.wParam == PBT_APMRESUMESUSPEND:
                # Tapa abierta
                self.callback_resume()
        
        return False, 0  # No consumir el evento
```

## Flujo de Datos - Modo Inalámbrico

### 1. Selección de Modo
```
Usuario → CardTypeStep.select_mode("wireless")
    ↓
wizard.waiting_for_nfc = True
    ↓
CardTypeStep.show_waiting_screen()
```

### 2. Espera de Evento
```
Usuario cierra tapa
    ↓
Windows genera WM_POWERBROADCAST + PBT_APMSUSPEND
    ↓
PowerEventFilter.nativeEventFilter() detecta
    ↓
MainWindow.on_system_suspend() llamado
    ↓
[Sistema en suspensión]
```

### 3. Reanudación y Lectura
```
Usuario abre tapa
    ↓
Windows genera WM_POWERBROADCAST + PBT_APMRESUMESUSPEND
    ↓
PowerEventFilter.nativeEventFilter() detecta
    ↓
MainWindow.on_system_resume() llamado
    ↓
Verifica: waiting_for_nfc == True
    ↓
CardTypeStep.on_card_read_success()
    ↓
Autocompleta datos
    ↓
Navega a AmountStep
```

## Estructura de Clases

```
QApplication
    └── MainWindow (QWidget)
        ├── PowerEventFilter (QAbstractNativeEventFilter)
        ├── CustomTitleBar
        ├── StepperWidget
        └── QStackedWidget
            ├── CardTypeStep (WizardStep)
            │   ├── Modo Physical
            │   └── Modo Wireless (espera suspensión)
            ├── LoginStep (WizardStep)
            ├── InfoStep (WizardStep)
            ├── AmountStep (WizardStep)
            ├── ProcessingStep (WizardStep)
            └── ResultStep (WizardStep)
```

## Estados de la Aplicación

### Estado: Esperando NFC
```python
wizard.waiting_for_nfc = True
CardTypeStep.waiting_for_card = True
```

**Condiciones:**
- Usuario seleccionó "Tarjeta Inalámbrica"
- Pantalla muestra "Esperando Tarjeta"
- Animación activa (📡 ↔ 📶)

**Transiciones:**
- Suspensión detectada → Mantiene estado
- Reanudación detectada → Lectura exitosa
- Botón cancelar → Vuelve a selección

### Estado: Lectura Exitosa
```python
wizard.waiting_for_nfc = False
CardTypeStep.waiting_for_card = False
```

**Acciones:**
- Genera datos aleatorios
- Muestra ✅
- Navega a AmountStep después de 1 segundo

### Estado: Error de Lectura
```python
CardTypeStep.on_card_read_error()
```

**Acciones:**
- Muestra ❌
- Cambia subtítulo a error
- Vuelve a selección después de 2 segundos

## Seguridad y Validaciones

### Prevención de Cierre Accidental
- El botón de cerrar (X) funciona normalmente
- NO se muestra ventana de verificación al cerrar
- El proceso NFC puede cancelarse en cualquier momento

### Validación de Estado
```python
if self.waiting_for_nfc and isinstance(self.stack.currentWidget(), CardTypeStep):
    # Solo procesar si estamos en la pantalla correcta
    self.steps[0].on_card_read_success()
```

## Mensajes de Debug

La aplicación imprime mensajes en consola para debugging:

```python
print("🔒 Sistema suspendido - Tapa cerrada")
print("🔓 Sistema reanudado - Tapa abierta")
print("📡 Leyendo tarjeta NFC...")
print("✅ Tarjeta NFC leída exitosamente")
```

## Compatibilidad

### Sistemas Operativos
- ✅ Windows 7, 8, 10, 11
- ❌ macOS (eventos diferentes)
- ❌ Linux (eventos diferentes)

### Hardware
- Requiere laptop con tapa
- Funciona con cualquier laptop que genere eventos de suspensión
- No requiere hardware NFC real

## Limitaciones Conocidas

1. **Solo Windows**: Los eventos `WM_POWERBROADCAST` son específicos de Windows
2. **Requiere tapa física**: No funciona con monitores externos o desktops
3. **Timing**: Puede haber un delay de 1-2 segundos en la detección
4. **Configuración de energía**: Depende de la configuración de energía del sistema

## Extensiones Futuras

### Soporte para macOS
```python
# Usar NSWorkspace notifications
NSWorkspace.shared.notificationCenter.addObserver(
    forName: NSWorkspace.willSleepNotification
)
```

### Soporte para Linux
```python
# Usar D-Bus para escuchar eventos de systemd
import dbus
bus = dbus.SystemBus()
bus.add_signal_receiver(
    handler_function,
    'PrepareForSleep',
    'org.freedesktop.login1.Manager'
)
```

### Timeout de Espera
```python
# Agregar timeout de 30 segundos
self.timeout_timer = QTimer()
self.timeout_timer.timeout.connect(self.on_timeout)
self.timeout_timer.start(30000)
```

## Testing

### Prueba Manual
1. Ejecutar `python test_suspend.py`
2. Seleccionar "Tarjeta Inalámbrica"
3. Cerrar tapa del laptop
4. Esperar 2-3 segundos
5. Abrir tapa
6. Verificar que los datos se autocompleten

### Prueba de Cancelación
1. Seleccionar "Tarjeta Inalámbrica"
2. Hacer clic en "Cancelar"
3. Verificar que vuelve a la selección inicial

### Prueba de Error
1. Modificar `on_system_resume()` para llamar `on_card_read_error()`
2. Verificar que muestra mensaje de error
3. Verificar que vuelve a la selección

## Troubleshooting

### La suspensión no se detecta
**Causa**: Configuración de energía de Windows
**Solución**: 
```
Panel de Control → Opciones de energía → 
Cambiar la configuración del plan → 
Configuración avanzada de energía →
Verificar que "Suspender" esté habilitado
```

### Los eventos se detectan múltiples veces
**Causa**: Múltiples instancias del filtro
**Solución**: Verificar que solo se instale una vez en `__init__`

### La aplicación no responde después de suspensión
**Causa**: Qt event loop bloqueado
**Solución**: Usar `QTimer.singleShot()` para operaciones asíncronas
