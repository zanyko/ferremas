from django.db import models
import datetime
from django.contrib.auth.models import User, AbstractUser


#::::::::::::::::::::::::::::::::::::::::::::::
#:::::: AQUI VAN LOS MODELOS (TABLAS) :::::::::
#::::::::::::::::::::::::::::::::::::::::::::::

class CustomUser(AbstractUser):
    pic = models.ImageField(upload_to='profile_pics', null=True, blank=True, default='profile_pics/default.png')
    is_staff=models.BooleanField(default=False)
    tipo = models.CharField(max_length=20,
        choices=(
            ('cliente', 'Cliente'),
            ('vendedor', 'Vendedor'),
            ('bodeguero', 'Bodeguero'),
            ('contador', 'Contador'),
            ('administrador', 'Administrador'),
        ),default='Cliente',verbose_name='Tipo')
    bio = models.TextField(verbose_name='biografia', default='', null=True, blank=True)

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='idCategoria')
    nombreCategoria= models.CharField(max_length=40, verbose_name='nombreCategoria')

    def __str__(self):
        return f" {self.idCategoria} - {self.nombreCategoria}"

class Obra(models.Model):
    idObra=models.CharField(max_length=5, primary_key=True, verbose_name='id Arbeit')
    nombre=models.CharField(max_length=30, verbose_name='Name der Arbeit')
    descripcion=models.CharField(max_length=255, verbose_name='Description')
    autor=models.CharField(max_length=99, verbose_name='Name des Autors')
    anio=models.CharField(max_length=4, verbose_name='Jahr der Arbeit')
    stock=models.IntegerField(verbose_name='Stock')
    categoria=models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name='Kategorie')
    imagen=models.ImageField(upload_to="imagenes", null=True, verbose_name='Fotografie')
    precio=models.IntegerField(blank=True,null=True,verbose_name='Precio')

    def __str__(self):
        return f"{self.idObra} - {self.nombre}"

class TipoUser(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='idTipoUser')
    nombreTipoUser= models.CharField(max_length=15, verbose_name='nombreTipoUser')

    def __str__(self):
        return f"{self.id} - {self.nombreTipoUser}"
    
class Producto(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idProducto')
    nombre=models.CharField(max_length=50, verbose_name='Name der Arbeit')
    descripcion = models.TextField(verbose_name='Description', null=True, blank=True)
    marca=models.CharField(max_length=99, verbose_name='Markenname')
    anio=models.CharField(max_length=4, verbose_name='Jahr der Produkt')
    stock=models.IntegerField(verbose_name='Stock')
    categoria=models.ForeignKey('Categoria', on_delete=models.CASCADE, verbose_name='Kategorie')
    imagen=models.ImageField(upload_to="imagenes", null=True, verbose_name='Fotografie')
    precio=models.IntegerField(blank=True,null=True,verbose_name='Precio')
    estado=models.CharField(max_length=20, default='disponible', choices=(('disponible', 'disponible'), ('no disponible', 'no disponible')), verbose_name='Estado')
    ubicacion=models.CharField(max_length=255, null=True, blank=True, verbose_name='Ubicacion')

    def __str__(self):
        return f"{self.id} | {self.nombre} | {self.marca} | {self.categoria} | ${self.precio} | {self.estado} | {self.stock}"

class Direccion(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    idUser = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idUser')
    name = models.CharField(max_length=20, null=True, blank=True, verbose_name='Nombre')
    street = models.CharField(max_length=40, null=True, blank=True, verbose_name='Calle')
    city = models.CharField(max_length=40, null=True, blank=True, verbose_name='Ciudad')
    state = models.CharField(max_length=40, null=True, blank=True, verbose_name='Region')
    zipcode = models.CharField(max_length=40, null=True, blank=True, verbose_name='Codigo Postal')
    country = models.CharField(max_length=40, null=True, blank=True, verbose_name='Pais')
    phone = models.CharField(max_length=40, null=True, blank=True, verbose_name='Numero')

    def __str__(self):
        return f"{self.id} | {self.idUser} | {self.name} | {self.street} | {self.city} | {self.state} | {self.zipcode} | {self.country} | {self.phone} "

class Preview(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idPreview')
    idUser=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idUserr')
    name=models.CharField(max_length=50, null=False, default='no user', verbose_name='name')
    cantidad=models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='Cantidad')
    total=models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='Total')
    idDireccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idDireccion')

    def __str__(self):
        return f"{self.id} | {self.idUser} | {self.name} | {self.cantidad} | {self.total} | {self.idDireccion}"

class Boleta(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='id')
    usuario=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idUsuario')
    total=models.IntegerField(default=0, null=True, blank=True, editable=False)
    complete=models.BooleanField(default=True, null=False, blank=False, verbose_name='Complete')
    fecha=models.DateTimeField(auto_now_add=True, verbose_name='Fecha')
    idDireccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idDireccion')

    def __str__(self):
        return f"<{self.id}> | {self.usuario} | {self.complete} | {self.fecha} | ${self.total} | {self.idDireccion}"

class BoletaItem(models.Model):
    product = models.ForeignKey(Obra, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    boleta = models.ForeignKey(Boleta, on_delete=models.SET_NULL, blank=True, null=True, editable=False)
    cantidad = models.IntegerField(default=0, null=True, blank=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.boleta} | {self.product} | {self.cantidad} | {self.fecha}"

class BoletaDetalle(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idBoletaDetalle')
    idBoleta = models.ForeignKey(Boleta, on_delete=models.SET_NULL, blank=False, null=True, editable=False, verbose_name='idBoleta')
    idProducto = models.ForeignKey(Producto, on_delete=models.SET_NULL, blank=False, null=True, editable=False, verbose_name='idProducto')
    nombre = models.CharField(max_length=50, null=False, default='no user', verbose_name='Nombre')
    cantidad = models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='Cantidad')
    totalPorItem = models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='TotalPorItem')
    
    def __str__(self):
        return f"{self.id} | {self.idBoleta} | {self.nombre} | {self.cantidad} | {self.totalPorItem}"

class Compra(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idCompras')
    idBoleta=models.ForeignKey(Boleta, on_delete=models.SET_NULL, blank=True, null=True, editable=True, verbose_name='idBoleta')
    cantidad=models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='Cantidad')
    total = models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='Total')
    estado = models.CharField(max_length=20, default='Pagado', verbose_name='Estado')
    fecha = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Fecha')
    created = models.BooleanField(default=False, verbose_name='created')
    
    def __str__(self):
        return f"{self.id} | {self.idBoleta} | {self.estado} | {self.cantidad} | ${self.total} | {self.fecha} | {self.created}"

