#!/usr/bin/env python
# -*- coding: utf-8 -*-
# kejq34/myapps/system/influent.shell.vIO-34-2.18-danenone.iflapp
# App: GlintPay | Banco QT5/QSS Simulado (Wizard Edition v3 - Ultra Minimalist)
# publisher: influent
# name: glintpay
# version: IO-3-25.11-Wizard-v3
# script: Python3

import sys
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QFrame, QGraphicsDropShadowEffect, QProgressBar, QDesktopWidget
)
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtCore import Qt, QPoint, QTimer, QThread, pyqtSignal
import ctypes
from ctypes import wintypes, POINTER, WINFUNCTYPE, c_int, c_uint, c_void_p, Structure, c_wchar_p

# --- WINDOWS API CONSTANTS ---
WM_POWERBROADCAST = 0x0218
PBT_APMSUSPEND = 0x0004
PBT_APMRESUMESUSPEND = 0x0007
PBT_POWERSETTINGCHANGE = 0x8013
BROADCAST_QUERY_DENY = 0x424D5144

# Constantes para mantener el sistema despierto
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040

# --- WINDOWS STRUCTURES ---
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

# --- WINDOWS API FUNCTIONS ---
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Definir SetThreadExecutionState
SetThreadExecutionState = kernel32.SetThreadExecutionState
SetThreadExecutionState.argtypes = [wintypes.DWORD]
SetThreadExecutionState.restype = wintypes.DWORD

# Definir funciones de ventana
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

PostMessageW = user32.PostMessageW
PostMessageW.argtypes = [wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM]
PostMessageW.restype = wintypes.BOOL

GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
GetModuleHandleW.restype = wintypes.HMODULE

# --- POWER MONITOR THREAD ---
class PowerMonitorThread(QThread):
    """Thread que monitorea eventos de energía de Windows"""
    suspend_detected = pyqtSignal()
    resume_detected = pyqtSignal()
    lid_closed = pyqtSignal()
    lid_opened = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.prevent_sleep = False
        self.hwnd = None
        
    def run(self):
        """Ejecutar el loop de mensajes de Windows"""
        # Crear una ventana invisible para recibir mensajes
        wndclass = WNDCLASS()
        wndclass.lpfnWndProc = WINFUNCTYPE(c_int, wintypes.HWND, c_uint, wintypes.WPARAM, wintypes.LPARAM)(self.wnd_proc)
        wndclass.lpszClassName = "PowerMonitorClass"
        wndclass.hInstance = kernel32.GetModuleHandleW(None)
        
        atom = RegisterClassW(ctypes.byref(wndclass))
        if not atom:
            print("❌ Error al registrar clase de ventana")
            return
        
        self.hwnd = CreateWindowExW(
            0,                          # dwExStyle
            "PowerMonitorClass",        # lpClassName
            "PowerMonitor",             # lpWindowName
            0,                          # dwStyle
            0, 0, 0, 0,                # x, y, width, height
            0,                          # hWndParent (NULL)
            0,                          # hMenu (NULL)
            wndclass.hInstance,         # hInstance
            0                           # lpParam (NULL)
        )
        
        if not self.hwnd:
            print("❌ Error al crear ventana")
            return
        
        print("✅ Monitor de energía iniciado correctamente")
        
        # Loop de mensajes
        msg = wintypes.MSG()
        while self.running:
            result = GetMessageW(ctypes.byref(msg), None, 0, 0)
            if result == 0 or result == -1:
                break
            TranslateMessage(ctypes.byref(msg))
            DispatchMessageW(ctypes.byref(msg))
    
    def wnd_proc(self, hwnd, msg, wparam, lparam):
        """Procesar mensajes de Windows"""
        if msg == WM_POWERBROADCAST:
            if wparam == PBT_APMSUSPEND:
                print("🔒 Evento: Sistema intentando suspender")
                self.suspend_detected.emit()
                
                # Si estamos esperando NFC, prevenir la suspensión
                if self.prevent_sleep:
                    print("⛔ BLOQUEANDO suspensión del sistema")
                    self.keep_system_awake()
                    return BROADCAST_QUERY_DENY  # Denegar la suspensión
                    
            elif wparam == PBT_APMRESUMESUSPEND:
                print("🔓 Evento: Sistema reanudando")
                self.resume_detected.emit()
                self.allow_system_sleep()
        
        return DefWindowProcW(hwnd, msg, wparam, lparam)
    
    def keep_system_awake(self):
        """Mantener el sistema y la pantalla despiertos"""
        result = SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )
        if result:
            print("✅ Sistema configurado para mantenerse despierto")
        else:
            print("❌ Error al configurar estado de ejecución")
    
    def allow_system_sleep(self):
        """Permitir que el sistema entre en suspensión normalmente"""
        SetThreadExecutionState(ES_CONTINUOUS)
        print("✅ Sistema puede suspenderse normalmente")
    
    def set_prevent_sleep(self, prevent):
        """Activar/desactivar prevención de suspensión"""
        self.prevent_sleep = prevent
        if prevent:
            self.keep_system_awake()
        else:
            self.allow_system_sleep()
    
    def stop(self):
        """Detener el thread"""
        self.running = False
        self.allow_system_sleep()
        if self.hwnd:
            PostMessageW(self.hwnd, 0x0012, 0, 0)  # WM_QUIT

