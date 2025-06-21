import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import *
from .forms import *
from core.compras import Carrito
from django.core.mail import send_mail

from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.integration_type import IntegrationType
import requests




@login_required
def enviar_correo_usuario(request):
    print("")
    print("Entrando a enviar_correo_usuario")
    if request.method == "POST":
        print("")
        print("dentro de POST")
        subject = request.POST.get('subject', 'Asunto por defecto')
        message = request.POST.get('message', 'Mensaje por defecto')
        user_email = request.user.email

        send_mail(
            subject,
            message,
            None,  # Usa DEFAULT_FROM_EMAIL
            [user_email],
            fail_silently=False,
        )
        print("")
        print("retornando JsonResponce")

        return JsonResponse({'status': 'ok', 'msg': 'Correo enviado'})
    print("")
    print("no entro al if")
    return JsonResponse({'status': 'error', 'msg': 'Método no permitido'}, status=405)





#::::::::::::::::::::::::::::::::::::::::::::::
#::::::AQUI VAN TODOS LOS CRUD AAAAAAAAAA::::::
#::::::::::::::::::::::::::::::::::::::::::::::


def crear(request):
    if request.method=='POST':
        obraform = obraForm(request.POST, request.FILES)
        if obraform.is_valid():
            obraform.save()     # similar to"insert into" from sql
            messages.add_message(reques=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('buscar')
    else:
        obraform=obraForm()   # asign an empty form
    return render(request,'crear.html',{'obraform':obraform}) # keys symbols are obligatory


def buscar(request):
    productos = Producto.objects.all()     #similar a select * from Vehiculo
    return render(request, 'buscar.html', {'productos':productos})

def editar(request):
    productos = Producto.objects.all()      #similar a select * from Vehiculo
    return render(request, 'editar.html', {'productos':productos})

def inventario(request):
    productos = Producto.objects.all()      #similar a select * from Vehiculo
    return render(request, 'inventario.html', {'productos':productos})

def admire(request, id):
    producto = get_object_or_404(Producto, id = id) # cuando un objeto no ha sido encontrado se envia el error 404
    return render(request, 'admire.html', {'producto':producto}) # aqui se guarda lo encontrado en la linea anterior

def usuarios(request):
    usuarios = CustomUser.objects.all()
    return render(request, 'usuarios.html', {'usuarios':usuarios})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::: PRODUKTE :::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::


def products(request):
    productos = Producto.objects.all()     #similar a select * from table
    return render(request, 'products.html', {'productos':productos})

def productoCrear(request):
    if request.method=='POST':
        productform = productForm(request.POST, request.FILES)
        if productform.is_valid():
            productform.save()     # similar to"insert into" from sql
            messages.add_message(request=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('buscar')
    else:
        productform=productForm()   # asign an empty form
    return render(request,'productoCrear.html',{'productform':productform}) # keys symbols are obligatory

def productoModify(request, id):
    producto = Producto.objects.get(id=id) # buscara el objeto con la id enviada
    daten={'fillMe': productForm(instance=producto), 'producto':producto} 
        # rellenamos 'datos' con un formulario de tipo 'productForm' con los datos "producto" de la linea anterior, en el otro parametro creamos otro objeto 'producto'
    if request.method=='POST':
        formulario = productForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()   #actualiza la info del objeto
            messages.add_message(request=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('editar')
    return render(request, 'productoModify.html', daten)




#::::::::::::::: PRODUKTKORB :::::::::::::::::::::

def agregar_producto(request, id):
    try:
        produkt = Producto.objects.get(id=id)  # Obtiene el producto
        produktbestand = int(produkt.stock)  # Stock del producto
        vz = int(request.POST.get('cantidad', 1))  # Cantidad solicitada

        if vz <= 0:  # Validación de cantidad positiva
            messages.add_message(request=request, level=messages.ERROR, message="Cantidad inválida")
        elif produktbestand <= 0:  # Sin stock disponible
            messages.add_message(request=request, level=messages.ERROR, message="No hay stock disponible")
        elif vz > produktbestand:  # Cantidad solicitada mayor al stock
            messages.add_message(request=request, level=messages.ERROR, message="Cantidad solicitada supera el stock disponible")
        else:
            print()
            print()
            print()
            print("Producto: ",produkt)
            print()
            print("ELSE: llamando a punto a .agregar")
            print()
            Carrito(request).agregar(produkt)  # Agrega el producto al carrito
            messages.add_message(request=request, level=messages.SUCCESS, message="Producto agregado al carrito")
        total_cantidad = Carrito(request).contar_cantidad_total()
        print(f"Cantidad total en el carrito: {total_cantidad}") 
    except Producto.DoesNotExist:
        messages.add_message(request=request, level=messages.ERROR, message="Producto no encontrado")
    except ValueError:
        messages.add_message(request=request, level=messages.ERROR, message="Cantidad inválida")
    except Exception as e:
        messages.add_message(request=request, level=messages.ERROR, message=f"Error: {str(e)}")
    # Redirección
    referer = request.META.get('HTTP_REFERER', 'products')
    return redirect(referer)

def eliminar_producto(request, id):
    carrito_compra=Carrito(request)
    produkt=Producto.objects.get(id=id) 
    print(f"::::::::::::::::::::{produkt}")
    carrito_compra.eliminar(produkt)
    messages.add_message(request=request,level=messages.SUCCESS, message="Produkt gelöscht")
    return redirect('carrito2')

def restar_producto(request, id):
    carrito_compra=Carrito(request)
    produkt=Producto.objects.get(id=id)
    carrito_compra.restar(produkt)
    messages.add_message(request=request,level=messages.SUCCESS, message="Produkt ausgeschlossen")
    return redirect('carrito2')

def limpiar_producto(request):
    carrito_compra=Carrito(request)
    carrito_compra.limpiar()
    messages.add_message(request=request,level=messages.SUCCESS, message="El carrito ha sido vaciado")
    return redirect('products')

#::::::::::::::: PRECOMPRA :::::::::::::::::::::

def preview(request):
    if not request.user.is_authenticated:
        print('------USER IS NOT AUTHENTICATED------')
        return redirect('carrito')

    direcciones = Direccion.objects.filter(idUser=request.user)

    if request.method=='POST':
        direccion_id = request.POST.get('direccion_id')

        if not direccion_id:
            messages.error(request, "Debes seleccionar una dirección.")
            return redirect('preview')
        
        carrito = request.session.get('carrito',{})
        cant=sum(int(value['cantidad']) for value in carrito.values())
        total = sum(int(value['precio']) * int(value['cantidad']) for value in carrito.values())

        direccion = get_object_or_404(Direccion, id=direccion_id, idUser=request.user)

        preview = Preview.objects.create(
            idUser=request.user,
            name=request.user.username,
            cantidad=cant,
            total=total,
            idDireccion=direccion
        )
        preview.save()
        print()
        print(f"Preview Creada: {preview.id}")
        print()
        return redirect('detallecarrito', id=preview.id)
    
    return render(request,'preview.html', {'direcciones': direcciones})

def detallecarrito(request,id):
    print("------ ",id," ------")
    preview = get_object_or_404(Preview, id=id)
    return render(request,'detallecarrito.html', {'preview': preview})

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def base(request):
    return render(request,'base.html')

def index(request):
    if request.method=='POST':

        messages.add_message(reques=request,level=messages.SUCCESS,message="Producto creado con éxito")
        return redirect('index')
    return render(request,'index.html')

def obras(request):
    obras = Obra.objects.all()     #similar a select * from Vehiculo
    return render(request, 'obras.html', {'obras':obras})

def nosotros(request):
    return render(request,'nosotros.html')

def modificar(request, id):
    obra = Obra.objects.get(idObra=id) # buscara el objeto con la id enviada
    daten={'fillMe': obraForm(instance=obra), 'obra':obra} 
        # rellenamos 'datos' con un formulario de tipo 'obraForm' con los datos "obra" de la linea anterior, en el otro parametro creamos otro objeto 'obra'
    if request.method=='POST':
        formulario = obraForm(request.POST, request.FILES, instance=obra)
        if formulario.is_valid():
            formulario.save()   #actualiza la info del objeto
            messages.add_message(reques=request,level=messages.SUCCESS,message="Producto creado con éxito")
            return redirect('editar')
    return render(request, 'modificar.html', daten)

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def profile(request):
    return render(request,'profile.html')

def profileMod(request):
    if request.method == 'POST':
        fill= EditarPerfil(request.POST, request.FILES, instance=request.user)
        if fill.is_valid():
            fill.save()
            messages.add_message(request=request,level=messages.SUCCESS, message="Perfil actualizado correctamente.")
            return redirect('profile')
        else:
            messages.add_message(request=request,level=messages.SUCCESS, message="Error al actualizar el perfil.")
    else:
        fill = EditarPerfil(instance=request.user)
    
    return render(request, 'profileMod.html', {'form': fill})

def profileWatch(request, id):
    usuario = get_object_or_404(CustomUser, id=id)
    return render(request,'profileWatch.html', {'usuario':usuario})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def eliminar(request, id):
    prod = get_object_or_404(Producto,id=id)
    if request.method=='POST':
        if 'elimina' in request.POST:   # boton que elimnina
            prod.delete() # elimina el objeto despues de confirmar
            return redirect('editar')
        else:
            return redirect ('editar')
    return render (request, 'eliminar.html',{'prod':prod})

def cerrar(request):
    logout(request)
    return redirect('index')

def signup(request):
    data={'form':RegistroUserForm()}
    if request.method=="POST":
        formulario = RegistroUserForm(data=request.POST,files=request.FILES)
        if formulario.is_valid():
            user = formulario.save()
            user.refresh_from_db()  # Esto asegura que el perfil de usuario sea actualizado con los datos adicionales
            user.pic = formulario.cleaned_data.get('pic')
            user.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            if user is not None:
                login(request, user)
                messages.success(request, "Sesión iniciada con éxito")
                return redirect('index')
        else:
            print(formulario.errors)
            
        data['form']=formulario
    return render(request, "registration/signup.html", data)


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def address(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.idUser = request.user
            form.save()
            messages.success(request, "Adresse hinzugefügt")
            return redirect('addresses')
        else:
            messages.error(request, "Adresse wurde nicht hinzugefügt")
            return redirect('address')
    else:
        form = DireccionForm()
    return render(request, 'address.html', {'form': form})

def addresses(request):
    userr = request.user
    addresses = Direccion.objects.filter(idUser=userr).order_by('-id')

    return render(request, 'addresses.html', {'addresses': addresses})

def addressMod(request, id):
    address = get_object_or_404(Direccion, id=id)
    daten={'fillMe': DireccionForm(instance=address), 'address':address}

    if request.method=='POST':
        form = DireccionForm(request.POST, request.FILES, instance=address)
        if form.is_valid():
            form.save()
            messages.add_message(request=request,level=messages.SUCCESS,message="Adresse elfolgreigt bearbeitet")
            return redirect('addresses')
        else:
            messages.error(request, "Adresse Fehler")
        
    return render(request, 'addressMod.html', daten)

#::::::::::::::::::::::::::::::::::::::::::::::
#:::::::::::::::::::CARRITO::::::::::::::::::::

def carrito(request):
    return render(request,'carrito.html')

def carrito2(request):
    print(request.session.get('carrito', {}))   
    return render(request,'carrito2.html')






#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::







webpay = settings.WEBPAY
afterkey = settings.AFTERKEY

transaction = Transaction.build_for_integration(
    commerce_code='597055555532',
    api_key=webpay
)

def pagoIniciar(request, id):
    preview = get_object_or_404(Preview, id=id)
    total = preview.total

    transaccion = transaction
    response = transaccion.create(
        buy_order=str(preview.id),
        session_id=str(request.user.id),
        amount=total,
        return_url=request.build_absolute_uri('/pagoExito/'),
    )
    request.session['webpay_token'] = response['token']

    return redirect(response['url'] + '?token_ws=' + response['token'])


def pagoExito(request):
    try:
        token = request.GET.get('token_ws') 
        transaccion = transaction
        print()
        print("dentro de pagoExito")
        print()

        response = transaccion.commit(token)

        if response['status'] == 'AUTHORIZED':
            
            print()
            print("status autorizado")
            print()
            carrito = request.session.get('carrito',{})
            
            preview_id = response['buy_order']
            preview = get_object_or_404(Preview, id=preview_id)
            
            boleta = Boleta.objects.create(
                usuario=preview.idUser,
                total=preview.total,
                complete=True,
                idDireccion=preview.idDireccion,
            )
            boleta.save()
            print(f"Boleta Creada: {boleta.id}")
            print()
            
            for key, value in carrito.items():
                print(f"key: {key}")
                print()
                producto_id = value['producto_id']
                quantity = int(value['cantidad'])
                tPerItem= int(value['precio']) * int(value['cantidad'])
                produkt = Producto.objects.get(id=producto_id)
                
                boletaDet = BoletaDetalle.objects.create(
                    idBoleta=boleta, 
                    idProducto=produkt,
                    nombre = value['nombre'],
                    cantidad = quantity,
                    totalPorItem = tPerItem,
                )

                if produkt.stock >= quantity:
                    produkt.stock -= quantity
                    produkt.save()
                    print(f"Stock actualizado para {produkt.nombre}: {produkt.stock}")
                else:
                    print(f"Error: Stock insuficiente para {produkt.nombre}")
                    messages.error(request, f"Stock insuficiente para {produkt.nombre}")
                    return redirect('carrito')
                boletaDet.save()
                print()
                print(f"BoletaDetalle Creada: {boletaDet.id}")
                print()
            print()
            print("Generando Compra...")
            print()
            compra = Compra.objects.create(
                idBoleta=boleta,
                cantidad=preview.cantidad,
                total=preview.total,
                estado='Pagado',
            )
            compra.save()
            print(f"Compra Creada: {compra.id}")
            print()

            user_email = request.user.email
            subject = "Pago realizado"
            message = (
                f"Hola {request.user.first_name or request.user.username},\n\n"
                f"Tu pago fue procesado correctamente.\n"
                f"ID de compra: {compra.id}\n"
                f"Monto: ${compra.total}\n"
                f"Total de items: {compra.cantidad}\n"
                f"Estado de pago: {response['status']}\n"
                f"Fecha: {compra.idBoleta.fecha}\n\n"
                "Gracias por comprar en Ferremas.\n\n\n"
                f"Tarjeta: {response.get('card_detail', 'No disponible')}\n"
                f"Tipo de pago: {response.get('payment_type_code', 'No disponible')}\n"
            )
            send_mail(
                subject,
                message,
                None,
                [user_email],
                fail_silently=False,
            )

            request.session['carrito'] = {}
            request.session.modified = True
            preview.delete() 

            return render(request, 'pagoExito.html', {'compra': compra, 'response': response})
        else:
            return render(request, 'pagoError.html', {'response': response})

    except Exception as e:
        print()
        print("error")
        print(f"Puede que hayas recargado la página: {e}")
        print()
        return render(request, 'index.html')
        

def pagoError(request):
    token = request.GET.get('token_ws')
    transaccion = transaction
    print()
    print("dentro de pagoError")
    print()
    
    response = transaccion.commit(token)
    print(f"Respuesta de Webpay: {response}")
    preview_id = response['buy_order']
    preview = get_object_or_404(Preview, id=preview_id)
    preview.delete()
    
    user_email = request.user.email
    subject = "Pago no procesado"
    message = (
        f"Hola {request.user.first_name or request.user.username},\n\n"
        f"Tu pago no pudo ser procesado.\n"
        "Gracias por preferir Ferremas.\n\n\n"
    )
    send_mail(
        subject,
        message,
        None,
        [user_email],
        fail_silently=False,
    )
    try:
        status = response.get('status', 'No disponible')
        buy_order = response.get('buy_order', 'No disponible')
        amount = response.get('amount', 'No disponible')
        error_message = response.get('error_message', 'No se proporcionó un mensaje de error')

        return render(request, 'pagoError.html', {
            'status': status,
            'buy_order': buy_order,
            'amount': amount,
            'error_message': error_message,
        })
    except Exception as e:
        print(f"Error al confirmar la transacción: {e}")
        return render(request, 'pagoError.html', {
            'status': 'Error desconocido',
            'buy_order': 'No disponible',
            'amount': 'No disponible',
            'error_message': str(e),
        })





#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def miscompras(request):
    print()
    print("Entrando a miscompras...")
    print()
    if request.user.is_authenticated:
        customer = request.user
        compras = Compra.objects.filter(idBoleta__usuario=customer).order_by('-id') # Filtra las compras del usuario autenticado
    else:
        messages.error(request, "Debes iniciar sesión para ver tus compras.")
        return redirect('login')  # Redirige al login si el usuario no está autenticado
    return render(request,'miscompras.html', {'compras':compras})

def vercompra(request, id):
    print()
    print("Entrando a ver compra...")
    print()
    if request.user.is_authenticated:
        customer = request.user
        compra = get_object_or_404(Compra, id=id)
        print(f"ID de compra: {compra.id}")
        print()
        boleta = get_object_or_404(Boleta, id=compra.idBoleta.id)
        productos = BoletaDetalle.objects.filter(idBoleta=boleta) # Filtra los productos de la boleta
        print()
        print()
    else:
        messages.error(request, "Debes iniciar sesión para ver tus compras.")
        return redirect('login')
    return render(request, 'vercompra.html', {
    'compra': compra,
    'boleta': boleta,
    'productos': productos
    })

def vercompras(request):
    print()
    print("Entrando a compras...")
    print()
    if request.user.is_authenticated:
        if request.user.tipo == 'vendedor' or request.user.tipo == 'contador' or request.user.is_superuser:
            compras = Compra.objects.all()
            purchases = []  # Array para almacenar los datos de compra y usuario
            for compra in compras:
                    boleta = compra.idBoleta
                    if boleta and boleta.usuario:
                        purchases.append({
                            'compra': compra,
                            'user_id': boleta.usuario.id  # Obtiene el id del usuario desde la boleta
                        })
                    else:
                        print()
                        print(f"Boleta o usuario no encontrado para la compra: {compra.id}")
    else:
        messages.error(request, "Privileges are needed")
        return redirect('login')
    
    return render(request,'vercompras.html', {'purchases':purchases})



def pedidoCrear(request, id):
    compra = get_object_or_404(Compra, id=id)
    user = get_object_or_404(CustomUser, id=compra.idBoleta.usuario.id)
    direccion = get_object_or_404(Direccion, id=compra.idBoleta.idDireccion.id)
    initial_data = {
        'estado': 'pendiente',
        'idDireccion':direccion,
    }
    formulario = pedidoForm(initial=initial_data)

    if request.method == 'POST':
        formulario = pedidoForm(request.POST)
        if formulario.is_valid():
            pedido = formulario.save(commit=False)
            pedido.idCompra = compra
            pedido.idUser = user
            pedido.estado = 'pendiente'
            pedido.idDireccion = direccion
            pedido.save()
            compra.created = True
            compra.save()
            print()
            print("Pedido creado con éxito.")
            messages.success(request, "Pedido creado con éxito")
            return redirect('pedidos')
        else:
            print()
            print("Errores en el formulario:", formulario.errors)
    else:
        print("No se ha enviado el formulario")

    # Renderiza el formulario con los datos precargados
    return render(request, 'pedidoCrear.html', {'form': formulario, 'idCompra':compra.id, 'idUser': user,'estado': 'pendiente'})




def pedidos(request):
    if request.user.is_authenticated:
        if request.user.tipo == 'vendedor' or request.user.tipo == 'bodeguero' or request.user.tipo == 'administrador' or request.user.is_superuser:
            pedidos = Pedido.objects.all()
        else:
            messages.error(request, "Privileges are needed")
            return redirect('login')
    return render(request,'pedidos.html', {'pedidos':pedidos})

def pedidoVer(request, id):
    if request.user.is_authenticated:
        pedido = get_object_or_404(Pedido, id=id)
        compra = get_object_or_404(Compra, id=pedido.idCompra.id)
        print(f"ID de compra: {compra.id}")
        print()
        boleta = get_object_or_404(Boleta, id=compra.idBoleta.id)
        productos = BoletaDetalle.objects.filter(idBoleta=boleta) # Filtra los productos de la boleta
        print()
        print()
    else:
        messages.error(request, "Debes iniciar sesión")
        return redirect('login')  # Redirige al login si el usuario no está autenticado
    return render(request, 'pedidoVer.html', {
    'compra': compra,
    'boleta': boleta,
    'pedido': pedido,
    'productos': productos
    })



def paqueteCrear(request, id):
    if request.user.is_authenticated:
        try:
            customer = request.user
            pedido = get_object_or_404(Pedido, id=id)
            print()
            print(f"ID de compra: {pedido.id}")
            print("Dirección asociada:", pedido.idDireccion)
            if pedido.idDireccion:
                print("Nombre dirección:", pedido.idDireccion.name)
            print()
            initial_data = {
                    'idPedido':pedido.id,
                }
            form = PaqueteForm(initial=initial_data)

            if request.method == 'POST':
                form = PaqueteForm(request.POST)
                if form.is_valid():
                    paquete = form.save(commit=False)
                    paquete.idPedido = pedido
                    paquete.estado = 'pendiente'
                    paquete.save()
                    print()
                    print("Paquete creado con éxito")
                    messages.success(request, "Paquete creado con éxito")
                    return redirect('despacho', id=paquete.id)
            return render(request,'paqueteCrear.html',{'form':form,'pedido': pedido})
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "Ocurrió un error al crear el paquete.")
            return redirect('index')
    else:
        messages.error(request, "Faltan privilegios")
        return redirect('login')


def despacho(request, id):
    try:
        paquete = Paquete.objects.get(id=id)
    except Paquete.DoesNotExist:
        raise Http404("Paquete no encontrado")
    
    pedido = get_object_or_404(Pedido, id=paquete.idPedido.id)
    compra = get_object_or_404(Compra, id=pedido.idCompra.id)
    usuario = compra.idBoleta.usuario
    email = usuario.email
    if not pedido.idDireccion:
        raise Http404("Dirección no encontrada")
    else:
        direccion = pedido.idDireccion
    print()
    print("Entrando a creacion de shipping")
    try:
        
        AFTERSHIP_KEY=afterkey
        tracking_number=f"STK-{paquete.id:06d}"
        order_promised_delivery_date = (datetime.datetime.now() + datetime.timedelta(weeks=2)).strftime('%Y-%m-%d')

        headers = {
            "aftership-api-key": AFTERSHIP_KEY,
            "Content-Type": "application/json"
        }
        print()
        print("Headers erstellt")
        data = {
            "tracking": {
                "tracking_number": tracking_number,
                "slug": "starken",
                "title": str(paquete.id),
                "emails": [email],
                "order_id": str(pedido.id),
                "order_promised_delivery_date": order_promised_delivery_date
            }
        }
        print()
        print("Data erstellt")
        response = requests.post(
            "https://api.aftership.com/v4/trackings",
            headers=headers,
            json=data
        )
        print()
        print("responce erstellt")
        result = response.json()
        print()
        print("result erstellt")
        
        if response.status_code == 201:
            print()
            print("responce.status_code richtig")
            messages.success(request, "Tracking registrado en AfterShip.")
            pedido.estado = 'enviado'
            pedido.sent = True
            pedido.save()

            subject = f"Paquete {compra.id} en camino"
            message = (
                f"Hola {usuario.first_name or usuario.username},\n\n"
                f"Tu paquete está en camino.\n"
                f"ID de compra: {compra.id}\n"
                f"Total de items: {compra.cantidad}\n"
                f"Fecha: {compra.idBoleta.fecha}\n\n"
                f"Número de seguimiento: {tracking_number}\n"
                f"Courier: https://www.starken.cl/seguimiento\n\n"
                "Gracias por preferir Ferremas.\n\n\n"
            )
            send_mail(
                subject,
                message,
                None,
                [email],
                fail_silently=False,
            )


            request.session['aftership_result'] = result
            return redirect('despacho_exito')
        else:
            messages.error(request, f"Error AfterShip: {result}")
            return render(request, 'despacho_Error.html')

    except Exception as e:
        paquete.delete()
        print()
        print("Error AfterShip:", e)
        return render(request, "despacho_error.html", {"error": str(e)})
    


def despacho_exito(request):
    aftership_result = request.session.pop('aftership_result', None)

    
    return render(request, 'despacho_exito.html', {'aftership_result': aftership_result})


def despacho_error(request):

    return render(request, 'despacho_error')



def ventas(request):
    if request.user.is_authenticated:
        if request.user.tipo == 'contador' or request.user.tipo == 'administrador' or request.user.is_superuser:
            compras = Compra.objects.all()
            purchases = []  # Array para almacenar los datos de compra y usuario
            for compra in compras:
                    boleta = compra.idBoleta
                    if boleta and boleta.usuario:
                        purchases.append({
                            'compra': compra,
                            'user_id': boleta.usuario.id  # Obtiene el id del usuario desde la boleta
                        })
                    else:
                        print()
                        print(f"Boleta o usuario no encontrado para la compra: {compra.id}")
    else:
        messages.error(request, "Privileges are needed")
        return redirect('login')
    return render(request,'ventas.html', {'purchases':purchases})



#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def gasto_crear(request):
    form=GastoForm()

    if request.method=='POST':
        form = GastoForm(request.POST, request.FILES)
        if form.is_valid():
            informe = form.save(commit=False)  
            informe.save()
            messages.add_message(request=request,level=messages.SUCCESS,message="Gasto creado con éxito")
            return redirect('gastos')

    return render(request,'gasto_crear.html', {'form':form})

def gastos(request):
    gastos = Gasto.objects.all()
    return render(request, 'gastos.html', {'gastos':gastos})

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
def informe_m_crear(request):
    user=request.user
    form=InformeMensualForm()    
    bal=BalanceMensual.objects.latest('fecha')
    if request.method=='POST':
        form = InformeMensualForm(request.POST, request.FILES)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.idUser = user  
            informe.save()
            messages.add_message(request=request,level=messages.SUCCESS,message="Informe mensual creado")
            return redirect('informe_m')

    return render(request,'informe_m_crear.html', {'form':form, 'bal': bal})

def informe_m(request):
    informes = InformeMensual.objects.all()
    return render(request, 'informe_m.html', {'informes': informes})

def informe_md(request, id):
    if request.user.is_authenticated:
        informe = get_object_or_404(InformeMensual, id=id)
    else:
        messages.error(request, "Debes iniciar sesión")
        return redirect('login')
    return render(request, 'informe_md.html', {'informe': informe})





def informe_d_crear(request):
    user=request.user
    form=InformeDesempForm()

    if request.method=='POST':
        form = InformeDesempForm(request.POST, request.FILES)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.idUser = user  
            informe.save()
            messages.add_message(request=request,level=messages.SUCCESS,message="Informe creado con éxito")
            return redirect('informe_d')

    return render(request,'informe_d_crear.html', {'user':user, 'form':form})


def informe_d(request):
    informes = InformeDesemp.objects.all()
    return render(request, 'informe_d.html', {'informes': informes})


def informe_dd(request, id):
    if request.user.is_authenticated:
        informe = get_object_or_404(InformeDesemp, id=id)
    else:
        messages.error(request, "Debes iniciar sesión para ver tus compras.")
        return redirect('index')
    return render(request, 'informe_dd.html', {'informe': informe})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def balmensual(request):
    form=BalanceMensual()

    gastos=Gasto.objects.all()
    totalgastos=0
    
    for gs in gastos:
        totalgastos += gs.total

    if request.method == 'POST':
        bal = BalanceMensualForm(request.POST)
        if bal.is_valid():
            balance = bal.save(commit=False)

            now = datetime.datetime.now()
            compras_mes_actual = Compra.objects.filter(
                fecha__year=now.year, fecha__month=now.month
            )
            totalll = 0
            for compra in compras_mes_actual:
                totalll += compra.total

            balance.totalVentas = totalll
            balance.gastos = totalgastos
            balance.BalanceMensual=(totalll-totalgastos)

            balance.save()
            messages.success(request, "Balance mensual creado con éxito")
            return redirect('balances')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        form = BalanceMensualForm()

    return render(request, 'balmensual.html', {'form': form, 'totalgastos':totalgastos})




def balances(request):
    if request.user.is_authenticated:
        if request.user.tipo == 'contador' or request.user.is_superuser:
            balances = BalanceMensual.objects.all()
        else:
            messages.error(request, "Privileges are needed")
            return redirect('index')
    return render(request,'balances.html', {'balances':balances})



def balance(request, id):
    if request.user.is_authenticated:
        balance = get_object_or_404(BalanceMensual, id=id)
    else:
        messages.error(request, "Debes iniciar sesión para ver tus compras.")
        return redirect('index')
    return render(request, 'balance.html', {'bal':balance})


#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

def change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene la sesión activa después del cambio
            messages.success(request, 'Contraseña actualizada.')
            return redirect('profile')  # Redirige a la página de perfil o donde desees
        else:
            messages.error(request, 'Corrige los errores.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'pwChange.html', {'form': form})

def generarBoleta(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            carrito = request.session.get('carrito',{})
            total = sum(int(value['precio']) * int(value['cantidad']) for value in carrito.values())

            boleta = Boleta.objects.create(
                usuario=request.user,
                total=total,
                complete=False,
            )
            return redirect('detallecarrito', id=boleta.id) #gracias a que puse 'id' y no 'boleta_id', funciono
        else:
            print('------USER IS NOT AUTHENTICATED------')
    return redirect('carrito')

#::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::