class Pedido(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idPedido')
    idCompra=models.ForeignKey(Compra, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idCompra')
    idUser=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idUsuario')
    estado=models.CharField(max_length=20, default='pendiente', choices=(('pendiente', 'pendiente'), ('enviado', 'enviado'), ('entregado', 'entregado')), verbose_name='Estado')
    fecha=models.DateTimeField(auto_now_add=True, null=False, verbose_name='Fecha')
    idDireccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idDireccion')
    sent = models.BooleanField(default=False, verbose_name='sent')
    
    def __str__(self):
        return f"{self.id} | {self.idCompra} | {self.idUser} | {self.estado} | {self.fecha} | {self.sent}"
    
#ventas: cuando se concreta el pedido
class Venta(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idVenta')
    idCompra=models.ForeignKey(Compra, blank=True, null=True, on_delete=models.SET_NULL, editable=False, verbose_name='idCompra')

    def __str__(self):
        return f"{self.id} | {self.idCompra}"   

class BalanceMensual(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idBalanceMensual')
    fecha=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha')
    totalVentas=models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='TotalVentas')
    gastos=models.IntegerField(default=0, null=True, blank=True, editable=True, verbose_name='Gastos')
    BalanceMensual=models.IntegerField(default=0, null=True, blank=True, editable=False, verbose_name='BalanceMensual')
    
    notas=models.TextField(verbose_name='Notas', null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.fecha} | ${self.BalanceMensual} | ${self.totalVentas} | ${self.gastos}"
    
class InformeMensual(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idInformeMensual')
    idUser=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=True, verbose_name='idUser')
    fecha=models.DateTimeField(auto_now_add=True, null=True, verbose_name='FechaInformeMensual')
    descripcion=models.TextField(verbose_name='Description', null=True, blank=True, editable=True)
    
    def __str__(self):
        return f"{self.id} | {self.idUser} | {self.fecha} | {self.descripcion}"

class InformeDesemp(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idInformeDesemp')
    idUser=models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True, editable=False, verbose_name='idUser')
    fecha=models.DateTimeField(auto_now_add=True, null=True, verbose_name='FechaInformeDesemp')
    descripcion=models.TextField(verbose_name='Description', null=True, blank=True)
    
    def __str__(self):
        return f"{self.id} | {self.idUser} | {self.fecha} | {self.descripcion}"

class Sucursal(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    name = models.CharField(max_length=40, default='', verbose_name='Nombre')
    address=models.CharField(max_length=255, null=True, blank=True, verbose_name='Direccion')

    def __str__(self):
        return f"{self.id} | {self.name} | {self.address}"

class Paquete(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='id')
    idPedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='idPedido')
    length = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Longitud')
    width = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Ancho')
    height = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Altura')
    weight = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='Peso')
    distance_unit = models.CharField(max_length=5, default='cm', verbose_name='Unidad de distancia')  # "in" o "cm"
    mass_unit = models.CharField(max_length=5, default='kg', verbose_name='Unidad de masa')           # "lb" o "kg"
    estado=models.CharField(max_length=20, default='pendiente', choices=(('entregado', 'Entregado'), ('pendiente', 'pendiente')), verbose_name='Estado')

    def __str__(self):
        return f"{self.id} | {self.idPedido} | {self.length} | {self.width} | {self.height} | {self.weight} | {self.distance_unit} | {self.mass_unit}"

class Gasto(models.Model):
    id=models.AutoField(primary_key=True, verbose_name='idGasto')
    total = models.IntegerField(null=True, blank=True, editable=True, verbose_name='Total')
    fecha = models.DateTimeField(auto_now_add=True, null=False, verbose_name='Fecha') 
    
    def __str__(self):
        return f"{self.id} | ${self.total} | {self.fecha}"

# para guardar los modelos hay que parar el server y hacer migraciones en la raiz del proyecto: 
# agregar "admin.site.register('modelo');" en admin.py
# py manage.py makemigrations
# py manage.py migrate