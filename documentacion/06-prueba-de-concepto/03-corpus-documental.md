# 06.3 — Corpus Documental

> Parte de **06 — Prueba de Concepto**. Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Descripción del corpus
- Documentos municipales: TUPA 2023 (252 procedimientos), ordenanzas, costos y plazos,
  requisitos y formatos — asimilables a los seeds del repositorio.

## Tratamiento inicial (a.md)
- Datos crudos → **CUADRO 7: Generación de corpus final** (campos: municipio, tramite,
  descripcion, tipo, categoria, costo, duracion, vigencia, formato_url).

## Mapeo a la BD implementada
| Campo del corpus (a.md) | Columna real | Tabla |
|---|---|---|
| codigo | `codigo` | `tramites` |
| tramite | `nombre` | `tramites` |
| descripcion | `descripcion` | `tramites` |
| tipo | `tipo` | `tramites` |
| categoria | — | ⚠️ G-14 (frontend `categoria` vs backend `tipo`) |
| costo | `costo` | `tramites` |
| duracion | `duracion_estimada_dias` | `tramites` |
| vigencia | `estado` (`vigente`) | `documentos`/filtros |
| formato_url | `url_formato`?/`fuentes` | `documentos`/`fuentes` |

## Estado real
- ✅ Corpus empírico disponible en `database/seeds/` (MPJ TUPA 2023).
- ⚠️ El corpus en formato de PoC (CUADRO 7) no está versionado como tal (G-21).