# --- ASSETS (SVGs) ---
class Assets:
    LOGO_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#6ADD30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 17L12 22L22 17" stroke="#6ADD30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M2 12L12 17L22 12" stroke="#6ADD30" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    CLOSE_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 6L6 18" stroke="#ff5f56" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M6 6L18 18" stroke="#ff5f56" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    MINIMIZE_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 12H19" stroke="#ffbd2e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    LOCK_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="11" width="18" height="11" rx="2" ry="2" stroke="#c9d1d9" stroke-width="2"/>
        <path d="M7 11V7C7 4.23858 9.23858 2 12 2C14.7614 2 17 4.23858 17 7V11" stroke="#c9d1d9" stroke-width="2"/>
    </svg>
    """
    USER_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    WALLET_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 12V8H6C4.89543 8 4 8.89543 4 10V20C4 21.1046 4.89543 22 6 22H20C21.1046 22 22 21.1046 22 20V12H20Z" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M22 12V16H20" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M4 10V4C4 2.89543 4.89543 2 6 2H16" stroke="#c9d1d9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    CHECK_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M20 6L9 17L4 12" stroke="#2ea44f" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
    CARD_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="5" width="20" height="14" rx="2" stroke="#c9d1d9" stroke-width="2"/>
        <path d="M2 10H22" stroke="#c9d1d9" stroke-width="2"/>
    </svg>
    """
    WIRELESS_SVG = """
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M5 12.55C5 12.55 7.5 9.5 12 9.5C16.5 9.5 19 12.55 19 12.55" stroke="#6ADD30" stroke-width="2" stroke-linecap="round"/>
        <path d="M7.5 15.05C7.5 15.05 9.25 13 12 13C14.75 13 16.5 15.05 16.5 15.05" stroke="#6ADD30" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="17" r="1.5" fill="#6ADD30"/>
    </svg>
    """

# --- CUSTOM WIDGETS ---

class SvgWidget(QWidget):
    def __init__(self, svg_content, size=24):
        super().__init__()
        self.svg_content = svg_content
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        try:
            from PyQt5.QtSvg import QSvgRenderer
            renderer = QSvgRenderer(bytearray(self.svg_content, 'utf-8'))
            renderer.render(painter)
        except ImportError:
            painter.setPen(Qt.white)
            painter.drawText(self.rect(), Qt.AlignCenter, "?")

