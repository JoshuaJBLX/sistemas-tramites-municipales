# 01.1 — Contexto del Problema

> Parte de **01 — Análisis del Problema** (equiv. a.md "1. Análisis del problema.docx").
> Leyenda: ✅ · ⚠️ · ❌ (G-XX). Entidad del sistema: **MPJ (Junín)**, TUPA 2023.

## Organización o comunidad objetivo
- Ciudadanos que requieren trámites municipales.
- Personal de atención al ciudadano.
- Proyección: municipalidades provinciales y distritales de Junín.

## Sector
- Sector público — gobierno local.
- E-government, modernización de la gestión pública, simplificación administrativa,
  Política Nacional de Transformación Digital, estrategia "Mi Muni en Línea" (PCM).

## Ubicación
- **a.md** ubicaba el piloto en Huancayo (MPH); el sistema implementado corresponde a la
  **Municipalidad Provincial de Junín** (región Junín), TUPA 2023 (252 procedimientos),
  portal <https://www.gob.pe/munijunin>.

## Proceso involucrado
- Procedimientos regulados por el TUPA: licencias, autorizaciones, certificados/constancias,
  registros municipales, registro civil, tributos y urbanismo (✅ en `database/seeds/tramites.sql`).

## Usuarios afectados
Ciudadanos en general · emprendedores · profesionales del sector construcción · adultos mayores ·
funcionarios municipales · personal de mesa de partes.

## Situación actual
- Información dispersa: ventanilla presencial, tableros físicos, PDFs del portal, teléfono,
  terceros no oficiales.
- El sistema implementado responde con un canal único de consulta web (asistente RAG+SLM) ✅.

## Vacíos asociados
- ❌ G-16: sin medición del impacto real del canal.