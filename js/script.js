function procesarPago() {
  const cedula = document.getElementById("cedula").value.trim();
  const clave = document.getElementById("clave").value.trim();
  const nacionalidad = document.getElementById("nacionalidad").value;
  const cuenta = document.getElementById("cuenta").value;
  const productoID = document.getElementById("productoID").value.trim();
  const monto = parseFloat(document.getElementById("monto").value);
  const resultado = document.getElementById("resultado");

  // Validación básica
  if (!cedula || !clave || !productoID || !monto) {
    resultado.textContent = "⚠️ Por favor, completa todos los campos.";
    resultado.style.color = "orange";
    return;
  }

  // Buscar nombre simulado desde Amazon
  const nombresSimulados = {
    B07PGL2ZSL: "Auriculares Bluetooth X12",
    B084KQLVFH: "Teclado Mecánico Neón RGB",
    B098Z7Y53H: "Mouse Inalámbrico Pro Gamer",
    B0C1P7Q8JK: "Smartwatch Sirius V3",
    B0B1XL9ZQH: "Cargador Rápido USB-C 45W"
  };

  const nombreProducto = nombresSimulados[productoID] || "Producto desconocido";

  // Simular estado aleatorio de transacción
  const estados = [
    { mensaje: "✅ Transacción exitosa", color: "lime" },
    { mensaje: "❌ Clave errada", color: "red" },
    { mensaje: "⚠️ Cuenta bloqueada", color: "yellow" },
    { mensaje: "💸 Fondos insuficientes", color: "orange" },
    { mensaje: "🚫 Transacción fallida", color: "crimson" }
  ];

  const aleatorio = Math.floor(Math.random() * estados.length);
  const estado = estados[aleatorio];

  // Mostrar respuesta
  resultado.innerHTML = `
    <p style="color:${estado.color}; font-weight:bold; font-size:1.1em;">
      ${estado.mensaje}
    </p>
    <p><strong>Producto:</strong> ${nombreProducto}</p>
    <p><strong>Monto:</strong> $${monto.toFixed(2)}</p>
    <p><strong>Cuenta:</strong> ${cuenta} · ${nacionalidad}</p>
  `;
}
