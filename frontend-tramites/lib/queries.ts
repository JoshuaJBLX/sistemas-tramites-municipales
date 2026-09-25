import { obtenerTramites, type Tramite } from './api';

/** Query helpers para el catálogo de trámites y documentos. */
export async function fetchTramites(): Promise<Tramite[]> {
  try {
    return await obtenerTramites();
  } catch (error) {
    console.error('No se pudo obtener el catálogo de trámites', error);
    return [];
  }
}

export function filtrarTramites(tramites: Tramite[], q: string, categoria = 'Todas'): Tramite[] {
  return tramites.filter(
    (t) =>
      (categoria === 'Todas' || t.categoria === categoria) &&
      (q === '' || `${t.nombre} ${t.descripcion}`.toLowerCase().includes(q.toLowerCase())),
  );
}

