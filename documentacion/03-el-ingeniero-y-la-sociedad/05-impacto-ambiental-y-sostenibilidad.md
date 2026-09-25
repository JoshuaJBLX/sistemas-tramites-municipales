# 03.5 — Impacto Ambiental y Sostenibilidad

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## ODS relacionados
- **ODS 11** — Ciudades y comunidades sostenibles: servicios públicos accesibles (✅ canal digital).
- **ODS 12** — Producción y consumo responsables: menos papel/consultas presenciales (✅ implícito).
- **ODS 13** — Acción por el clima: menor huella frente a infraestructura en nube pesada (⚠️).

## Eficiencia energética real
- ✅ SLM **local y pequeño** (Qwen 2.5 3B, ~2-4 GB RAM) vs. LLMs remotos (>100B): menor consumo.
- ✅ Embeddings BGE-M3 locales (sin costo/energía por llamada API externa).
- ⚠️ No hay medición de consumo energético en el repositorio (G-16).

## Sostenibilidad del sistema
- ✅ Arquitectura hexagonal → bajo acoplamiento: reemplazar SLM o vectorstore es acotado.
- ⚠️ Mantenimiento: panel administrativo funcional pendiente (G-16); actualización por
  `documentos.estado` (G-13).