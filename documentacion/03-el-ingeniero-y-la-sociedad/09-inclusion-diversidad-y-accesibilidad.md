# 03.9 — Inclusión, Diversidad y Accesibilidad

> Parte de **03 — El Ingeniero y la Sociedad** (AG-101/AG-102). Leyenda: ✅ · ⚠️ · ❌ (G-XX).

## Accesibilidad web y discapacidad
| Medida | Estado |
|---|---|
| Diseño responsive/móvil | ✅ (`frontend-tramites`, Tailwind) |
| Alto contraste y tipografía legible | ✅ `globals.css` (tema cálido, sombras suaves) |
| Modo claro/oscuro | ⚠️ Relativo (tema claro predominante) |
| Animal/lector de pantalla etiquetas ARIA | ❌ Sin auditoría (G-26) |
| Cumplimiento WCAG 2.1 AA | ❌ Sin verificación (G-26) |

## Baja conectividad y rendimiento
- ✅ Página ligera, sin dependencias pesadas de cliente; demo offline en `lib/api.ts`.

## Simplicidad usable (baja alfabetización digital)
- ✅ Lenguaje claro, sugerencias rápidas, aviso legal.
- ⚠️ Sin validación de comprensión (SUS — G-05).

## Diversidad lingüística y NLU adaptativa
- ✅ Idioma español (normalización de tildes en `ServicioNLP.py`).
- ❌ Otros idiomas/dialectos futuros no contemplados.

## Vacíos
- ❌ G-26 (auditoría de accesibilidad) · ❌ G-05 (medición de usabilidad).