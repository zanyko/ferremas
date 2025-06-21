from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"), # path del index, debe ser un path por cada def
    path('base/', views.base,name="base"),
    path('obras/', views.obras,name="obras"),
    path('buscar/', views.buscar,name="buscar"),
    path('editar/', views.editar,name="editar"),
    path('crear/', views.crear,name="crear"),
    path('nosotros/', views.nosotros,name="nosotros"),
    path('carrito/', views.carrito,name="carrito"),
    path('carrito2/', views.carrito2,name="carrito2"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    path('products/', views.products,name="products"),
    path('productoCrear/', views.productoCrear,name="productoCrear"),
    path('productoModify/<id>', views.productoModify,name="productoModify"),

    path('agregar/<int:id>',views.agregar_producto,name="Add"),
    path('eliminar/<int:id>',views.eliminar_producto,name="Del"),
    path('restar/<int:id>',views.restar_producto,name="Sub"),
    path('limpiar/',views.limpiar_producto,name="CLS"),
    
    path('preview/',views.preview,name="preview"),
    path('detallecarrito/<int:id>/', views.detallecarrito,name="detallecarrito"),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('login/', views.login, name='login'),
    path('signup/', views.signup,name="signup"),
    path('logout/', views.cerrar,name="cerrar"),
    path('usuarios/', views.usuarios,name="usuarios"),
    path('pwChange/', views.change,name='change'),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('profile/', views.profile,name="profile"),
    path('profileMod/', views.profileMod,name="profileMod"),
    path('profileWatch/<id>', views.profileWatch,name="profileWatch"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('admire/<id>/', views.admire,name="admire"),
    path('modificar/<id>/',views.modificar,name="modificar"),
    path('eliminar/<id>/',views.eliminar,name="eliminar"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('generarBoleta/', views.generarBoleta,name="generarBoleta"),
    path('miscompras', views.miscompras,name="miscompras"),
    path('vercompra/<int:id>/', views.vercompra,name="vercompra"),
    path('vercompras/', views.vercompras,name="vercompras"),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::

    path('inventario/', views.inventario,name="inventario"),
    path('pedidoCrear/<int:id>/', views.pedidoCrear,name="pedidoCrear"),
    path('pedidos/', views.pedidos,name="pedidos"),
    path('pedidoVer/<int:id>', views.pedidoVer,name="pedidoVer"),
    
    path('paqueteCrear/<int:id>/', views.paqueteCrear,name="paqueteCrear"),
    
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    path('pagoIniciar/<int:id>/', views.pagoIniciar, name='pagoIniciar'),
    path('pagoExito/', views.pagoExito, name='pagoExito'),
    path('pagoError/', views.pagoError, name='pagoError'),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    path('address/', views.address,name="address"),
    path('addresses/', views.addresses,name="addresses"),
    path('addressMod/<int:id>/', views.addressMod,name="addressMod"),
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::

    path('despacho/<int:id>', views.despacho, name='despacho'),
    path('despacho_exito/', views.despacho_exito, name='despacho_exito'),
    path('despacho_error/', views.despacho_error, name='despacho_error'),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    path('api/enviar-correo/', views.enviar_correo_usuario, name='enviar_correo_usuario'),

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::

    path('gasto_crear', views.gasto_crear, name='gasto_crear'),
    path('gastos', views.gastos, name='gastos'),

    path('informe_m_crear', views.informe_m_crear, name='informe_m_crear'),
    path('informe_m', views.informe_m, name='informe_m'),
    path('informe_md/<int:id>/', views.informe_md, name='informe_md'),
    
    path('informe_d_crear', views.informe_d_crear, name='informe_d_crear'),
    path('informe_d', views.informe_d, name='informe_d'),
    path('informe_dd/<int:id>/', views.informe_dd, name='informe_dd'),
    
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::

    path('ventas/', views.ventas,name="ventas"),
    path('balmensual/', views.balmensual,name="balmensual"),
    path('balances/', views.balances,name="balances"),
    path('balance/<int:id>/', views.balance,name="balance"),
]
