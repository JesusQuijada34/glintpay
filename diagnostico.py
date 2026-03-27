#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar la detección de eventos de energía
"""

import ctypes
from ctypes import wintypes, POINTER, WINFUNCTYPE, c_int, c_uint, Structure, c_wchar_p
import time

# Constantes
WM_POWERBROADCAST = 0x0218
PBT_APMSUSPEND = 0x0004
PBT_APMRESUMESUSPEND = 0x0007
BROADCAST_QUERY_DENY = 0x424D5144

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

# Estructura WNDCLASS
class WNDCLASS(Structure):
    _fields_ = [
        ('style', c_uint),
        ('lpfnWndProc', WINFUNCTYPE(c_int, wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM)),
        ('cbClsExtra', c_int),
        ('cbWndExtra', c_int),
        ('hInstance', wintypes.HINSTANCE),
        ('hIcon', wintypes.HICON),
        ('hCursor', wintypes.HANDLE),
        ('hbrBackground', wintypes.HBRUSH),
        ('lpszMenuName', c_wchar_p),
        ('lpszClassName', c_wchar_p)
    ]

# APIs
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

SetThreadExecutionState = kernel32.SetThreadExecutionState
SetThreadExecutionState.argtypes = [wintypes.DWORD]
SetThreadExecutionState.restype = wintypes.DWORD

RegisterClassW = user32.RegisterClassW
RegisterClassW.argtypes = [POINTER(WNDCLASS)]
RegisterClassW.restype = wintypes.ATOM

CreateWindowExW = user32.CreateWindowExW
CreateWindowExW.argtypes = [
    wintypes.DWORD,      # dwExStyle
    wintypes.LPCWSTR,    # lpClassName
    wintypes.LPCWSTR,    # lpWindowName
    wintypes.DWORD,      # dwStyle
    c_int,               # x
    c_int,               # y
    c_int,               # nWidth
    c_int,               # nHeight
    wintypes.HWND,       # hWndParent
    wintypes.HMENU,      # hMenu
    wintypes.HINSTANCE,  # hInstance
    wintypes.LPVOID      # lpParam
]
CreateWindowExW.restype = wintypes.HWND

GetMessageW = user32.GetMessageW
GetMessageW.argtypes = [POINTER(wintypes.MSG), wintypes.HWND, c_uint, c_uint]
GetMessageW.restype = wintypes.BOOL

TranslateMessage = user32.TranslateMessage
TranslateMessage.argtypes = [POINTER(wintypes.MSG)]
TranslateMessage.restype = wintypes.BOOL

DispatchMessageW = user32.DispatchMessageW
DispatchMessageW.argtypes = [POINTER(wintypes.MSG)]
DispatchMessageW.restype = wintypes.LPARAM

DefWindowProcW = user32.DefWindowProcW
DefWindowProcW.argtypes = [wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM]
DefWindowProcW.restype = wintypes.LPARAM

GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
GetModuleHandleW.restype = wintypes.HMODULE

# Variables globales
prevent_sleep = True
event_count = 0

def wnd_proc(hwnd, msg, wparam, lparam):
    """Procesar mensajes de Windows"""
    global event_count
    
    if msg == WM_POWERBROADCAST:
        event_count += 1
        
        if wparam == PBT_APMSUSPEND:
            print(f"\n{'='*60}")
            print(f"🔒 EVENTO #{event_count}: Sistema intentando suspender")
            print(f"{'='*60}")
            
            if prevent_sleep:
                print("⛔ BLOQUEANDO suspensión del sistema")
                result = SetThreadExecutionState(
                    ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
                )
                if result:
                    print("✅ Sistema configurado para mantenerse despierto")
                    print("📺 Pantalla permanecerá encendida")
                else:
                    print("❌ Error al configurar estado de ejecución")
                
                print(f"{'='*60}\n")
                return BROADCAST_QUERY_DENY
                
        elif wparam == PBT_APMRESUMESUSPEND:
            print(f"\n{'='*60}")
            print(f"🔓 EVENTO #{event_count}: Sistema reanudando")
            print(f"{'='*60}\n")
    
    return DefWindowProcW(hwnd, msg, wparam, lparam)

def main():
    print("=" * 70)
    print("DIAGNÓSTICO DE DETECCIÓN DE EVENTOS DE ENERGÍA")
    print("=" * 70)
    print("\n📋 Este script verifica que la detección de eventos funcione\n")
    
    print("🔧 Configurando monitor de energía...")
    
    # Crear clase de ventana
    wndclass = WNDCLASS()
    wndclass.lpfnWndProc = WINFUNCTYPE(c_int, wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM)(wnd_proc)
    wndclass.lpszClassName = "DiagnosticClass"
    wndclass.hInstance = GetModuleHandleW(None)
    
    atom = RegisterClassW(ctypes.byref(wndclass))
    if not atom:
        print("❌ Error al registrar clase de ventana")
        return
    
    print("✅ Clase de ventana registrada")
    
    # Crear ventana
    hwnd = CreateWindowExW(
        0,
        "DiagnosticClass",
        "Diagnostic",
        0,
        0, 0, 0, 0,
        0, 0,
        wndclass.hInstance,
        0
    )
    
    if not hwnd:
        print("❌ Error al crear ventana")
        return
    
    print("✅ Ventana creada")
    print("✅ Monitor de energía activo\n")
    
    print("=" * 70)
    print("INSTRUCCIONES:")
    print("=" * 70)
    print("1. Asegúrate de que Windows esté configurado:")
    print("   Opciones de energía → Al cerrar la tapa → 'No hacer nada'")
    print("\n2. CIERRA LA TAPA DE TU LAPTOP")
    print("\n3. Observa los mensajes en esta consola")
    print("\n4. Si ves '🔒 EVENTO: Sistema intentando suspender'")
    print("   significa que la detección funciona correctamente")
    print("\n5. La pantalla NO debe apagarse")
    print("\n6. Presiona Ctrl+C para salir")
    print("=" * 70)
    print("\n⏳ Esperando eventos de energía...\n")
    
    # Loop de mensajes
    msg = wintypes.MSG()
    try:
        while True:
            result = GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result == 0 or result == -1:
                break
            TranslateMessage(ctypes.byref(msg))
            DispatchMessageW(ctypes.byref(msg))
    except KeyboardInterrupt:
        print("\n\n👋 Diagnóstico finalizado")
        print(f"📊 Total de eventos detectados: {event_count}")
        
        # Restaurar comportamiento normal
        SetThreadExecutionState(ES_CONTINUOUS)
        print("✅ Sistema restaurado a comportamiento normal")

if __name__ == "__main__":
    main()
