from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import *

class RegistroUserForm(UserCreationForm):
    pic = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    class Meta:
        model = CustomUser
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2', 'pic','bio')

class EditarPerfil(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'pic','bio')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Email',
            'pic': 'Imagen de Perfil',
            'bio': 'Biografía'
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese primer nombre',
                'id': 'first_name'
                }),
            'last_name': forms.TextInput(
                attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido',
                'id': 'last_name'
                }),
            'email': forms.EmailInput(
                attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese email',
                'id': 'email'
                }),
            'pic': forms.FileInput(
                attrs={
                'class': 'form-control', 
                'id': 'pic'
                }),
            'bio': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese biografía',
                    'rows': 4,
                }),
        }

class obraForm(forms.ModelForm):
    class Meta:
        model = Obra
        fields = ['idObra','nombre','descripcion','autor','anio','stock','categoria','imagen','precio']
        # cada field se compone de un 'label' y un 'widget'
        labels={
            'idObra':'ID',
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'autor':'Autor',
            'anio':'Año',
            'stock':'Stock',
            'categoria':'Categoria',
            'imagen':'Imagen',
            'precio':'Precio'
        }
        # tipo de etiqueta para los atributos:
        widgets={
            'idObra':forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese id de Obra',
                    'id' : 'idObra'
                }
            ),
            'nombre' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese nombre de Obra',
                    'id' : 'nombre'
                }
            ),
            'descripcion':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese breve descripcion',
                    'id':'descripcion'
                }
            ),
            'autor':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese nombre de Autor',
                    'id':'autor'
                }
            ),
            'anio':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese año de la obra',
                    'id':'anio'
                }
            ),
            'stock':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'precio'
                }
            ),
            # categoria es un select, es decir, una lista desplegable
            'categoria' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'id' : 'categoria'
                }
            ),
            'imagen' : forms.FileInput(
                attrs={
                    'class' : 'form-control',
                    'id' : 'imagen'
                }
            ),
            'precio':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'precio'
                }
            ),
        } # end widgets

class productForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre','descripcion','marca','anio','stock','categoria','imagen','precio','estado','ubicacion']
        # cada field se compone de un 'label' y un 'widget'
        labels={
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'marca':'Marca',
            'anio':'Año',
            'stock':'Stock',
            'categoria':'Categoria',
            'imagen':'Imagen',
            'precio':'Precio',
            'estado':'Estado',
            'ubicacion':'Ubicacion'
        }
        # tipo de etiqueta para los atributos:
        widgets={
            'nombre' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Ingrese nombre de Producto',
                    'id' : 'nombreproducto'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese una descripción detallada',
                    'rows': 4,
                }
            ),
            'marca':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese nombre de Marca',
                    'id':'idmarca'
                }
            ),
            'anio':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese año',
                    'id':'idanio'
                }
            ),
            'stock':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'idstock'
                }
            ),
            # categoria es un select, es decir, una lista desplegable
            'categoria' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'id' : 'categoria'
                }
            ),
            'imagen' : forms.FileInput(
                attrs={
                    'class' : 'form-control',
                    'id' : 'idimagen'
                }
            ),
            'precio':forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'id':'idprecio'
                }
            ),
            'estado' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'id' : 'idestado'
                }
            ),
            'ubicacion':forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese ubicacion',
                    'id':'idubicacion'
                }
            ),
            
        } # end widgets

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña actual'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nueva contraseña'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'})

class pedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']  # Excluye 'idUser'
        labels = {
            'estado': 'Estado',
        }
        widgets = {
            'estado': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'estado'
                }
            ),
        }

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['name', 'street', 'city', 'state', 'zipcode', 'country', 'phone']
        labels = {
            'name': 'Nombre',
            'street': 'Calle',
            'city': 'Ciudad',
            'state': 'Región',
            'zipcode': 'Código Postal',
            'country': 'País',
            'phone': 'Número de Teléfono',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre',
                    'id': 'name'
                }
            ),
            'street': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la calle',
                    'id': 'street'
                }
            ),
            'city': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la ciudad',
                    'id': 'city'
                }
            ),
            'state': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la región',
                    'id': 'state'
                }
            ),
            'zipcode': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el código postal',
                    'id': 'zipcode'
                }
            ),
            'country': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el país',
                    'id': 'country'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el número de teléfono',
                    'id': 'phone'
                }
            ),
        }

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = [
            'idPedido',
            'length',
            'width',
            'height',
            'weight',
            'distance_unit',
            'mass_unit',
        ]
        labels = {
            'idPedido': 'Compra asociada',
            'length': 'Longitud',
            'width': 'Ancho',
            'height': 'Altura',
            'weight': 'Peso',
            'distance_unit': 'Unidad de distancia',
            'mass_unit': 'Unidad de masa',
        }
        widgets = {
            'distance_unit': forms.Select(choices=[('in', 'Pulgadas'), ('cm', 'Centímetros')]),
            'mass_unit': forms.Select(choices=[('lb', 'Libras'), ('kg', 'Kilogramos')]),
        }

class InformeMensualForm(forms.ModelForm):
    class Meta:
        model = InformeMensual
        fields = ['descripcion']
        labels = {
            'descripcion': 'Descripción',
        }
        widgets = {
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Describa el informe',
                    'rows': 4,
                }
            ),
        }

class InformeDesempForm(forms.ModelForm):
    class Meta:
        model = InformeDesemp
        fields = ['descripcion']
        labels = {
            'descripcion': 'Descripción',
        }
        widgets = {
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción',
                    'rows': 4,
                }
            ),
        }

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['total']
        labels = {
            'total': 'Total',
        }
        widgets = {
            'total': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el total',
                }
            ),
        }

class BalanceMensualForm(forms.ModelForm):
    class Meta:
        model = BalanceMensual
        fields = ['notas']
        labels = {
            'notas': 'Notas',
        }
        widgets = {
            'notas': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese notas adicionales',
                    'rows': 4,
                }
            ),
        }




