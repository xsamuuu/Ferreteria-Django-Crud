from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'descripcion', 'categoria', 'proveedor', 'precio_compra', 'precio_venta', 'stock', 'stock_minimo', 'unidad_medida', 'activo']


class AddToCartForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:100px'}))


class CheckoutForm(forms.Form):
    tipo_documento = forms.ChoiceField(choices=[('DNI','DNI'),('RUC','RUC'),('CE','CE'),('PAS','PAS')])
    numero_documento = forms.CharField(max_length=20)
    nombres = forms.CharField(max_length=100)
    apellidos = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)

