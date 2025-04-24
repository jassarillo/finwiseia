from django import forms
from .models import RegistroEmpresa

from django import forms
from django.contrib.auth.hashers import make_password  # Para encriptar contraseñas
from .models import RegistroEmpresa

class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroEmpresa
        fields = ['nombre', 'email', 'password', 'persona', 'telefono', 'direccion', 'sector', 'pais', 'acercad']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre de la empresa'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email de la empresa'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de la empresa'}),
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección de la empresa'}),
            'acercad': forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre tu empresa'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])  # Encriptar la contraseña
        if commit:
            instance.save()
        return instance


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')  # Sobrescribimos 'username' para usar el email
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Correo electrónico o contraseña incorrectos.")
        return self.cleaned_data

