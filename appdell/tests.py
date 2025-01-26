import random
from faker import Faker
from .models import solicitud
from datetime import datetime, timedelta

# Inicializar Faker para generar datos ficticios
fake = Faker()

def generar_fecha_aleatoria(inicio, fin):
    """
    Genera una fecha aleatoria entre dos fechas dadas.
    """
    delta = fin - inicio
    random_days = random.randint(0, delta.days)
    return inicio + timedelta(days=random_days)

def generar_registros(num_registros=100):
    """
    Genera registros ficticios en la tabla RegistroBecado.
    Asegura que las cédulas no se repitan.
    """
    generos = ['Masculino', 'Femenino']
    carrera = [
        'agronomia animal', 'agronomia vegetal', 'medicina veterinaria',
        'medicina', 'enfermeria', 'radiologia', 'odontologia',
        'administracion comercial', 'contaduria publica',
        'economia', 'comunicacion social', 'derecho',
        'ing informatica', 'ing electronica',
        'ing hidrocarburos (gas)', 'ing hidrocarburos (petroleo)',
        'ingeniería industrial', 'educacion integral',
        'educacion mencion computacion'
    ]
    
    
    # Lista de valores posibles para el campo "cursando"
  
    # Usar un conjunto para evitar cédulas duplicadas
    cedulas_usadas = set()
    
    for _ in range(num_registros):
        # Generar una cédula única
        while True:
            cedula = fake.unique.random_int(min=1000000, max=99999999)
            if cedula not in cedulas_usadas:
                cedulas_usadas.add(cedula)
                break
        
        # Crear un registro ficticio
        registro = solicitud(
            nombre=fake.first_name(),
            apellido=fake.last_name(),
            cedula=str(cedula),
            edad=random.randint(18, 30),
            genero=random.choice(generos),
            f_nacimiento=fake.date_of_birth(minimum_age=18, maximum_age=30),
            email=fake.unique.email(),
            ubicacion=fake.city(),
            carrera=random.choice(carrera),
            # Generar fecha_creacion aleatoria entre hace 5 años y hoy
            fecha_creacion=generar_fecha_aleatoria(datetime.now() - timedelta(days=365*5), datetime.now()),
            comentario=fake.sentence(),
            residencia=fake.city(),
        )
        
        # Guardar el registro en la base de datos
        registro.save()
        
        # Imprimir un mensaje confirmando la creación del registro
        print(f"Registro creado: {registro.nombre} {registro.apellido} - Cédula: {registro.cedula}")

# Ejecutar la función para generar registros
generar_registros(50)  # Cambia el número si deseas menos o más registros


#necesito un codigo python django para insertar en una base de datos sql en la tabla solicitud datos ficticion en las columnas nombre apellido cedula edad f_nacimiento ubicacion #email genero comentario fecha_creacion residencia carrera teniendo en cuenta que las carreras son [
#        'agronomia animal', 'agronomia vegetal', 'medicina veterinaria',
#        'medicina', 'enfermeria', 'radiologia', 'odontologia',
#        'administracion comercial', 'contaduria publica',
#        'economia', 'comunicacion social', 'derecho',
#        'ing informatica', 'ing electronica',
#        'ing hidrocarburos (gas)', 'ing hidrocarburos (petroleo)',
#        'ingeniería industrial', 'educacion integral',
#        'educacion mencion computacion'
#    ] y los generos son ['Masculino', 'Femenino']