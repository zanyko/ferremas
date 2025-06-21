function actualizarFechaReloj() {
    const ahora = new Date();
    const dia = ahora.getDate().toString().padStart(2, '0');
    const mes = (ahora.getMonth() + 1).toString().padStart(2, '0');
    const anio = ahora.getFullYear();
    const horas = ahora.getHours().toString().padStart(2, '0');
    const minutos = ahora.getMinutes().toString().padStart(2, '0');
    const segundos = ahora.getSeconds().toString().padStart(2, '0');
    const reloj = document.getElementById('reloj');
    if (reloj) {
        reloj.textContent = `${dia}/${mes}/${anio} ${horas}:${minutos}:${segundos}`;
    }
}
setInterval(actualizarFechaReloj, 1000);
actualizarFechaReloj();