class CustomTitleBar(QWidget):
    def __init__(self, parent=None, title="GlintPay"):
        super().__init__(parent)
        self.setFixedHeight(32)
        self.parent = parent
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(8, 0, 8, 0)
        self.layout.setSpacing(8)
        
        self.icon = SvgWidget(Assets.LOGO_SVG, 16)
        self.layout.addWidget(self.icon)
        
        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #c9d1d9; font-weight: bold; font-size: 11px;")
        self.layout.addWidget(self.title_label)
        
        self.layout.addStretch()
        
        self.btn_min = self.create_nav_btn(Assets.MINIMIZE_SVG, self.minimize_window)
        self.btn_close = self.create_nav_btn(Assets.CLOSE_SVG, self.close_window)
        
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.start = QPoint(0, 0)
        self.pressing = False

    def create_nav_btn(self, svg, callback):
        btn = QPushButton()
        btn.setFixedSize(24, 24)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
        """)
        layout = QVBoxLayout(btn)
        layout.setContentsMargins(4, 4, 4, 4)
        svg_widget = SvgWidget(svg, 16)
        layout.addWidget(svg_widget)
        btn.clicked.connect(callback)
        return btn

    def minimize_window(self):
        self.parent.showMinimized()

    def close_window(self):
        self.parent.close()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(self.parent.x() + movement.x(),
                                  self.parent.y() + movement.y(),
                                  self.parent.width(),
                                  self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False

class HelperBubble(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setStyleSheet("""
            background-color: #2ea44f;
            color: white;
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 11px;
        """)
        self.hide()

class StepperWidget(QWidget):
    def __init__(self, steps, parent=None):
        super().__init__(parent)
        self.steps = steps
        self.current_step = 0
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(12, 6, 12, 6)
        self.layout.setSpacing(8)
        self.labels = []
        
        for i, step_name in enumerate(steps):
            lbl = QLabel(step_name)
            lbl.setAlignment(Qt.AlignCenter)
            self.labels.append(lbl)
            self.layout.addWidget(lbl)
            if i < len(steps) - 1:
                line = QFrame()
                line.setFrameShape(QFrame.HLine)
                line.setStyleSheet("background-color: #30363d; max-height: 1px;")
                self.layout.addWidget(line)
        
        self.update_steps(0)

    def update_steps(self, index):
        self.current_step = index
        for i, lbl in enumerate(self.labels):
            if i == index:
                lbl.setStyleSheet("color: #2ea44f; font-weight: bold; font-size: 11px;")
            elif i < index:
                lbl.setStyleSheet("color: #8b949e; font-size: 10px;")
            else:
                lbl.setStyleSheet("color: #484f58; font-size: 10px;")

# --- WIZARD STEPS ---

class WizardStep(QWidget):
    def __init__(self, title, subtitle, parent_wizard):
        super().__init__()
        self.wizard = parent_wizard
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 12, 20, 12)
        self.layout.setSpacing(8)
        
        # Header
        self.title = QLabel(title)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        self.subtitle = QLabel(subtitle)
        self.subtitle.setStyleSheet("font-size: 12px; color: #8b949e;")
        
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.subtitle)
        
        # Content Area
        self.content_area = QVBoxLayout()
        self.content_area.setSpacing(12)
        self.layout.addLayout(self.content_area)
        
        self.layout.addStretch()
        
        # Navigation
        self.nav_layout = QHBoxLayout()
        self.nav_layout.setSpacing(8)
        self.btn_back = QPushButton("Atrás")
        self.btn_next = QPushButton("Siguiente")
        
        self.style_nav_btn(self.btn_back, secondary=True)
        self.style_nav_btn(self.btn_next)
        
        self.btn_back.clicked.connect(self.go_back)
        self.btn_next.clicked.connect(self.go_next)
        
        self.nav_layout.addWidget(self.btn_back)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.btn_next)
        
        self.layout.addLayout(self.nav_layout)
        
        # Helper
        self.helper = HelperBubble("", self)

    def style_nav_btn(self, btn, secondary=False):
        if secondary:
            bg = "transparent"
            hover = "rgba(255,255,255,0.05)"
        else:
            bg = "#2ea44f"
            hover = "#2c974b"
            
        btn.setFixedHeight(32)
        btn.setMinimumWidth(80)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
                padding: 0 16px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
        """)

    def go_back(self):
        self.wizard.prev_step()

    def go_next(self):
        if self.validate():
            self.wizard.next_step()

    def validate(self):
        return True
    
    def clear_fields(self):
        pass
        
    def show_helper(self, text, widget):
        self.helper.setText(text)
        self.helper.adjustSize()
        pos = widget.mapTo(self, QPoint(0, -self.helper.height() - 5))
        self.helper.move(pos)
        self.helper.show()
        QTimer.singleShot(3000, self.helper.hide)

class CardTypeStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Tipo de Tarjeta", "Selecciona el modo de pago.", wizard)
        self.btn_back.hide()
        self.btn_next.hide()
        
        # Botón Tarjeta Física
        self.btn_physical = self.create_card_button(
            Assets.CARD_SVG,
            "Tarjeta Física",
            "Ingreso manual de datos"
        )
        self.btn_physical.clicked.connect(lambda: self.select_mode("physical"))
        
        # Botón Tarjeta Inalámbrica
        self.btn_wireless = self.create_card_button(
            Assets.WIRELESS_SVG,
            "Tarjeta Inalámbrica",
            "Lectura automática NFC"
        )
        self.btn_wireless.clicked.connect(lambda: self.select_mode("wireless"))
        
        self.content_area.addWidget(self.btn_physical)
        self.content_area.addWidget(self.btn_wireless)
        
        # Estado de espera
        self.waiting_for_card = False
        self.waiting_label = None
        
    def create_card_button(self, svg, title, subtitle):
        btn = QPushButton()
        btn.setFixedHeight(100)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.03);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                text-align: left;
                padding: 16px;
            }
            QPushButton:hover {
                background-color: rgba(46, 164, 79, 0.1);
                border: 2px solid #2ea44f;
            }
        """)
        
        layout = QHBoxLayout(btn)
        layout.setSpacing(16)
        
        icon = SvgWidget(svg, 48)
        layout.addWidget(icon)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        
        subtitle_lbl = QLabel(subtitle)
        subtitle_lbl.setStyleSheet("font-size: 12px; color: #8b949e;")
        
        text_layout.addWidget(title_lbl)
        text_layout.addWidget(subtitle_lbl)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        return btn
    
    def select_mode(self, mode):
        self.wizard.card_mode = mode
        if mode == "wireless":
            # Modo inalámbrico: esperar evento de suspensión
            self.waiting_for_card = True
            self.show_waiting_screen()
            self.wizard.waiting_for_nfc = True
            # Activar prevención de suspensión
            self.wizard.power_monitor.set_prevent_sleep(True)
            print("📡 Modo NFC activado - Esperando cierre de tapa")
        else:
            # Modo físico: ir a login normal
            self.wizard.waiting_for_nfc = False
            self.wizard.power_monitor.set_prevent_sleep(False)
            self.wizard.next_step()
    
    def show_waiting_screen(self):
        """Mostrar pantalla de espera para lectura NFC"""
        # Ocultar botones
        self.btn_physical.hide()
        self.btn_wireless.hide()
        
        # Cambiar título
        self.title.setText("Esperando Tarjeta")
        self.subtitle.setText("Acerca tu tarjeta al lector NFC")
        
        # Agregar indicador de espera
        self.waiting_label = QLabel("📡")
        self.waiting_label.setStyleSheet("font-size: 64px;")
        self.waiting_label.setAlignment(Qt.AlignCenter)
        self.content_area.addWidget(self.waiting_label)
        
        instruction = QLabel("Cierra la tapa del laptop para simular\nla lectura de la tarjeta inalámbrica")
        instruction.setStyleSheet("color: #8b949e; font-size: 13px;")
        instruction.setAlignment(Qt.AlignCenter)
        instruction.setWordWrap(True)
        self.content_area.addWidget(instruction)
        
        # Botón cancelar
        self.btn_cancel = QPushButton("Cancelar")
        self.style_nav_btn(self.btn_cancel, secondary=True)
        self.btn_cancel.clicked.connect(self.cancel_waiting)
        self.nav_layout.addWidget(self.btn_cancel)
        
        # Animar el icono
        self.animate_timer = QTimer()
        self.animate_timer.timeout.connect(self.animate_waiting)
        self.animate_timer.start(500)
        self.animate_state = 0
    
    def animate_waiting(self):
        """Animar el icono de espera"""
        icons = ["📡", "📶", "📡", "📶"]
        self.animate_state = (self.animate_state + 1) % len(icons)
        if self.waiting_label:
            self.waiting_label.setText(icons[self.animate_state])
    
    def cancel_waiting(self):
        """Cancelar la espera y volver a la selección"""
        self.waiting_for_card = False
        self.wizard.waiting_for_nfc = False
        self.wizard.power_monitor.set_prevent_sleep(False)
        if hasattr(self, 'animate_timer'):
            self.animate_timer.stop()
        self.reset_screen()
    
    def reset_screen(self):
        """Resetear la pantalla a la selección inicial"""
        # Limpiar widgets de espera
        if self.waiting_label:
            self.waiting_label.deleteLater()
            self.waiting_label = None
        
        # Limpiar otros widgets del content_area
        while self.content_area.count() > 2:
            item = self.content_area.takeAt(2)
            if item.widget():
                item.widget().deleteLater()
        
        # Remover botón cancelar
        if hasattr(self, 'btn_cancel'):
            self.btn_cancel.deleteLater()
        
        # Restaurar título
        self.title.setText("Tipo de Tarjeta")
        self.subtitle.setText("Selecciona el modo de pago.")
        
        # Mostrar botones
        self.btn_physical.show()
        self.btn_wireless.show()
    
    def on_card_read_success(self):
        """Llamado cuando se detecta la tarjeta (suspensión detectada)"""
        if self.waiting_for_card:
            self.waiting_for_card = False
            self.wizard.power_monitor.set_prevent_sleep(False)
            if hasattr(self, 'animate_timer'):
                self.animate_timer.stop()
            
            # Autocompletar datos
            self.wizard.data['cedula'] = str(random.randint(10000000, 30000000))
            self.wizard.data['tipo'] = "Cuenta Ahorro"
            self.wizard.data['pin'] = "1234"
            
            # Mostrar mensaje de éxito
            if self.waiting_label:
                self.waiting_label.setText("✅")
            
            self.subtitle.setText("¡Tarjeta leída exitosamente!")
            self.subtitle.setStyleSheet("font-size: 12px; color: #2ea44f;")
            
            # Ir a la pantalla de monto después de un breve delay
            QTimer.singleShot(1500, lambda: self.wizard.stack.setCurrentIndex(3))
            QTimer.singleShot(1500, self.wizard.update_stepper)
    
    def on_card_read_error(self):
        """Llamado cuando hay un error en la lectura"""
        if self.waiting_for_card:
            # Mostrar error
            if self.waiting_label:
                self.waiting_label.setText("❌")
            
            self.subtitle.setText("Error: No se pudo leer la tarjeta")
            self.subtitle.setStyleSheet("font-size: 12px; color: #ff5f56;")
            
            # Volver a la selección después de 2 segundos
            QTimer.singleShot(2000, self.cancel_waiting)
    
    def clear_fields(self):
        if hasattr(self, 'animate_timer') and self.animate_timer.isActive():
            self.animate_timer.stop()
        self.waiting_for_card = False
        self.reset_screen()

class LoginStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Bienvenido", "Ingresa tu clave de acceso.", wizard)
        self.btn_back.hide()
        
        icon = SvgWidget(Assets.LOCK_SVG, 48)
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(icon)
        center_layout.addStretch()
        self.content_area.addLayout(center_layout)
        
        self.pin_input = QLineEdit()
        self.pin_input.setPlaceholderText("PIN")
        self.pin_input.setEchoMode(QLineEdit.Password)
        self.pin_input.setMaxLength(4)
        self.pin_input.setAlignment(Qt.AlignCenter)
        self.pin_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.03);
                border: none;
                color: white;
                padding: 12px;
                font-size: 20px;
                letter-spacing: 8px;
                border-radius: 4px;
            }
            QLineEdit:focus {
                background-color: rgba(46, 164, 79, 0.1);
            }
        """)
        self.content_area.addWidget(self.pin_input)

    def validate(self):
        if len(self.pin_input.text()) < 4:
            self.show_helper("El PIN debe tener 4 dígitos", self.pin_input)
            return False
        return True
    
    def clear_fields(self):
        self.pin_input.clear()

class InfoStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Datos", "Información del beneficiario.", wizard)
        
        self.cedula = QLineEdit()
        self.cedula.setPlaceholderText("Cédula de Identidad")
        self.cedula.setStyleSheet(self.input_style())
        
        self.tipo = QComboBox()
        self.tipo.addItems(["Cuenta Ahorro", "Cuenta Corriente"])
        self.tipo.setStyleSheet("""
            QComboBox {
                background-color: rgba(255, 255, 255, 0.03);
                border: none;
                color: white;
                padding: 10px;
                border-radius: 4px;
                font-size: 13px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox:hover { background-color: rgba(255, 255, 255, 0.05); }
            QComboBox QAbstractItemView {
                background-color: #161b22;
                border: none;
                selection-background-color: #2ea44f;
            }
        """)
        
        self.content_area.addWidget(self.cedula)
        self.content_area.addWidget(self.tipo)

    def input_style(self):
        return """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.03);
                border: none;
                color: white;
                padding: 10px;
                font-size: 13px;
                border-radius: 4px;
            }
            QLineEdit:focus { background-color: rgba(46, 164, 79, 0.1); }
        """

    def validate(self):
        if not self.cedula.text():
            self.show_helper("Ingresa una cédula válida", self.cedula)
            return False
        self.wizard.data['cedula'] = self.cedula.text()
        self.wizard.data['tipo'] = self.tipo.currentText()
        return True
    
    def clear_fields(self):
        self.cedula.clear()
        self.tipo.setCurrentIndex(0)

class AmountStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Monto", "¿Cuánto deseas transferir?", wizard)
        
        icon = SvgWidget(Assets.WALLET_SVG, 40)
        center = QHBoxLayout()
        center.addStretch()
        center.addWidget(icon)
        center.addStretch()
        self.content_area.addLayout(center)
        
        self.monto = QLineEdit()
        self.monto.setPlaceholderText("0.00")
        self.monto.setAlignment(Qt.AlignRight)
        self.monto.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.03);
                border: none;
                color: #2ea44f;
                padding: 12px;
                font-size: 28px;
                font-weight: bold;
                border-radius: 4px;
            }
            QLineEdit:focus { background-color: rgba(46, 164, 79, 0.1); }
        """)
        
        self.content_area.addWidget(self.monto)
        
        self.balance_lbl = QLabel(f"Saldo disponible: {self.wizard.saldo:.2f} BsF")
        self.balance_lbl.setStyleSheet("color: #8b949e; font-size: 11px;")
        self.balance_lbl.setAlignment(Qt.AlignRight)
        self.content_area.addWidget(self.balance_lbl)

    def validate(self):
        try:
            val = float(self.monto.text())
            if val <= 0:
                self.show_helper("El monto debe ser mayor a 0", self.monto)
                return False
            if val * 1.16 > self.wizard.saldo:
                self.show_helper("Saldo insuficiente (recuerda el IVA)", self.monto)
                return False
            self.wizard.data['monto'] = val
            return True
        except ValueError:
            self.show_helper("Ingresa un número válido", self.monto)
            return False
    
    def update_balance_label(self):
        self.balance_lbl.setText(f"Saldo disponible: {self.wizard.saldo:.2f} BsF")

    def clear_fields(self):
        self.monto.clear()
        self.update_balance_label()

class ProcessingStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Procesando", "Validando transacción...", wizard)
        self.btn_back.hide()
        self.btn_next.hide()
        
        self.bar = QProgressBar()
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 2px;
                height: 3px;
            }
            QProgressBar::chunk {
                background-color: #2ea44f;
                border-radius: 2px;
            }
        """)
        self.content_area.addSpacing(20)
        self.content_area.addWidget(self.bar)
        
    def start_process(self):
        self.bar.setValue(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bar)
        self.timer.start(50)
        
    def update_bar(self):
        val = self.bar.value()
        if val >= 100:
            self.timer.stop()
            self.wizard.finish_transaction()
        else:
            self.bar.setValue(val + 2)

class ResultStep(WizardStep):
    def __init__(self, wizard):
        super().__init__("Recibo", "Transacción finalizada", wizard)
        self.btn_back.hide()
        self.btn_next.setText("Finalizar")
        self.btn_next.clicked.disconnect()
        self.btn_next.clicked.connect(self.wizard.reset_wizard)
        
        self.icon = SvgWidget(Assets.CHECK_SVG, 48)
        center = QHBoxLayout()
        center.addStretch()
        center.addWidget(self.icon)
        center.addStretch()
        self.content_area.addLayout(center)
        
        self.details = QLabel()
        self.details.setStyleSheet("color: #c9d1d9; font-family: monospace; font-size: 11px;")
        self.details.setAlignment(Qt.AlignCenter)
        self.content_area.addWidget(self.details)

    def set_receipt(self, text):
        self.details.setText(text)

