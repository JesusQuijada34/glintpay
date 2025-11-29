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
    QFrame, QGraphicsDropShadowEffect, QProgressBar
)
from PyQt5.QtGui import QColor, QFont, QPainter
from PyQt5.QtCore import Qt, QPoint, QTimer

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

# --- MAIN WINDOW ---

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(360, 520)
        
        self.saldo = 1000.00
        self.data = {}
        
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
        self.stepper = StepperWidget(["Login", "Datos", "Monto", "Fin"], self)
        self.container_layout.addWidget(self.stepper)
        
        # Wizard Stack
        self.stack = QStackedWidget()
        self.steps = []
        
        self.steps.append(LoginStep(self))
        self.steps.append(InfoStep(self))
        self.steps.append(AmountStep(self))
        self.steps.append(ProcessingStep(self))
        self.steps.append(ResultStep(self))
        
        for step in self.steps:
            self.stack.addWidget(step)
            
        self.container_layout.addWidget(self.stack)
        self.main_layout.addWidget(self.container)

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
        if idx >= 3:
            self.stepper.update_steps(3)
        else:
            self.stepper.update_steps(idx)

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
        
        self.steps[2].update_balance_label()
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
