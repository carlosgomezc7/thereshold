import datetime

def calculate_metric_prediction(metric):
    """
    Calcula la derivada (tasa de cambio diaria) del consumo y predice 
    los días restantes antes de llegar al límite.
    
    En un entorno real, esto requeriría un histórico de datos. 
    Para este prototipo, simulamos una tasa constante calculada 
    asumiendo que el ciclo empezó el día 1 del mes actual.
    """
    today = datetime.date.today()
    start_of_cycle = today.replace(day=1)
    days_elapsed = (today - start_of_cycle).days
    
    if days_elapsed <= 0:
        days_elapsed = 1 # Prevenir división por cero si es día 1
        
    # Derivada (tasa de cambio diaria)
    daily_rate = metric.current_value / days_elapsed
    
    # Proyectar días restantes
    remaining_value = metric.max_limit - metric.current_value
    
    if daily_rate > 0:
        days_remaining = int(remaining_value / daily_rate)
    else:
        days_remaining = 999 # Consumo nulo
        
    # Clasificar el estado para el dashboard
    if days_remaining <= 5:
        status = 'critical'  # Rojo
    elif days_remaining <= 15:
        status = 'warning'   # Amarillo
    else:
        status = 'normal'    # Azul
        
    percentage = min(100, int((metric.current_value / metric.max_limit) * 100)) if metric.max_limit > 0 else 0
        
    return {
        'daily_rate': round(daily_rate, 2),
        'days_remaining': days_remaining,
        'status': status,
        'percentage': percentage
    }

def calculate_economic_optimization(a, b, c, d, F, max_capacity=1000):
    """
    Calcula el volumen de producción óptimo (q*) que maximiza la ganancia.
    
    Modelo:
    P(q) = a - b*q       (Precio / Demanda)
    R(q) = q * P(q)      (Ingreso)
    C(q) = F + c*q + d*q^2 (Costo)
    Profit(q) = R(q) - C(q)
              = - (b + d)*q^2 + (a - c)*q - F
              
    Primera derivada para encontrar el punto crítico:
    Profit'(q) = -2*(b + d)*q + (a - c) = 0 => q* = (a - c) / (2*(b + d))
    
    Segunda derivada para verificar que es máximo:
    Profit''(q) = -2*(b + d) -> Si b + d > 0, Profit''(q) < 0 (Máximo)
    """
    # Evitar divisiones por cero
    denominator = 2 * (b + d)
    if denominator <= 0:
        return {
            'optimal_q': 0.0,
            'max_profit': -F,
            'optimal_price': a,
            'revenue_at_opt': 0.0,
            'cost_at_opt': F,
            'is_valid': False,
            'message': 'Los coeficientes de sensibilidad de precio o ineficiencia de costo deben ser mayores a cero.'
        }
        
    # Punto crítico
    q_opt = (a - c) / denominator
    
    # Restricciones
    if q_opt < 0:
        # Si q_opt es negativo, el máximo en el dominio q >= 0 es q = 0
        q_opt = 0.0
        msg = "El precio de reserva (a) es menor que el costo variable unitario (c). No es rentable producir."
    elif q_opt > max_capacity:
        q_opt = float(max_capacity)
        msg = f"El óptimo teórico supera la capacidad máxima operativa ({max_capacity} unidades). Producción limitada a la capacidad."
    else:
        msg = "Punto óptimo calculado exitosamente dentro de los límites de capacidad."
        
    # Calcular métricas en el óptimo
    price_opt = max(0.0, a - b * q_opt)
    revenue_opt = q_opt * price_opt
    cost_opt = F + c * q_opt + d * (q_opt ** 2)
    profit_opt = revenue_opt - cost_opt
    
    # Generar puntos para la curva (para graficar)
    steps = 20
    curve_data = []
    # Definir el rango del gráfico hasta 1.5 veces el óptimo o la capacidad máxima
    limit_range = max(q_opt * 1.5, 10.0)
    if max_capacity:
        limit_range = min(limit_range, max_capacity)
        
    for i in range(steps + 1):
        q_val = (limit_range / steps) * i
        p_val = max(0.0, a - b * q_val)
        r_val = q_val * p_val
        c_val = F + c * q_val + d * (q_val ** 2)
        pr_val = r_val - c_val
        curve_data.append({
            'q': round(q_val, 1),
            'revenue': round(r_val, 2),
            'cost': round(c_val, 2),
            'profit': round(pr_val, 2)
        })
        
    return {
        'optimal_q': round(q_opt, 2),
        'optimal_price': round(price_opt, 2),
        'revenue_at_opt': round(revenue_opt, 2),
        'cost_at_opt': round(cost_opt, 2),
        'max_profit': round(profit_opt, 2),
        'is_valid': True,
        'message': msg,
        'curve_data': curve_data
    }
