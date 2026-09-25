# 02.7 — Conocimientos Fundamentales y Especializados

> Parte de **02 — Conocimientos de Ingeniería** (AG-107). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 6.1 Ingeniería de requisitos
- ✅ RF y HU derivadas del problema (documentos 02.3 y 02.4).
- ✅ Trazabilidad HU→código en `../00-documentos-rectores/02-implementacion-de-historias.md`.

## 6.2 Modelamiento del dominio municipal
- ✅ Entidades: `Tramite.py`, `Documento.py`, `Consulta.py`, `Respuesta.py`, `Usuario.py`,
  `Municipalidad.py`, `Fuente.py`.
- ✅ Value objects: `EstadoDocumento`, `IntencionConsulta`, `NivelConfianza`, `TipoTramite`,
  `FuenteOficial`.
- ⚠️ Vigencia solo por `estado` (`vigente|obsoleto|en_revision`), sin `versión` (G-13).

## 6.3 Diseño de software
- ✅ Puertos/interfaces (inversión de dependencias): `domain/ports`.
- ✅ Desde la capa `domain` no se depende de `infrastructure` (núcleo puro).

## 7. Conocimientos especializados

### 7.1 Gobierno digital
- ✅ Alineado a D.L. 1412, "Mi Muni en Línea": canal digital ciudadano (chat).

### 7.2 Gestión documental
- ⚠️ Estados de vigencia básicos (`documentos.estado`); sin versión ni flujo de
  aprobación/derogación completo (G-13, HU-02/03 parciales).

### 7.3 Procesamiento de lenguaje natural (NLP)
- ✅ Normalización + patrones léxicos para intención (`ServicioNLP.py`).
- ❌ Sin modelos ML/NLU avanzados (G-02).

### 7.4 Conclusión de conocimientos especializados
- El dominio municipal y la orientación ciudadana están cubiertos de forma funcional; la NLP y
  la gestión documental avanzada quedan pendientes.