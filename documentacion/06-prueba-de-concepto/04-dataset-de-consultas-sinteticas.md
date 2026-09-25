# 06.4 — Dataset de Consultas Sintéticas

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Diseño del dataset (método Toby Sterling)
- Preguntas generadas: **200** (a.md) usando el método Sterling (respuesta → contexto →
  pregunta), cubriendo: modalidades (estándar/barata/al paso), otras variantes
  (`otros casos especiales`, `necesito ayuda`, etc.) y formas coloquiales.

## Distribución por intención objetivo (a.md)
| Intención | Sin variación | Con variación | Total |
|---|---|---|---|
| consultar_requisitos | 15 | 45 | 60 |
| consultar_costo | 15 | 45 | 60 |
| consultar_estado | 15 | 25 | 40 |
| consultar_ubicacion | 15 | 25 | 40 |

## Correspondencia con el clasificador real
- ✅ `IntencionConsulta` del dominio incluye estos valores **+ saludo + otro** (6 valores).
- ⚠️ El dataset de 200 consultas **no está versionado** (G-21); el clasificador real es por
  patrones regex (`ServicioNLP.py`), no por dataset (G-02).