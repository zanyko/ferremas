def total_carrito(request):
    total=0
    if request.user.is_authenticated:
        try:
            carrito = request.session['carrito']
            if "carrito" in request.session:
                for key, value in carrito.items():
                    total+=(int(value["precio"]))*(value["cantidad"])
        except:
            total=0
    return {'total_carrito':int(total)}