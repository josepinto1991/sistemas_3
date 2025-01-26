from django.shortcuts import render, redirect
from .models import solicitud, Registro_becado
from .forms import userForm, loginForm
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from datetime import datetime, date
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import pandas as pd
from django.http import HttpResponse
from django.http.response import JsonResponse


def copy(request):
    return render(request, "app/pages/copy_cy.html")


def success(request):
    return render(request, "app/pages/success.html")


def success2(request):
    return render(request, "app/pages/success2.html")


def index(request):

    today = datetime.now().strftime("%d de %B de %Y a las %H:%M")
    return render(request, "app/index.html", {"today": today})


def solicitudes(request):

    return render(request, "app/pages/application.html")


def solicitudes_2(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        cedula = request.POST.get("cedula")
        edad = request.POST.get("edad")
        f_nacimiento = request.POST.get("f_nacimiento")
        ubicacion = request.POST.get("ubicacion")
        email = request.POST.get("email")
        genero = request.POST.get("genero")
        residencia = request.POST.get("residencia")
        comentario = request.POST.get("comentario")
        carrera = request.POST.get("carrera")
        reporte_de_notas = request.FILES.get("reporte_de_notas")

        # Verificar si ya existe una solicitud con la misma cédula
        if solicitud.objects.filter(cedula=cedula).exists():
            return render(
                request,
                "app/pages/copy_ci.html",
                {
                    "error": "Ya formulaste una solicitud.",
                    "today": date.today(),
                    "solicitudes": solicitud.objects.all(),
                },
            )

        try:
            # Convertir f_nacimiento a un objeto date
            f_nacimiento = datetime.strptime(f_nacimiento, "%Y-%m-%d").date()

            # Validar si el archivo es un PDF
            if reporte_de_notas and not reporte_de_notas.name.endswith(".pdf"):
                return render(
                    request,
                    "app/pages/application_2.html",
                    {
                        "error": "Solo se permiten archivos PDF.",
                        "today": date.today(),
                        "solicitudes": solicitud.objects.all(),
                    },
                )

            # Crear una nueva instancia de Solicitud
            nueva_solicitud = solicitud(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                edad=int(edad),
                f_nacimiento=f_nacimiento,
                ubicacion=ubicacion,
                email=email,
                genero=genero,
                residencia=residencia,
                comentario=comentario,
                carrera=carrera,
                reporte_de_notas=reporte_de_notas,
            )
            nueva_solicitud.save()

            return redirect("success")

        except IntegrityError as e:
            print(f"Error al guardar la solicitud: {e}")
            return render(
                request,
                "app/pages/application_2.html",
                {
                    "error": "Ocurrió un error al guardar la solicitud.",
                    "today": date.today(),
                    "solicitudes": solicitud.objects.all(),
                },
            )

    else:
        solicitudes = solicitud.objects.all()
        context = {
            "today": date.today(),
            "solicitudes": solicitudes,
        }

    return render(request, "app/pages/application_2.html", context)


def buscar(request):
    cedulas = []
    registros = []  # Inicializa una lista para los registros
    mensaje = None
    query = request.GET.get("cedula")

    if request.method == "GET":
        if query:
            # Filtra las solicitudes por cédula
            cedulas = solicitud.objects.filter(cedula=query).order_by("cedula")
            # Filtra los registros que coinciden con las cédulas encontradas
            registros = Registro_becado.objects.filter(
                cedula=query
            )  # Ajusta según tu modelo
        else:
            mensaje = "Por favor, ingresa una cédula para buscar."

    return render(
        request,
        "app/pages/b_.html",
        {
            "cedulas": cedulas,
            "registros": registros,  # Pasa los registros al contexto
            "mensaje": mensaje,
        },
    )


def basic(request):
    return render(request, "app/pages/basic-grid.html")


# solo visible para administrador logueado
@login_required
def metricas(request):
    return render(request, "app/pages/metricas.html")


@login_required
def get_chart(request):
    # Obtener datos de las tablas
    registros_becados = Registro_becado.objects.all()
    # Agrupar estatus por fecha
    estatus_count = {"Aceptado": {}, "Rechazado": {}}

    for registro in registros_becados:
        fecha = registro.fecha_creacion.strftime("%Y-%m")
        estatus = registro.estatus  # Suponiendo que 'estatus' es un campo en el modelo

        if estatus not in ["Aceptado", "Rechazado"]:
            continue  # Ignorar otros estatus si existen

        if fecha not in estatus_count[estatus]:
            estatus_count[estatus][fecha] = 0
        estatus_count[estatus][fecha] += 1  # Contar cada registro por fecha

    # Preparar datos para el gráfico
    fechas_becados = list(
        set(estatus_count["Aceptado"].keys()).union(
            set(estatus_count["Rechazado"].keys())
        )
    )
    fechas_becados.sort()  # Asegurarse de que las fechas estén ordenadas

    conteos_aceptados = [
        estatus_count["Aceptado"].get(fecha, 0) for fecha in fechas_becados
    ]
    conteos_rechazados = [
        estatus_count["Rechazado"].get(fecha, 0) for fecha in fechas_becados
    ]
    conteo_todos = [
        estatus_count["Aceptado"].get(fecha, 0)
        + estatus_count["Rechazado"].get(fecha, 0)
        for fecha in fechas_becados
    ]

    # Calcular totales
    total_aceptados = sum(conteos_aceptados)
    total_rechazados = sum(conteos_rechazados)

    # Preparar datos para el gráfico de pastel
    pie_data = [
        {
            "value": total_aceptados,
            "name": "Aceptados",
            "itemStyle": {"color": "#4CAF50"},
        },
        {
            "value": total_rechazados,
            "name": "Rechazados",
            "itemStyle": {"color": "#F44336"},
        },
    ]

    detalles_tooltip = []
    for fecha in fechas_becados:
        total_aceptados = estatus_count["Aceptado"].get(fecha, 0)
        total_rechazados = estatus_count["Rechazado"].get(fecha, 0)
        total_registros = total_aceptados + total_rechazados
        detalles_tooltip.append(
            {
                "fecha": fecha,
                "aceptados": total_aceptados,
                "rechazados": total_rechazados,
                "total": total_registros,
            }
        )

    # Configurar el gráfico
    charts = {
        "chart1": {
            "title": {"text": "Conteo de Registros por Mes", "left": "center"},
            "legend": {  # Agregar leyendas aquí
                "data": [
                    "Aceptados",
                    "Rechazados",
                    "Todos",
                ],  # Nombres de las series para la leyenda
                "left": "right",
                "orient": "vertical",
            },
            "xAxis": {
                "type": "category",
                "data": fechas_becados,
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Aceptados",
                    "data": conteos_aceptados,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {"color": "#4CAF50"},  # Color verde para aceptados
                },
                {
                    "name": "Rechazados",
                    "data": conteos_rechazados,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {"color": "#F44336"},  # Color rojo para rechazados
                },
                {
                    "name": "Todos",
                    "data": conteo_todos,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {
                        "color": "#0000FF"  # Color azul para todos (código hexadecimal válido)
                    },
                },
            ],
            "tooltip_data": detalles_tooltip,
        },
        "chart2": {
            "title": {
                "text": "Distribución de porcentaje de Registros",
                "left": "center",
            },
            "legend": {"orient": "vertical", "left": "left"},
            "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c} ({d}%)"},
            "series": [
                {
                    "name": "Registros:",
                    "type": "pie",
                    "radius": ["40%", "70%"],  # Para hacer un donut
                    "center": ["50%", "50%"],
                    # Aquí se asignan los datos y se definen los colores
                    "data": pie_data,
                    # Efecto al pasar el mouse sobre un segmento
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        },
        # Gráfico 3: Promedio de solicitudes
        "chart3": {
            "title": {"text": "Conteo de Registros por Mes", "left": "center"},
            "legend": {  # Agregar leyendas aquí
                "data": [
                    "Aceptados",
                    "Rechazados",
                    "Todos",
                ],  # Nombres de las series para la leyenda
                "left": "right",
                "orient": "vertical",
            },
            "xAxis": {
                "type": "category",
                "data": fechas_becados,
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "Aceptados",
                    "data": conteos_aceptados,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {"color": "#4CAF50"},  # Color verde para aceptados
                },
                {
                    "name": "Rechazados",
                    "data": conteos_rechazados,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {"color": "#F44336"},  # Color rojo para rechazados
                },
                {
                    "name": "Todos",
                    "data": conteo_todos,
                    "type": "line",
                    "smooth": True,  # Opcional: suavizar la línea
                    "itemStyle": {
                        "color": "#0000FF"  # Color azul para todos (código hexadecimal válido)
                    },
                },
            ],
            "tooltip_data": detalles_tooltip,
        },
        # Gráfico 4: Promedio de registros becados
        "chart4": {
            "title": {
                "text": "Distribución de porcentaje de Registros",
                "left": "center",
            },
            "legend": {"orient": "vertical", "left": "left"},
            "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b}: {c} ({d}%)"},
            "series": [
                {
                    "name": "Registros:",
                    "type": "pie",
                    "radius": ["40%", "70%"],  # Para hacer un donut
                    "center": ["50%", "50%"],
                    # Aquí se asignan los datos y se definen los colores
                    "data": pie_data,
                    # Efecto al pasar el mouse sobre un segmento
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        },
    }

    return JsonResponse(charts)


@login_required
def full_solicitud(request):
    # Obtiene todos los registros inicialmente
    registros = solicitud.objects.all()

    # Filtrado basado en los parámetros de búsqueda
    cedula = request.GET.get("cedula")
    genero = request.GET.get("genero")
    carrera = request.GET.get("carrera")

    # Aplica filtros si se proporcionan
    if cedula:
        registros = registros.filter(cedula__icontains=cedula)
    if genero:
        registros = registros.filter(genero=genero)
    if carrera:
        registros = registros.filter(carrera=carrera)

    # Exportar a Excel si se solicita
    if request.GET.get("export") == "excel":
        df = pd.DataFrame(list(registros.values()))
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="registros_de_solicitudes_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
        )
        df.to_excel(response, index=False)
        return response

    # Renderizar la plantilla con los registros filtrados
    return render(
        request, "app/pages/full_vista_solicitud.html", {"registros": registros}
    )


