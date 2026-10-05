from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Direccion, Usuario


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    first_name = forms.CharField(max_length=150, required=True, label='Nombre')
    last_name = forms.CharField(max_length=150, required=True, label='Apellido')
    telefono = forms.CharField(max_length=20, required=False, label='Teléfono')

    class Meta:
        model = Usuario
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'telefono',
            'password1',
            'password2',
        ]
        labels = {'username': 'Nombre de usuario'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True}),
    )
    password = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['sector', 'calle', 'referencia', 'es_principal']
        labels = {
            'sector': 'Sector o barrio',
            'calle': 'Calle y número',
            'referencia': 'Referencia',
            'es_principal': 'Usar como dirección principal',
        }
        widgets = {
            'sector': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Villa Lora, Palmarito...',
            }),
            'calle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Calle Duarte #25',
            }),
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Casa azul frente al parque',
            }),
            'es_principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
