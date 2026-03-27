# GlintPay - Simulador Bancario con Detección Real de Suspensión

## 🚀 Características Principales

### 1. Selección de Tipo de Tarjeta
Al iniciar la aplicación, verás dos opciones:

#### 🔲 Tarjeta Física (Modo Manual)
- Ingreso manual de todos los datos
- PIN (4 dígitos)
- Cédula de identidad
- Tipo de cuenta
- Monto a transferir

#### 📡 Tarjeta Inalámbrica (Modo NFC)
- **IMPORTANTE**: Este modo espera un evento REAL de suspensión del sistema
- Al seleccionar esta opción, la aplicación muestra "Esperando Tarjeta"
- **Debes cerrar la tapa del laptop** para simular la lectura NFC
- Cuando cierres la tapa, el sistema entra en suspensión
- Al abrir la tapa nuevamente, la aplicación detecta el evento y:
  - ✅ Autocompleta los datos (cédula, tipo de cuenta, PIN)
  - Te lleva directamente a la pantalla de monto
- Si cancelas o hay un error, vuelve a la selección inicial

### 2. Detección REAL de Suspensión del Sistema
La aplicación utiliza eventos nativos de Windows para detectar:
- **PBT_APMSUSPEND**: Cuando cierras la tapa del laptop
- **PBT_APMRESUMESUSPEND**: Cuando abres la tapa del laptop

**NO es una simulación**, es un evento real del sistema operativo.

### 3. Flujo de Trabajo - Modo Inalámbrico

```
1. Seleccionar "Tarjeta Inalámbrica"
   ↓
2. Pantalla muestra: "Esperando Tarjeta" 📡
   ↓
3. Cerrar la tapa del laptop (suspensión real)
   ↓
4. Abrir la tapa del laptop (reanudación)
   ↓
5. ✅ Datos autocompletados
   ↓
6. Ingresar monto
   ↓
7. Procesar transacción
```

### 4. Mensajes de Transacción (15 tipos)

#### Éxito ✅
- TRANSACCIÓN EXITOSA
- PAGO CONFIRMADO
- OPERACIÓN APROBADA

#### Error ❌
- TRANSACCIÓN FALLIDA
- PIN INVÁLIDO
- CÉDULA INVÁLIDA
- ERROR DE CONEXIÓN
- DATOS INCORRECTOS
- LÍMITE EXCEDIDO
- ACCESO DENEGADO

#### Advertencia ⚠️
- FONDOS INSUFICIENTES
- CUENTA SUSPENDIDA
- SESIÓN EXPIRADA

#### Bloqueo 🔒
- TARJETA BLOQUEADA

#### Pendiente ⏳
- TRANSACCIÓN PENDIENTE

## 📋 Requisitos
```bash
pip install PyQt5
```

## ▶️ Cómo Ejecutar
```bash
python glintpay.py
```

## 🎮 Instrucciones de Uso

### Para Niños (Modo Inalámbrico):
1. Abre la aplicación
2. Haz clic en "Tarjeta Inalámbrica" (el botón con la señal 📡)
3. Verás un mensaje que dice "Esperando Tarjeta"
4. **Cierra la tapa de tu laptop** (como si fueras a guardarla)
5. **Abre la tapa de nuevo**
6. ¡Mágicamente los datos aparecen! ✨
7. Solo escribe cuánto dinero quieres enviar
8. Presiona "Siguiente" y listo

### Para Adultos (Modo Físico):
1. Selecciona "Tarjeta Física"
2. Ingresa PIN de 4 dígitos
3. Ingresa cédula
4. Selecciona tipo de cuenta
5. Ingresa monto
6. Procesa la transacción

## 🔧 Detalles Técnicos

### Eventos de Windows Detectados:
- `WM_POWERBROADCAST`: Mensaje de energía de Windows
- `PBT_APMSUSPEND (0x0004)`: Sistema entrando en suspensión
- `PBT_APMRESUMESUSPEND (0x0007)`: Sistema reanudando

### Implementación:
```python
class PowerEventFilter(QAbstractNativeEventFilter):
    """Filtro para detectar eventos de suspensión/reanudación"""
    def nativeEventFilter(self, eventType, message):
        # Detecta eventos nativos de Windows
        # No es simulación, es detección real
```

## ⚠️ Notas Importantes

1. **Solo funciona en Windows**: Los eventos de suspensión son específicos de Windows
2. **Requiere cerrar la tapa**: No funciona con minimizar o cerrar la ventana
3. **Modo educativo**: Perfecto para enseñar a niños sobre pagos contactless
4. **Seguro**: No realiza transacciones reales, es solo una simulación visual

## 🎨 Características Visuales
- Interfaz oscura moderna (GitHub Dark Theme)
- Animaciones suaves en modo de espera
- Iconos SVG personalizados
- Mensajes con colores según tipo
- Indicador animado mientras espera la tarjeta

## 📊 Datos de Prueba
- Saldo inicial: 1000.00 BsF
- IVA: 16%
- PIN autocompletado: 1234
- Cédula: Generada aleatoriamente (10000000-30000000)
- Tipo de cuenta: Cuenta Ahorro

## 🐛 Solución de Problemas

### La aplicación no detecta la suspensión:
- Asegúrate de estar en Windows
- Verifica que estés en modo "Tarjeta Inalámbrica"
- Cierra completamente la tapa (no solo minimices)
- Espera 1-2 segundos antes de abrir

### El botón "Cancelar" no aparece:
- Es normal, aparece solo en modo de espera NFC

### Los datos no se autocompletan:
- Verifica que hayas cerrado y abierto la tapa
- Revisa la consola para ver los mensajes de debug

## 🎓 Uso Educativo

Esta aplicación es ideal para:
- Enseñar a niños sobre pagos contactless
- Demostrar tecnología NFC de forma visual
- Explicar eventos del sistema operativo
- Práctica de interfaces de pago seguras
