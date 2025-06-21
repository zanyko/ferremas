from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Categoria)
admin.site.register(Obra)
admin.site.register(TipoUser)
admin.site.register(Producto)#producto en general
admin.site.register(Preview)
admin.site.register(Boleta)#generado al aprobar compra de cliente
admin.site.register(BoletaItem)
admin.site.register(BoletaDetalle)#
admin.site.register(Compra)#generado a partir de boleta
admin.site.register(Pedido)#pedidos realizados por vendedor
admin.site.register(Venta)#realizado por contador
admin.site.register(BalanceMensual)#realizado por contador
admin.site.register(InformeMensual)#realizado por admin
admin.site.register(InformeDesemp)#realizado por admin
admin.site.register(Sucursal)
admin.site.register(Direccion)
admin.site.register(Paquete)
admin.site.register(Gasto)