document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const submitBtn = document.getElementById('submitBtn');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('resultContainer');
    const resultCard = document.getElementById('resultCard');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const productName = document.getElementById('productName');
    const productPrice = document.getElementById('productPrice');
    const accountTypeDisplay = document.getElementById('accountTypeDisplay');
    const nationalityDisplay = document.getElementById('nationalityDisplay');
    const closeBtn = document.getElementById('closeBtn');

    // Base de datos simulada de productos de Amazon
    const amazonProducts = {
        "B08N5KWB9H": {
            name: "Echo Dot (4ª generación) | Altavoz inteligente con Alexa | Antracita",
            price: 39.99
        },
        "B07XKF5RMZ": {
            name: "Fire TV Stick con mando por voz Alexa | Streaming HD",
            price: 29.99
        },
        "B08KTZ8249": {
            name: "Kindle Paperwhite | Resistente al agua | 8GB",
            price: 119.99
        },
        "B07PGL2M5K": {
            name: "Apple AirPods con estuche de carga",
            price: 129.00
        },
        "B08BX7FV5L": {
            name: "Samsung Galaxy S21 5G | 128GB | Phantom Gray",
            price: 699.99
        },
        "B07DJD1RT3": {
            name: "AmazonBasics - Cable HDMI de alta velocidad",
            price: 6.99
        },
        "B07FK8SQ48": {
            name: "Logitech MX Master 3 - Ratón inalámbrico avanzado",
            price: 99.99
        },
        "B08L8J9X68": {
            name: "PlayStation 5 | Consola de juegos",
            price: 499.99
        },
        "B08PP5MSVB": {
            name: "Xbox Series X | Consola de juegos",
            price: 499.99
        },
        "B08N5KWB9H": {
            name: "Nintendo Switch con pantalla OLED | Consola de juegos",
            price: 349.99
        }
    };

    // Tipos de resultados posibles
    const transactionResults = [
        {
            type: "success",
            title: "TRANSACCIÓN EXITOSA",
            message: "¡Pago procesado correctamente! El producto ha sido adquirido."
        },
        {
            type: "error",
            title: "CLAVE ERRADA",
            message: "La clave ingresada no coincide. Por favor intente nuevamente."
        },
        {
            type: "error",
            title: "CUENTA BLOQUEADA",
            message: "Su cuenta ha sido bloqueada por seguridad. Contacte al servicio al cliente."
        },
        {
            type: "error",
            title: "FONDOS INSUFICIENTES",
            message: "No tiene suficiente saldo para completar esta transacción."
        },
        {
            type: "error",
            title: "TRANSACCIÓN FALLIDA",
            message: "Error en el procesamiento del pago. Intente nuevamente más tarde."
        },
        {
            type: "warning",
            title: "PENDIENTE DE APROBACIÓN",
            message: "Su transacción está siendo verificada. Recibirá una notificación pronto."
        },
        {
            type: "success",
            title: "PAGO APROBADO",
            message: "¡Felicidades! Su compra ha sido aprobada y será enviada pronto."
        }
    ];

    // Evento click del botón de enviar
    submitBtn.addEventListener('click', processTransaction);

    // Evento click del botón de cerrar
    closeBtn.addEventListener('click', closeResult);

    // Función para procesar la transacción
    function processTransaction() {
        // Obtener valores del formulario
        const idNumber = document.getElementById('idNumber').value;
        const password = document.getElementById('password').value;
        const productId = document.getElementById('productId').value.toUpperCase();
        const accountType = document.querySelector('input[name="accountType"]:checked').value;
        const nationality = document.querySelector('input[name="nationality"]:checked').value;

        // Validaciones básicas
        if (!idNumber || !password || !productId) {
            showPopup('ERROR', 'Por favor complete todos los campos', 'error');
            return;
        }

        // Mostrar loader
        showLoader();

        // Simular tiempo de búsqueda (1.5 a 3 segundos)
        const searchTime = Math.random() * 1500 + 1500;

        setTimeout(() => {
            // Ocultar loader
            hideLoader();

            // Buscar producto
            const product = amazonProducts[productId];
            
            if (!product) {
                showPopup('PRODUCTO NO ENCONTRADO', 'El ID del producto no existe en nuestra base de datos', 'error');
                return;
            }

            // Mostrar información del producto
            productName.textContent = product.name;
            productPrice.textContent = $${product.price.toFixed(2)};
            accountTypeDisplay.textContent = accountType === 'ahorro' ? 'Ahorro' : 'Corriente';
            nationalityDisplay.textContent = nationality === 'venezolano' ? 'Venezolano' : 'Extranjero';

            // Seleccionar un resultado aleatorio
            const randomResult = transactionResults[Math.floor(Math.random() * transactionResults.length)];

            // Mostrar el resultado
            showResult(randomResult);
        }, searchTime);
    }

    // Función para mostrar el loader
    function showLoader() {
        loader.classList.remove('hidden');
        loader.style.display = 'block';
    }

    // Función para ocultar el loader
    function hideLoader() {
        loader.classList.add('hidden');
        setTimeout(() => {
            loader.style.display = 'none';
        }, 300);
    }

    // Función para mostrar el resultado
    function showResult(result) {
        resultTitle.textContent = result.title;
        resultMessage.textContent = result.message;
        
        // Aplicar clase según el tipo de resultado
        resultTitle.className = 'result-title ' + result.type;
        resultMessage.className = 'result-message ' + result.type;
        
        // Mostrar el contenedor de resultados
        resultContainer.classList.add('show');
        resultCard.classList.add('animate__animated', 'animate__fadeInUp');
    }

    // Función para cerrar el resultado
    function closeResult() {
        resultContainer.classList.remove('show');
        resultCard.classList.remove('animate__animated', 'animate__fadeInUp');
    }

    // Función para mostrar un popup (no usada actualmente)
    function showPopup(title, message, type) {
        // Implementación de popup personalizado si se desea
        alert(${title}: ${message});
    }
});
