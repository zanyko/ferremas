class Carrito:
    def __init__(self, request):
        self.request=request
        self.session=request.session
        carrito = self.session.get("carrito")
        if not carrito:
            self.session["carrito"]={}
            self.carrito=self.session["carrito"]
        else:
            self.carrito=carrito

    def contar_items(self):
        total_items = 0
        for item in self.carrito.values():
            total_items += item['cantidad']
        return total_items

    def contar_cantidad_total(self):
        """
        Cuenta la cantidad total de objetos en el carrito sumando la cantidad de cada ítem.
        """
        return sum(item['cantidad'] for item in self.carrito.values())

    def guardar(self):
        self.session["carrito"]=self.carrito
        self.session.modified=True

    def agregar(self, producto):
        print("--------------------")
        print("INSIDE AGREGAR")
        print("-------------------")
        id=str(producto.id)
        if id not in self.carrito.keys():
            print("--------------------")
            print("Produkt nicht im Warenkorb")
            print("")
            self.carrito[id]={
                "producto_id":id,
                "nombre":producto.nombre,
                "precio":producto.precio,
                "cantidad":1,
                "total":producto.precio,
            }
        else:
            print("--------------------")
            print("Produkt im Warenkorb")
            print("")
            for key,value in self.carrito.items():
                if key==id:
                    value["cantidad"]=value["cantidad"]+1
                    value["total"]=value["total"]+producto.precio
                    break
        self.guardar()
    

    def eliminar(self, producto):
        id = str(producto.id)
        print()
        print("Verificando...")
        print()
        for key, value in self.carrito.items():
            if value["producto_id"] == id:
                del self.carrito[key]
                print()
                print()
                print()
                print(f"::::::::::: {producto.nombre} wurde gelöscht :::::::::::")
                print()
                break
        self.guardar()
    
    def restar(self, producto):
        id=str(producto.id)
        for key, value in self.carrito.items():
            if key==id:
                value["cantidad"]=value["cantidad"]-1
                value["total"]=int(value["total"])-producto.precio
                print()
                print()
                print(f"::::::::::: {producto.nombre} wurde ausgeschlossen :::::::::::")
                print()
            if value["cantidad"]<1:
                self.eliminar(producto)
                print()
                print()
                print(f"::::::::::: {producto.nombre} wurde gelöscht :::::::::::")
                print()
            break
        self.guardar()
        
            

    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified=True