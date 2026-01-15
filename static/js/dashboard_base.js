document.addEventListener('DOMContentLoaded', function() {
    // 1. Inicializar Sidenav
    var sidenavElems = document.querySelectorAll('.sidenav');
    var sidenavInstances = M.Sidenav.init(sidenavElems, {
        edge: 'left',
        draggable: true
    });

    // 2. Inicializar Collapsibles (Acordeón del menú)
    var collapsibleElems = document.querySelectorAll('.collapsible');
    var collapsibleInstances = M.Collapsible.init(collapsibleElems, {
        accordion: false // false = permite abrir varios menús a la vez
    });

    // 3. Inicializar Selects (si tienes formularios en el dashboard)
    var selectElems = document.querySelectorAll('select');
    var selectInstances = M.FormSelect.init(selectElems);

    // 4. Inicializar Dropdowns (para notificaciones/perfil si usas)
    var dropdownElems = document.querySelectorAll('.dropdown-trigger');
    var dropdownInstances = M.Dropdown.init(dropdownElems, {
        alignment: 'right',
        constrainWidth: false
    });

    // --- LÓGICA DE ACTIVACIÓN AUTOMÁTICA Y FLECHAS ---

    // Detectar URL actual
    var currentPath = window.location.pathname;
    
    // Obtener todos los enlaces del menú
    var menuLinks = document.querySelectorAll('.sidenav .collapsible-body li a');

    menuLinks.forEach(function(link) {
        var linkHref = link.getAttribute('href');

        // Si la URL actual coincide con el enlace (o es una sub-ruta)
        // Nota: Ajusta la lógica si usas URLs relativas complejas
        if (linkHref !== '#' && currentPath === linkHref) {
            
            // 1. Activar el item específico (li)
            var parentLi = link.parentElement;
            parentLi.classList.add('active-item'); // Usamos tu clase 'active-item'
            
            // 2. Abrir el Collapsible padre
            var parentCollapsibleBody = link.closest('.collapsible-body');
            if (parentCollapsibleBody) {
                parentCollapsibleBody.style.display = 'block'; // Forzar visualización
                
                // Activar el Header del collapsible (para rotar la flecha)
                var parentHeaderLi = parentCollapsibleBody.parentElement;
                parentHeaderLi.classList.add('active');
                
                var headerLink = parentHeaderLi.querySelector('.collapsible-header');
                if (headerLink) {
                    headerLink.classList.add('active');
                }
            }   
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // 1. Inicializar componentes de Materialize
    M.Sidenav.init(document.querySelectorAll('.sidenav'));
    M.Collapsible.init(document.querySelectorAll('.collapsible'), { accordion: false });
    M.Dropdown.init(document.querySelectorAll('.dropdown-trigger'), { alignment: 'right' });

    // 2. Lógica del Menú de 3 Estados
    const body = document.body;
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    const root = document.documentElement; // Para acceder a variables CSS

    // Estados: 0 = Expandido, 1 = Mini, 2 = Oculto
    let menuState = 0; 
    
    // Configuración de anchos (deben coincidir con CSS)
    const widthExpanded = '300px';
    const widthMini = '80px';
    const widthHidden = '0px';

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            menuState = (menuState + 1) % 3; // Ciclo: 0 -> 1 -> 2 -> 0

            switch (menuState) {
                case 0: // EXPANDIDO
                    body.classList.remove('is-mini', 'is-hidden');
                    root.style.setProperty('--sidenav-width-current', widthExpanded);
                    // Cambiar icono del botón (opcional)
                    toggleBtn.querySelector('i').textContent = 'menu_open'; 
                    break;

                case 1: // MINI (Solo Iconos)
                    body.classList.add('is-mini');
                    body.classList.remove('is-hidden');
                    root.style.setProperty('--sidenav-width-current', widthMini);
                    toggleBtn.querySelector('i').textContent = 'view_week';
                    break;

                case 2: // OCULTO
                    body.classList.add('is-hidden');
                    body.classList.remove('is-mini');
                    root.style.setProperty('--sidenav-width-current', widthHidden);
                    toggleBtn.querySelector('i').textContent = 'menu';
                    break;
            }
        });
    }

    // 3. Activación automática de enlaces (Mantiene tu lógica anterior)
    const currentPath = window.location.pathname;
    document.querySelectorAll('.sidenav .collapsible-body li a').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.parentElement.classList.add('active');
            const parentBody = link.closest('.collapsible-body');
            if (parentBody) {
                parentBody.style.display = 'block';
                parentBody.parentElement.classList.add('active');
                if(parentBody.parentElement.querySelector('.collapsible-header')) {
                    parentBody.parentElement.querySelector('.collapsible-header').classList.add('active');
                }
            }
        }
    });
});