# --- PAYMENT VERIFICATION WINDOW ---

class PaymentVerificationWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 350)
        
        # Mensajes de transacciones bancarias (éxito y errores)
        self.messages = [
            ("❌", "TRANSACCIÓN FALLIDA", "No se pudo completar la operación", "#ff5f56"),
            ("✅", "TRANSACCIÓN EXITOSA", "Pago procesado correctamente", "#2ea44f"),
            ("⚠️", "FONDOS INSUFICIENTES", "Saldo no disponible para esta operación", "#ffbd2e"),
            ("🔒", "TARJETA BLOQUEADA", "Su tarjeta ha sido bloqueada por seguridad", "#ff5f56"),
            ("❌", "PIN INVÁLIDO", "El PIN ingresado es incorrecto", "#ff5f56"),
            ("⚠️", "CÉDULA INVÁLIDA", "Documento de identidad no verificado", "#ffbd2e"),
            ("❌", "ERROR DE CONEXIÓN", "No se pudo conectar con el servidor", "#ff5f56"),
            ("⏳", "TRANSACCIÓN PENDIENTE", "Esperando confirmación del banco", "#8b949e"),
            ("❌", "LÍMITE EXCEDIDO", "Ha superado el límite diario de transacciones", "#ff5f56"),
            ("⚠️", "CUENTA SUSPENDIDA", "Su cuenta requiere verificación", "#ffbd2e"),
            ("✅", "PAGO CONFIRMADO", "Transferencia realizada exitosamente", "#2ea44f"),
            ("❌", "DATOS INCORRECTOS", "Verifique la información ingresada", "#ff5f56"),
            ("⚠️", "SESIÓN EXPIRADA", "Por favor inicie sesión nuevamente", "#ffbd2e"),
            ("🔒", "ACCESO DENEGADO", "Autenticación requerida", "#ff5f56"),
            ("✅", "OPERACIÓN APROBADA", "Su pago ha sido procesado", "#2ea44f"),
        ]
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        
        # Container
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: none;
                border-radius: 8px;
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 200))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(30, 30, 30, 30)
        self.container_layout.setSpacing(20)
        
        # Icono
        self.icon_label = QLabel("⏳")
        self.icon_label.setStyleSheet("font-size: 64px;")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.icon_label)
        
        # Título
        self.title = QLabel("PROCESANDO")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffffff;")
        self.title.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.title)
        
        # Mensaje
        self.message_label = QLabel("Verificando transacción...")
        self.message_label.setStyleSheet("color: #8b949e; font-size: 14px;")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.container_layout.addWidget(self.message_label)
        
        # Referencia
        self.ref_label = QLabel("")
        self.ref_label.setStyleSheet("color: #484f58; font-size: 11px; font-family: monospace;")
        self.ref_label.setAlignment(Qt.AlignCenter)
        self.container_layout.addWidget(self.ref_label)
        
        self.main_layout.addWidget(self.container)
        
        # Timer para mostrar resultado
        self.result_timer = QTimer()
        self.result_timer.timeout.connect(self.show_random_result)
        
    def start_verification(self):
        # Generar referencia aleatoria
        ref = random.randint(10000000, 99999999)
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.ref_label.setText(f"REF: {ref} | {date}")
        
        # Mostrar resultado después de 2-4 segundos
        delay = random.randint(2000, 4000)
        self.result_timer.singleShot(delay, self.show_random_result)
        
    def show_random_result(self):
        # Seleccionar mensaje aleatorio
        icon, title, message, color = random.choice(self.messages)
        
        self.icon_label.setText(icon)
        self.title.setText(title)
        self.title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
        self.message_label.setText(message)
        self.message_label.setStyleSheet(f"color: {color}; font-size: 14px;")
        
        # Cerrar después de 3 segundos
        QTimer.singleShot(3000, self.close)

