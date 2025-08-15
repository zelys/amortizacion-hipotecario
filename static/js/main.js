// Funcionalidad para alternar entre componentes
document.addEventListener('DOMContentLoaded', function() {
    // Si hay botones para volver al formulario en la página
    const botones = document.querySelectorAll('.toggle-form-button');
    botones.forEach(function(boton) {
        boton.addEventListener('click', function() {
            const formComponent = document.getElementById('form-component');
            const tableComponent = document.getElementById('table-component');
            
            if (formComponent && tableComponent) {
                formComponent.style.display = 'block';
                tableComponent.style.display = 'none';
            }
        });
    });
});
