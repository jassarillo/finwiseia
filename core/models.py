from django.db import models

# Create your models here.

from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


from django.db import models

class RegistroEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Encriptaremos la contraseña más adelante
    persona = models.CharField(max_length=1, choices=[('F', 'Persona Fisica'), ('M', 'Persona Moral')])
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    sector = models.CharField(max_length=50, choices=[
        ('energetico', 'ENERGETICO'),
        ('inmobiliario', 'INMOBILIARIO'),
        ('materiales', 'MATERIALES'),
        ('industrial', 'INDUSTRIAL'),
        ('consumonobasico', 'BIENES DE CONSUMO NO BÁSICO'),
        ('consumofrecuente', 'PRODUCTOS DE CONSUMO FRECUENTE'),
        ('salud', 'SALUD'),
        ('financiero', 'SERVICIOS FINANCIEROS'),
        ('tecnologia', 'TECNOLOGIA DE LA INFORMACION'),
        ('telecomunicaciones', 'TELECOMUNICACIONES'),
        ('otro', 'OTRO')
    ])
    pais = models.CharField(max_length=2, choices=[
        ('1', 'México'),
        ('2', 'EUA'),
        ('3', 'Colombia'),
        ('4', 'Argentina'),
        ('5', 'Chile')
    ])
    acercad = models.TextField()

    def __str__(self):
        return self.nombre

from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id')  # Relacionar con el modelo User
    nombre = models.CharField(max_length=254)
    email = models.EmailField(unique=True)  # Email único
    password = models.CharField(max_length=255)  # Hash de la contraseña
    persona = models.CharField(max_length=1)  # 'F' o 'M' por ejemplo
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    sector = models.CharField(max_length=50)
    pais = models.CharField(max_length=50)
    acercad = models.TextField()

    class Meta:
        db_table = 'usuario'  # Nombre exacto de la tabla en la base de datos

    def __str__(self):
        return self.nombre


class ContactoEmpresa(models.Model):
    empresa = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    country_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=50, choices=[
        ('CEO', 'CEO / Fundador'),
        ('CFO', 'CFO / Finanzas'),
        ('Contralor', 'Contralor Financiero'),
        ('Analista', 'Analista Financiero'),
        ('Otro', 'Otro'),
    ])
    employees = models.CharField(max_length=50, choices=[
        ('1-10', '1 - 10'),
        ('11-50', '11 - 50'),
        ('51-200', '51 - 200'),
        ('201-500', '201 - 500'),
        ('501-1000', '501 - 1000'),
        ('1000+', 'Más de 1000'),
    ])
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa}"
