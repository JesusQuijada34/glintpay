document.getElementById("formulario").addEventListener("submit", function (e) {
  e.preventDefault();
  alert("Consulta realizada. ¡Gracias por usar GlintPay!");
});

const osInfo = document.getElementById("os-info");
let os = "Desconocido";

if (navigator.userAgent.indexOf("Win") !== -1) os = "Windows";
else if (navigator.userAgent.indexOf("Mac") !== -1) os = "MacOS";
else if (navigator.userAgent.indexOf("Linux") !== -1) os = "Linux";
else if (/Android/i.test(navigator.userAgent)) os = "Android";
else if (/iPhone|iPad/i.test(navigator.userAgent)) os = "iOS";

osInfo.textContent = `Sistema Detectado: ${os}`;
