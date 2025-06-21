function actualizarReloj() {
    const ahora = new Date();
    const horas = ahora.getHours().toString().padStart(2, '0');
    const minutos = ahora.getMinutes().toString().padStart(2, '0');
    const segundos = ahora.getSeconds().toString().padStart(2, '0');
    const reloj = document.getElementById('reloj');
    if (reloj) {
        reloj.textContent = `${horas}:${minutos}:${segundos}`;
    }
}
setInterval(actualizarReloj, 1000);
actualizarReloj();