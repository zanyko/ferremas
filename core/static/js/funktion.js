function validarSignUp(event) {
    event.preventDefault(); // Previene el envío del formulario

    let username = document.getElementById('id_username').value;
    let firstName = document.getElementById('id_first_name').value;
    let lastName = document.getElementById('id_last_name').value;
    let email = document.getElementById('id_email').value;
    let password1 = document.getElementById('id_password1').value;
    let password2 = document.getElementById('id_password2').value;
    let pic = document.getElementById('id_pic').value;

    let errorMessage = '';

    if (!username) {
        errorMessage += 'El campo Usuario es obligatorio.\n';
    }
    if(username.lenght<=3){
        alert('Porfavor su nombre de usuario debe ser mayor a 3 caracteres');
    }
    if (!firstName) {
        errorMessage += 'El campo Nombre es obligatorio.\n';
    }
    if(firstName.lenght<=3){
        alert('Porfavor su nombre debe ser mayor a 3 caracteres');
    }
    if (!lastName) {
        errorMessage += 'El campo Apellido es obligatorio.\n';
    }
    if(lastName.lenght<=3){
        alert('Porfavor su apellido debe ser mayor a 3 caracteres');
    }
    if (!email) {
        errorMessage += 'El campo Email es obligatorio.\n';
    } 
    else {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            errorMessage += 'El Email no es válido.\n';
        }
    }
    if (password1=='' || password2=='') {
        errorMessage += 'Los campos de Contraseña son obligatorios.\n';
    } 
    if (password1.lenght<=8 || password2.lenght<=8){
        alert('Cada contraseña debe ser mayor a 8 caracteres');
    }
    if (password1 !== password2) {
        errorMessage += 'Las contraseñas no coinciden.\n';
    }

    if (errorMessage) {
        alert(errorMessage);
    } 
    else {
        document.getElementById('signupForm').submit();
    }
}

function validarAddress(event) {
    event.preventDefault(); // Previene el envío del formulario

    let name = document.getElementById('id_name').value;
    let street = document.getElementById('id_street').value;
    let city = document.getElementById('id_city').value;
    let state = document.getElementById('id_state').value;
    let zipcode = document.getElementById('id_zipcode').value;
    let country = document.getElementById('id_country').value;
    let phone = document.getElementById('id_phone').value;

    let errorMessage = '';

    if (!name) {
        errorMessage += 'Ingrese nombre de la nueva dirección\n';
    }
    if(name.lenght<=3){
        alert('"Nombre" debe ser mayor a 3 caracteres');
    }
    if (!street) {
        errorMessage += 'Ingrese calle\n';
    }
    if(street.lenght<=3){
        alert('"Calle" debe ser mayor a 3 caracteres');
    }
    if (!city) {
        errorMessage += 'Ingrese ciudad\n';
    }
    if(city.lenght<=3){
        alert('"Ciudad" debe ser mayor a 3 caracteres');
    }
    if (!state) {
        errorMessage += 'Ingrese región\n';
    }
    if(state.lenght<=3){
        alert('"Región" debe ser mayor a 3 caracteres');
    }
    if (!zipcode) {
        errorMessage += 'Ingrese código postal\n';
    }
    if(zipcode.lenght<=3){
        alert('"Código postal" debe ser mayor a 3 caracteres');
    }
    if (!country) {
        errorMessage += 'Ingrese país\n';
    }
    if(country.lenght<=3){
        alert('"País" debe ser mayor a 3 caracteres');
    }
    if (!phone) {
        errorMessage += 'Ingrese telefóno\n';
    }
    if(phone.lenght<=3){
        alert('"Telefóno" debe ser mayor a 8 caracteres');
    }

    if (errorMessage) {
        alert(errorMessage);
    } 
    else {
        document.getElementById('addressForm').submit();
    }
}