@login_required
def full(request):
    # Obtiene todos los registros inicialmente
    registros = Registro_becado.objects.all()

    # Filtrado basado en los parámetros de búsqueda
    cedula = request.GET.get("cedula")
    genero = request.GET.get("genero")
    carrera = request.GET.get("carrera")
    tipo_beneficio = request.GET.get("t_beneficio")
    estatus = request.GET.get("estatus")

    # Aplica filtros si se proporcionan
    if cedula:
        registros = registros.filter(cedula__icontains=cedula)
    if genero:
        registros = registros.filter(genero=genero)
    if carrera:
        registros = registros.filter(carrera=carrera)
    if tipo_beneficio:
        registros = registros.filter(t_beneficio=tipo_beneficio)
    if estatus:
        registros = registros.filter(estatus=estatus)

    # Exportar a Excel si se solicita
    if request.GET.get("export") == "excel":
        df = pd.DataFrame(list(registros.values()))
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = (
            f'attachment; filename="registros_becados_{datetime.now().strftime("%Y-%m-%d")}.xlsx"'
        )
        df.to_excel(response, index=False)
        return response

    # Renderizar la plantilla con los registros filtrados
    return render(request, "app/pages/full-width.html", {"registros": registros})


@login_required
def form_registro(request):
    if request.method == "POST":
        # Recoger datos del formulario
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        cedula = request.POST.get("cedula")
        f_nacimiento = request.POST.get("f_nacimiento")
        ubicacion = request.POST.get("ubicacion")
        email = request.POST.get("email")
        genero = request.POST.get("genero")
        telefono1 = request.POST.get("telefono1")
        telefono2 = request.POST.get("telefono2")
        carrera = request.POST.get("carrera")
        sede = request.POST.get("cede")
        t_beneficio = request.POST.get("t_beneficio")
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_final = request.POST.get("fecha_final")
        estatus = request.POST.get("estatus")
        comentario = request.POST.get("comentario")
        cursando = request.POST.get("cursando")

        # Verificar si ya existe una solicitud con la misma cédula
        if Registro_becado.objects.filter(cedula=cedula).exists():
            return render(
                request,
                "app/pages/copy_ci.html",
                {
                    "error": "Ya formulaste un registro con la misma cédula.",
                    "today": date.today(),
                    "solicitudes": Registro_becado.objects.all(),
                },
            )

        try:
            # Crear nueva solicitud
            nueva_solicitud = Registro_becado(
                nombre=nombre,
                apellido=apellido,
                cedula=cedula,
                f_nacimiento=f_nacimiento,
                ubicacion=ubicacion,
                email=email,
                genero=genero,
                telefono1=telefono1,
                telefono2=telefono2,
                carrera=carrera,
                sede=sede,
                t_beneficio=t_beneficio,
                fecha_inicio=fecha_inicio,
                fecha_final=fecha_final,
                estatus=estatus,
                comentario=comentario,
                cursando=cursando,
            )
            nueva_solicitud.save()
            return redirect("success2")

        except IntegrityError:
            return render(
                request,
                "app/pages/form_registro.html",
                {
                    "error": "Ocurrió un error al guardar la solicitud. La cédula puede estar duplicada.",
                    "today": date.today(),
                    "solicitudes": Registro_becado.objects.all(),
                },
            )

    # Manejo del método GET
    solicitudes = Registro_becado.objects.all()
    context = {
        "today": date.today(),
        "solicitudes": solicitudes,
    }

    return render(request, "app/pages/form_registro.html", context)


# login y registro


class Registro(View):
    form_class = userForm
    initial = {"key": "value"}
    template_name = "app/pages/registro.html"

    @login_required  # quitar para poder reguistrar administradores validos
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")
            return redirect(to="/")
        return render(request, self.template_name, {"form": form})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="/")
        return super(Registro, self).dispatch(request, *args, **kwargs)


class CustomLoginView(LoginView):
    form_class = loginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)
