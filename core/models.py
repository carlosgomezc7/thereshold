from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='metrics')
    max_limit = models.FloatField(help_text="Límite máximo permitido")
    current_value = models.FloatField(
        default=0.0, help_text="Valor actual consumido")
    metric_type = models.CharField(
        max_length=10,
        choices=[
            ('ingreso', 'Ingreso'),
            ('egreso', 'Egreso'),
        ],
        default='ingreso',
        help_text='Tipo de métrica: ingreso o egreso'
    )
    unit = models.CharField(
        max_length=20, help_text="Unidad de medida, ej. GB, USD")
    cutoff_date = models.DateField(
        help_text="Fecha en que se reinicia el consumo")

    def __str__(self):
        return f"{self.name} - {self.department.name}"
