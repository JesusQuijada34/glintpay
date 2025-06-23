const resultados = [
  "✅ Transacción Exitosa",
  "❌ Clave Incorrecta",
  "🔒 Tarjeta Bloqueada",
  "🪙 Fondos Insuficientes",
  "🔌 Error de Conexión",
  "❎ Transacción fallida",
];

document.getElementById("formulario").addEventListener("submit", function (e) {
  e.preventDefault();
  const resultado = resultados[Math.floor(Math.random() * resultados.length)];
  
  const alerta = document.createElement("div");
  alerta.textContent = resultado;
  alerta.className = "alerta";
  document.body.appendChild(alerta);
  
  setTimeout(() => {
    alerta.remove();
  }, 3000);
});