# --- MAIN WINDOW ---

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(360, 560)
        
        self.saldo = 1000.00
        self.data = {}
        self.card_mode = None
        self.verification_window = None
        self.waiting_for_nfc = False
        
        # Iniciar monitor de energía en thread separado
        self.power_monitor = PowerMonitorThread()
        self.power_monitor.suspend_detected.connect(self.on_system_suspend)
        self.power_monitor.resume_detected.connect(self.on_system_resume)
        self.power_monitor.start()
        
        print("🚀 GlintPay iniciado")
        print("📋 Monitor de energía activo")
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        
        # Container with Shadow
        self.container = QFrame()
        self.container.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: none;
                border-radius: 8px;
            }
            QLabel { color: #c9d1d9; }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(16)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 4)
        self.container.setGraphicsEffect(shadow)
        
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        # Title Bar
        self.title_bar = CustomTitleBar(self)
        self.container_layout.addWidget(self.title_bar)
        
        # Stepper
        self.stepper = StepperWidget(["Tipo", "Login", "Datos", "Monto"], self)
        self.container_layout.addWidget(self.stepper)
        
        # Wizard Stack
        self.stack = QStackedWidget()
        self.steps = []
        
        self.steps.append(CardTypeStep(self))  # 0
        self.steps.append(LoginStep(self))     # 1
        self.steps.append(InfoStep(self))      # 2
        self.steps.append(AmountStep(self))    # 3
        self.steps.append(ProcessingStep(self))# 4
        self.steps.append(ResultStep(self))    # 5
        
        for step in self.steps:
            self.stack.addWidget(step)
            
        self.container_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.container)
    
    def on_system_suspend(self):
        """Llamado cuando el sistema intenta entrar en suspensión (tapa cerrada)"""
        print("🔒 Evento de suspensión detectado")
        
        # Si estamos esperando lectura NFC, simular lectura de tarjeta
        if self.waiting_for_nfc and isinstance(self.stack.currentWidget(), CardTypeStep):
            print("📡 Leyendo tarjeta NFC...")
            print("✅ Tarjeta detectada - Procesando datos")
            
            # Simular un pequeño delay de lectura
            QTimer.singleShot(500, self.complete_nfc_read)
    
    def complete_nfc_read(self):
        """Completar la lectura NFC"""
        if self.waiting_for_nfc and isinstance(self.stack.currentWidget(), CardTypeStep):
            self.waiting_for_nfc = False
            self.steps[0].on_card_read_success()
    
    def on_system_resume(self):
        """Llamado cuando el sistema se reanuda (tapa abierta)"""
        print("🔓 Sistema reanudado")
    
    def closeEvent(self, event):
        """Limpiar recursos al cerrar"""
        print("👋 Cerrando aplicación")
        
        # Detener el monitor de energía
        if hasattr(self, 'power_monitor'):
            self.power_monitor.stop()
            self.power_monitor.wait(2000)  # Esperar máximo 2 segundos
        
        event.accept()

    def next_step(self):
        current = self.stack.currentIndex()
        if current < self.stack.count() - 1:
            self.stack.setCurrentIndex(current + 1)
            self.update_stepper()
            if isinstance(self.stack.currentWidget(), ProcessingStep):
                self.stack.currentWidget().start_process()

    def prev_step(self):
        current = self.stack.currentIndex()
        if current > 0:
            self.stack.setCurrentIndex(current - 1)
            self.update_stepper()
            
    def update_stepper(self):
        idx = self.stack.currentIndex()
        if idx >= 4:
            self.stepper.update_steps(3)
        elif idx == 0:
            self.stepper.update_steps(0)
        else:
            self.stepper.update_steps(idx - 1 if self.card_mode == "wireless" and idx > 0 else idx)

    def finish_transaction(self):
        monto = self.data.get('monto', 0)
        iva = monto * 0.16
        total = monto + iva
        
        self.saldo -= total
        
        ref = random.randint(10000000, 99999999)
        date = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        receipt = f"""GLINTPAY RECEIPT
----------------
Fecha: {date}
Ref: {ref}

Monto:  Bs {monto:.2f}
IVA:    Bs {iva:.2f}
TOTAL:  Bs {total:.2f}

Saldo Restante:
Bs {self.saldo:.2f}"""
        
        self.steps[-1].set_receipt(receipt)
        self.next_step()
        
    def reset_wizard(self):
        for step in self.steps:
            step.clear_fields()
        
        self.card_mode = None
        self.steps[3].update_balance_label()
        self.stack.setCurrentIndex(0)
        self.update_stepper()

def main():
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 9)
    app.setFont(font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
