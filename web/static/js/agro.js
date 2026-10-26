const Toast = Swal.mixin({
  toast: true, position: 'top-end', showConfirmButton: false,
  timer: 3500, timerProgressBar: true,
});
const AgroSwal = Swal.mixin({
  confirmButtonColor: '#4a7c3a', cancelButtonColor: '#8a9186',
  customClass: { popup: 'agro-swal' },
});

// Mensajes de Django -> toasts
const NIVELES = { success: 'success', error: 'error', warning: 'warning', info: 'info', debug: 'info' };
(window.DJANGO_MESSAGES || []).forEach(m => Toast.fire({ icon: NIVELES[m.level] || 'info', title: m.text }));

// Confirmación de cierre de sesión (si el JS falla, el formulario igual funciona)
const logoutForm = document.getElementById('logout-form');
if (logoutForm) {
  logoutForm.addEventListener('submit', async e => {
    e.preventDefault();
    const r = await AgroSwal.fire({
      icon: 'question', title: '¿Cerrar sesión?',
      text: 'Tendrás que iniciar sesión de nuevo para ver el catálogo.',
      showCancelButton: true, confirmButtonText: 'Sí, salir', cancelButtonText: 'Cancelar', reverseButtons: true,
    });
    if (r.isConfirmed) logoutForm.submit();
  });
}

// Funciones que llegan en próximos sprints
document.querySelectorAll('[data-soon]').forEach(btn => btn.addEventListener('click', () =>
  AgroSwal.fire({ icon: 'info', title: btn.dataset.soon, text: 'Esta función se habilita en un siguiente sprint.', confirmButtonText: 'Entendido' })
));

// Vista rápida de producto (modal)
document.addEventListener('click', e => {
  const btn = e.target.closest('[data-quickview]');
  if (!btn) return;
  const tpl = document.getElementById('qv-' + btn.dataset.quickview);
  const disponible = tpl.dataset.disponible === '1';
  AgroSwal.fire({
    html: tpl.innerHTML, width: 640, showCloseButton: true,
    showConfirmButton: disponible, confirmButtonText: '<i class="bi bi-cart-plus me-1"></i> Agregar al carrito',
    showCancelButton: true, cancelButtonText: 'Cerrar',
    customClass: { popup: 'agro-swal text-start' },
  }).then(r => {
    if (r.isConfirmed) Toast.fire({ icon: 'info', title: 'El carrito se activa en el siguiente paso' });
  });
});

// Mostrar/ocultar contraseña
window.addEventListener('load', () => {
  document.querySelectorAll('input[type=password]').forEach(inp => {
    const parent = inp.parentElement;
    parent.style.position = 'relative';
    const btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'pw-toggle'; btn.setAttribute('aria-label', 'Mostrar u ocultar contraseña');
    btn.innerHTML = '<i class="bi bi-eye"></i>';
    btn.style.top = inp.offsetTop + 'px'; btn.style.height = inp.offsetHeight + 'px';
    btn.addEventListener('click', () => {
      const oculto = inp.type === 'password';
      inp.type = oculto ? 'text' : 'password';
      btn.innerHTML = `<i class="bi bi-eye${oculto ? '-slash' : ''}"></i>`;
    });
    parent.appendChild(btn);
  });
});