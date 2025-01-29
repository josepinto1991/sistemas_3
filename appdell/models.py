from django.db import models
import datetime 

# Create your models here.


class solicitud(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    apellido = models.CharField(max_length=100, blank=False, null=False)
    cedula = models.CharField(max_length=8, blank=False, null=False, unique=True)
    edad = models.IntegerField(blank=False, null=False) 
    f_nacimiento = models.DateField(blank=False, null=False)
    ubicacion = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=150, blank=False, null=False)
    genero = models.CharField(
        max_length=10,
        choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')],
        blank=True
    )
    residencia = models.CharField(max_length=100, blank=False, null=False)
    comentario = models.TextField(blank=True) 
    fecha_creacion = models.DateField(default=datetime.date.today, blank=False, null=False)
    carrera = models.CharField(max_length=100, default='none', blank=False, null=False)
    reporte_de_notas = models.FileField(upload_to='pdfs/', null=True, blank=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"


class Registro_becado(models.Model):
    nombre = models.CharField(max_length=100)
    nombre2 = models.CharField(max_length=100, blank=True)
    apellido = models.CharField(max_length=100)
    apellido2 = models.CharField(max_length=100, blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    genero = models.CharField(max_length=10, choices=[('masculino', 'Masculino'), ('femenino', 'Femenino')], blank=True)
    edad = models.IntegerField(blank=False, null=False)
    f_nacimiento = models.DateField()
    
    email = models.EmailField(max_length=150)
    telefono1 = models.CharField(max_length=12)
    telefono2 = models.CharField(max_length=12, blank=True)
    ubicacion = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    sede = models.CharField(max_length=100)
    
    cursando = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_final = models.DateField()
    
    t_beneficio = models.CharField(max_length=100)
    
    estatus = models.CharField(max_length=20)
    
    fecha_creacion = models.DateField(auto_now_add=True) 
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
