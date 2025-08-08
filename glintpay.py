#!/usr/bin/env python
# -*- coding: utf-8 -*-
# kejq34/myapps/system/influent.shell.vIO-34-2.18-danenone.iflapp
# kejq34/home/influent.glintpay.v2-25.08-13.46-danenone/.gites
# App: GlintPay | Banco QT5/QSS Simulado
# publisher: influent
# name: glintpay
# version: IO-2-25.08-13.46-danenone
# script: Python3
# nocombination
#  
#  Copyright 2025 Jesus Quijada <@JesusQuijada34>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
import random
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox,
    QPushButton, QVBoxLayout, QTextEdit
)
from PyQt5.QtGui import QColor, QPalette, QIcon
from PyQt5.QtCore import Qt
import subprocess

saldo_simulado = 1000.00  # Saldo inicial

def aplicar_tema_fusion(app, modo="claro"):
    app.setStyle("Fusion")
    palette = QPalette()
    if modo == "oscuro":
        palette.setColor(QPalette.Window, QColor("#0d1117"))
        palette.setColor(QPalette.Base, QColor("#161b22"))
        palette.setColor(QPalette.Text, QColor("#c9d1d9"))
        palette.setColor(QPalette.Button, QColor("#21262d"))
        palette.setColor(QPalette.ButtonText, QColor("#c9d1d9"))
        palette.setColor(QPalette.Highlight, QColor("#2ea44f"))
    else:
        palette.setColor(QPalette.Window, QColor("#ffffff"))
        palette.setColor(QPalette.Base, QColor("#D5E9FE"))
        palette.setColor(QPalette.Text, QColor("#6A7467"))
        palette.setColor(QPalette.Button, QColor("#46C423"))
        palette.setColor(QPalette.ButtonText, QColor("#000000"))
        palette.setColor(QPalette.Highlight, QColor("#2ea44f"))
    app.setPalette(palette)

class VentanaFactura(QWidget):
    def __init__(self, cedula, tipo_cuenta, monto, iva, total, saldo_restante):
        super().__init__()
        self.setWindowTitle("🧾 Factura Banco")
        self.setFixedSize(420, 360)
        layout = QVBoxLayout()
        referencia = random.randint(10000000, 99999999)
        doc = random.randint(10000, 99999)
        facturaid = random.randint(10000000, 99999999)
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        banco = random.choice(["BDV", "Banesco", "Mercantil", "Provincial"])
        mensaje = random.choice([
            "Aprobada",
            "Tarjeta Bloqueada",
            "Fondo Insuficiente",
            "Clave errada",
            "Error del servidor"
        ])
        recibo = QTextEdit()
        recibo.setReadOnly(True)
        recibo.setText("Imprimida en la terminal")
        subprocess.run(['clear'])
        print(f"""                      GLINTPAY
                  RIF G-382688518
          ALFARE CORRELATION ENGINE, INC.
    GITHUB NORDWILLE, CC STREET VILLE P/B LOCAL
               1 & 2 STREET WAYLAND
                 POSTAL CODE 0000
            PHONE: T.ME/JESUSQUIJADA34
Nombre: Cliente simple
CI/RIF: {cedula}
Dirección: 1
Teléfono: t.me/JesusQuijada34
Forma Pago: Contado
Vend.: GitHub
Doc.: {doc} Ref.: {referencia}
                    FACTURA
FACTURA:
----------------------------------------------
PRODUCTO (E)                      Bs. {monto}
----------------------------------------------
SUBTIL                            Bs. {monto}
----------------------------------------------
EXENTO                            Bs. {iva}
----------------------------------------------
BS                                Bs. {monto}
----------------------------------------------
TOTAL                             Bs. {total}
MH                                  Z7C7022418""") #V: {banco}{cedula}{tipo_cuenta}{monto:.2f}{iva:.2f}{total:.2f}{saldo_restante:.2f}{referencia}{fecha}{mensaje}
        recibo.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(recibo)
        self.setLayout(layout)

class VentanaRespuesta(QWidget):
    def __init__(self, mensaje, callback_factura):
        super().__init__()
        self.setWindowTitle("💳 Respuesta del Banco")
        self.setFixedSize(380, 200)
        self.setStyleSheet("background-color: white;")
        layout = QVBoxLayout()

        label = QLabel(mensaje)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; color: #d11a2a;")
        layout.addWidget(label)

        boton = QPushButton("Continuar")
        boton.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: 1px solid #2ea44f;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #22863a;
                border-color: #22863a;
            }
        """)
        boton.clicked.connect(lambda: [self.close(), callback_factura()])
        layout.addWidget(boton)
        self.setLayout(layout)

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🏦 GLINTPAY 🏦 | QT5 Full Edition")
        self.setFixedSize(420, 480)
        self.setWindowIcon(QIcon("app/app-icon.ico"))  # Icono principal
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.saldo_label = QLabel(f"Saldo: {saldo_simulado:.2f} BsF")
        self.saldo_label.setStyleSheet("font-size: 14px; margin: 8px;")
        layout.addWidget(self.saldo_label)

        self.clave = self.crear_input("🔐 Clave (PIN)")
        layout.addWidget(self.clave)

        self.cedula = self.crear_input("🧾 Cédula")
        layout.addWidget(self.cedula)

        self.tipo = QComboBox()
        self.tipo.addItems(["Ahorro", "Corriente"])
        self.tipo.setStyleSheet("""
            QComboBox {
                padding: 30px;
                font-size: 15px;
                color: #000
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #6ADD30;
            }
            QComboBox:hover {
                background-color: #67DE2B;
                border-color: #67D330;
            }
        """)
        layout.addWidget(self.tipo)

        self.monto = self.crear_input("💰 Monto en Bs")
        layout.addWidget(self.monto)

        pagar_btn = QPushButton("💸 Pagar")
        pagar_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ea44f;
                color: white;
                padding: 10px;
                font-size: 15px;
                border: 1px solid #2ea44f;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #22863a;
                border-color: #67D330;
            }
        """)
        pagar_btn.clicked.connect(self.accion_pagar)
        layout.addWidget(pagar_btn)

        self.setLayout(layout)

    def crear_input(self, placeholder):
        campo = QLineEdit()
        campo.setPlaceholderText(placeholder)
        campo.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #f6f8fa;
                color: #000;
            }
        """)
        return campo

    def accion_pagar(self):
        global saldo_simulado
        try:
            monto = float(self.monto.text())
        except ValueError:
            monto = 0.0

        iva = monto * 0.16
        total = monto + iva
        cedula = self.cedula.text()
        tipo_cuenta = self.tipo.currentText()

        self.clave.clear()
        self.cedula.clear()
        self.monto.clear()

        def abrir_factura():
            factura = VentanaFactura(cedula, tipo_cuenta, monto, iva, total, saldo_simulado)
            factura.show()

        if total > saldo_simulado or monto <= 0:
            mensaje = random.choice([
                "❌ Saldo insuficiente.",
                "🔒 Tarjeta bloqueada.",
                "🚫 Transacción denegada.",
                "⚠️ Error en el sistema.",
                "🕒 Tiempo agotado."
            ])
        else:
            saldo_simulado -= total
            self.saldo_label.setText(f"Saldo simulado: {saldo_simulado:.2f} BsF")
            mensaje = random.choice([
                "✅ Transacción aprobada.",
                "🎉 Compra procesada.",
            ])

        respuesta = VentanaRespuesta(mensaje, abrir_factura)
        respuesta.show()

def main():
    app = QApplication(sys.argv)
    aplicar_tema_fusion(app, modo="claro")  # Cambia a "oscuro" si prefieres
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
