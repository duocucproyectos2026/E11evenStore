from django import forms
from .models import Cliente
from .models import Administrativo
from django.core.exceptions import ValidationError
import re
import random


# inicio sesion clientes/admin
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "email",
                "required": "required",
            }
        ),
    )

    clave = forms.CharField(
        label="clave",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "clave",
                "required": "required",
            }
        ),
    )


# Formulario registro clientes
class RegistroForm(forms.ModelForm):
    repetirClave = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Cliente
        fields = [
            "usuario",
            "nombre",
            "apellidos",
            "rut",
            "email",
            "clave",
            "repetirClave",
            "fechaNacimiento",
            "direccion",
        ]
        widgets = {
            "clave": forms.PasswordInput(),
            "fechaNacimiento": forms.DateInput(attrs={"type": "date"}),
            "usuario": forms.TextInput(attrs={"readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["usuario"].required = False

    def clean_rut(self):
        rut = self.cleaned_data.get("rut")
        if not re.match(r"^\d{7,8}-[\dkK]$", rut):
            raise ValidationError("El RUT debe tener el formato 12345678-9")
        return rut

    def clean(self):
        cleaned_data = super().clean()
        clave = cleaned_data.get("clave")
        repetir_clave = cleaned_data.get("repetirClave")
        if clave != repetir_clave:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Generar usuario único tipo CLTE_1234
        if not instance.usuario:
            while True:
                codigo = f"CLTE_{random.randint(1000, 9999)}"
                print(f"Intentando generar usuario: {codigo}")  # 
                if not Cliente.objects.filter(usuario=codigo).exists():
                    instance.usuario = codigo
                    print(f"Usuario asignado: {codigo}")  # 
                    break

        if commit:
            instance.save()
        return instance


# EDICION DATOS CLIENTE
class EditarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["usuario", "direccion", "email", "clave"]


class DireccionEnvioForm(forms.Form):
    direccion = forms.CharField(label="Dirección de envío", max_length=255)


# METODOS DE PAGO
class MetodoPagoForm(forms.Form):
    METODOS = [
        ("transferencia", "Transferencia Bancaria"),
        ("gift_card", "Gift Card"),
        ("tarjeta_credito", "Tarjeta de Crédito"),
        ("tarjeta_debito", "Tarjeta de Débito"),
    ]
    metodo_pago = forms.ChoiceField(choices=METODOS, label="Método de pago")
