# PMV2 - Extensión de documentos

## Nuevos campos en documentos
- `version`, `fecha_publicacion`, `archivo_nombre`, `mime_type`, `hash_contenido`
- `fragmentado`, `eliminado_en`

## Tabla fragmentos_documento
Para chunking con embeddings (HU-04).

## Migración
Aplicar: `database/migrations/004_documentos_pmv2.sql`

## Backend
- Nuevos puertos/adaptadores: `ExtraccionTextoPort`, `AlmacenamientoDocumentosPort`, `FragmentoRepository`
- Caso de uso `CargarDocumento` (orquesta carga + extracción + almacenamiento + fragmentación)
- Caso de uso `ProcesarDocumento` (chunking + embeddings por fragmento)
- `GestionarDocumentos` ampliado (baja lógica, filtros, metadatos)
- `DocumentoRepository` ampliado (listar, marcar_eliminado, eliminar_fisico)
- `FragmentoRepositoryImpl`, `ExtraccionTextoAdapter`
- Nuevos endpoints admin: `POST/GET /api/admin/documentos/*`, `POST /api/admin/documentos/{id}/procesar`, `DELETE /api/admin/documentos/{id}` (lógica), `DELETE /api/admin/documentos/{id}/fisico`
- Enpoints públicos de documentos mantenidos (compatibles)

## Frontend
- `DocumentManager` en admin: carga con metadatos, reprocesado, baja lógica/física
- `lib/api.ts` ampliado con funciones admin de documentos
- Reemplaza el listado estático por gestión real (G-12 en parte)

## Notas
- Upload ahora valida extensiones (.pdf,.docx,.txt,.md) y extrae texto (D-7 mitigado)
- Baja lógica `eliminado_en` cumple HU-03 (no usar en búsquedas por defecto)
- `derogado` añadido al enum
- Fragmentos guardados con embedding para futura recuperación por fragmento (HU-04)
