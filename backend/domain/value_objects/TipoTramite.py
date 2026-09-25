"""Value Object: TipoTramite."""

from enum import Enum


class TipoTramite(str, Enum):
    LICENCIA_FUNCIONAMIENTO = 'licencia_funcionamiento'
    PARTIDA_NACIMIENTO = 'partida_nacimiento'
    CERTIFICADO_DOMICILIO = 'certificado_domicilio'
    LICENCIA_CONSTRUCCION = 'licencia_construccion'
    PAGO_TRIBUTOS = 'pago_tributos'
    OTRO = 'otro'
