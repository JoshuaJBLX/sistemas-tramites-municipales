"""Value Object: IntencionConsulta."""

from enum import Enum


class IntencionConsulta(str, Enum):
    CONSULTAR_REQUISITOS = 'consultar_requisitos'
    CONSULTAR_COSTO = 'consultar_costo'
    CONSULTAR_ESTADO = 'consultar_estado'
    CONSULTAR_UBICACION = 'consultar_ubicacion'
    SALUDO = 'saludo'
    OTRO = 'otro'
