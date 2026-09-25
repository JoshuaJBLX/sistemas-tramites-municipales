# 01.3 — Caracterización del Proceso (AS-IS)

> Parte de **01 — Análisis del Problema**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## 3.1 Proceso AS-IS con puntos críticos
- Descripción del proceso actual (documental): el ciudadano acude a ventanilla, consulta
  tableros/PDFs o llama; recepción manual; posibles desistimientos por expedientes incompletos.

## 3.2 Diagrama SIPOC del proceso actual

| Proveedor | Entrada | Proceso | Salida | Cliente |
|---|---|---|---|---|
| Ciudadano | Solicitud/duda | Atención en ventanilla / mesa de partes | Orientación o inicio de expediente | Ciudadano |

## 3.3 Caracterización de puntos críticos

| Punto crítico | Dónde ocurre | Quién participa | Información | Errores/retrasos |
|---|---|---|---|---|
| A. Consulta inicial | Ventanilla | Ciudadano + funcionario | Requisitos/costo/plazo | Inconsistencia de fuentes |
| B. Preparación | Hogar | Ciudadano | Requisitos | Expedientes incompletos |
| C. Recepción | Mesa de partes | Funcionario | Documentación | Falta de control de vigencia |
| D. Orientación oficial | Tableros/PDF | Ciudadano | TUPA | Documentos desactualizados |

- **Leyenda informativa (C)**: la caracterización es documental; el asistente del sistema ataca
  los puntos A (consulta) y D (vigencia) con `estado='vigente'` (✅ `BusquedaVectorialAdapter.py`).

## Vacíos asociados
- ❌ G-13: sin campos de vigencia detallada (`version`, `fecha_publicacion`); la vigencia se
  reduce al campo `estado`.