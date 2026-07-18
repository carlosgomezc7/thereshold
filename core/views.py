from django.shortcuts import render
from django.http import JsonResponse
from .models import Department
from .calculators import calculate_metric_prediction, calculate_economic_optimization

def dashboard_view(request):
    """
    Vista principal del Dashboard.
    Obtiene los departamentos y métricas, e inyecta los cálculos predictivos
    para ser renderizados en el template.
    """
    # Usamos prefetch_related para optimizar las consultas a la base de datos
    departments = Department.objects.prefetch_related('metrics').all()
    
    dashboard_data = []
    
    for dept in departments:
        dept_data = {
            'department': dept.name,
            'metrics': []
        }
        for metric in dept.metrics.all():
            # Inyectar el cálculo predictivo desde calculators.py
            prediction = calculate_metric_prediction(metric)
            metric_info = {
                'id': metric.id,
                'name': metric.name,
                'max_limit': metric.max_limit,
                'current_value': metric.current_value,
                'unit': metric.unit,
                'cutoff_date': metric.cutoff_date.strftime('%Y-%m-%d'),
                'prediction': prediction
            }
            dept_data['metrics'].append(metric_info)
            
        dashboard_data.append(dept_data)

    context = {
        'dashboard_data': dashboard_data
    }
    return render(request, 'core/dashboard.html', context)

def generate_ai_summary(request):
    """
    Vista preparada para consumir la API de Gemini.
    Al presionar el botón "Generar Resumen AI", se haría una petición POST aquí.
    """
    if request.method == 'POST':
        # TODO: Implementar la integración real con Gemini API
        # 1. Recopilar datos de métricas críticas desde la DB
        # 2. Formatear el prompt: prompt = f"Analiza estos recursos y dame recomendaciones: {datos}"
        # 3. Llamar a la API: response = gemini_client.generate_content(prompt)
        # 4. Obtener el texto: summary = response.text
        
        # Respuesta simulada para el prototipo
        summary = "Este es un resumen predictivo generado por IA (Simulado). El departamento de IT está a punto de agotar su presupuesto de AWS en 3 días. Se recomienda apagar las instancias EC2 no utilizadas. El almacenamiento en la nube de Contabilidad está en niveles óptimos."
        
        return JsonResponse({'status': 'success', 'summary': summary})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

def optimization_view(request):
    """
    Vista interactiva para simular parámetros económicos de optimización.
    """
    # Valores por defecto para la simulación
    a = float(request.GET.get('a', 150.0))    # Precio de reserva
    b = float(request.GET.get('b', 0.1))      # Sensibilidad de precio
    c = float(request.GET.get('c', 30.0))     # Costo variable base
    d = float(request.GET.get('d', 0.05))     # Ineficiencia de costo variable
    F = float(request.GET.get('F', 1000.0))   # Costo fijo
    max_cap = int(request.GET.get('max_cap', 1500))
    
    optimization_result = calculate_economic_optimization(a, b, c, d, F, max_cap)
    
    context = {
        'params': {
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'F': F,
            'max_cap': max_cap
        },
        'result': optimization_result
    }
    
    return render(request, 'core/optimization.html', context)
