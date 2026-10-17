"""Genera database/seeds/tramites.sql con el catálogo del TUPA 2023 oficial.

Fuentes (ambas verificables):
  * Listado de 252 procedimientos: vault municipal
    `H:\\OBSIDIAN-WORKS\\MUNICIPALIDADES JUNIN\\08b - TUPA Listado Completo (252 Procedimientos).md`
  * PDF oficial del TUPA 2023 (gob.pe) del que se extraen costo, plazo,
    área responsable y requisitos por número de página impreso ("pág. N").

Uso:
    python backend/scripts/generar_seed_tupa.py [--pdf RUTA] [--listado RUTA]
        [--salida RUTA] [--sin-db]

El PDF solo se descarga si no se pasa --pdf. La extracción usa pypdf.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import urllib.request
import uuid
from difflib import SequenceMatcher
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

URL_TUPA = (
    'https://cdn.www.gob.pe/uploads/document/file/4966732/'
    'Texto%20%C3%9Anico%20de%20Procedimientos%20Administrativos%20%28TUPA%29%202023.pdf'
    '?v=1691764064'
)
RAIZ = Path(__file__).resolve().parents[2]
LISTADO_DEFECTO = Path(
    r'H:\OBSIDIAN-WORKS\MUNICIPALIDADES JUNIN'
    r'\08b - TUPA Listado Completo (252 Procedimientos).md'
)
SALIDA_DEFECTO = RAIZ / 'database' / 'seeds' / 'tramites.sql'
CACHE = Path(r'C:\Users\Acer\AppData\Local\Temp\opencode')
MUNICIPALIDAD_ID = '11111111-1111-1111-1111-111111111111'
ESPACIO_UUID = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')

CABECERA = 'Denominación del Procedimiento Administrativo'
CARGOS = ('JEFE', 'GERENTE', 'SUB GERENTE', 'DIRECTOR', 'DIRECTORA', 'PRESIDENTE',
          'COORDINADOR', 'ESPECIALISTA', 'ANALISTA', 'SUPERVISOR', 'ENCARGADO')
UNIDADES = ('OFICINA', 'GERENCIA', 'SUB GERENCIA', 'SUBGERENCIA', 'UNIDAD',
            'DIRECCION', 'DIRECCIÓN', 'SECRETARIA', 'SECRETARÍA', 'AREA', 'ÁREA',
            'ALCALDIA', 'ALCALDÍA', 'ARCHIVO', 'PRESUPUESTO', 'PLANEAMIENTO',
            'JEFATURA')
ORG_RE = re.compile(
    r'^(?:' + '|'.join(CARGOS) + r')?\s*[-:]?\s*(' + '|'.join(UNIDADES) + r')\b', re.I)
GENERICAS = {'MUNICIPALIDAD PROVINCIAL DE JUNIN', 'MUNICIPALIDAD', 'ENTIDAD'}

AREAS_POR_PALABRA = (
    ('TRIBUT', 'GERENCIA DE ADMINISTRACION TRIBUTARIA Y RENTAS'),
    ('PREDIAL', 'GERENCIA DE ADMINISTRACION TRIBUTARIA Y RENTAS'),
    ('REGISTRO CIVIL', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('NACIMIENTO', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('MATRIMONIO', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('DEFUNCIÓN', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('DEFUNCION', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('DOMICILIARIO', 'SUB GERENCIA DE REGISTRO CIVIL'),
    ('EDIFIC', 'GERENCIA DE DESARROLLO URBANO E INFRAESTRUCTURA'),
    ('HABILITACIÓN', 'GERENCIA DE DESARROLLO URBANO E INFRAESTRUCTURA'),
    ('HABILITACION', 'GERENCIA DE DESARROLLO URBANO E INFRAESTRUCTURA'),
    ('URBAN', 'GERENCIA DE DESARROLLO URBANO E INFRAESTRUCTURA'),
    ('CONSTRUCC', 'GERENCIA DE DESARROLLO URBANO E INFRAESTRUCTURA'),
    ('ITSE', 'OFICINA DE DEFENSA CIVIL'),
    ('SEGURIDAD EN EDIFICACIONES', 'OFICINA DE DEFENSA CIVIL'),
    ('AMBIENT', 'GERENCIA DE RECURSOS NATURALES Y MEDIO AMBIENTE'),
    ('MALEZA', 'GERENCIA DE RECURSOS NATURALES Y MEDIO AMBIENTE'),
    ('ARBOL', 'GERENCIA DE RECURSOS NATURALES Y MEDIO AMBIENTE'),
    ('ESPETÁCULO', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('ESPECTÁCULO', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('ESPECTACULO', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('VEHICULAR', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('VEHÍCULAR', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('TRÁNSITO', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('TRANSITO', 'SUB GERENCIA DE TRANSPORTE Y SEGURIDAD VIAL'),
    ('COPIA', 'OFICINA DE ARCHIVO'),
    ('EXPEDIENTE', 'OFICINA DE ARCHIVO'),
    ('DOCUMENTO', 'OFICINA DE ARCHIVO'),
    ('COMPRA', 'SUB GERENCIA DE LOGISTICA'),
    ('SELECCIÓN', 'SUB GERENCIA DE LOGISTICA'),
    ('SELECCION', 'SUB GERENCIA DE LOGISTICA'),
    ('INFORMACIÓN PÚBLICA', 'SECRETARIA GENERAL'),
    ('INFORMACION PUBLICA', 'SECRETARIA GENERAL'),
)
AREA_POR_DEFECTO = 'OFICINA DE ATENCIÓN AL CIUDADANO'

# Prototipos escritos a mano en el seed inicial que sí corresponden a un
# procedimiento del TUPA (decisión revisada uno a uno). Se conserva el id y
# el texto curado del prototipo; el costo/plazo/área vienen del PDF oficial.
MAPEO_PROTOTIPOS: dict[int, str] = {
    166: 'Autorización de Ocupación de Vía Pública',
    109: 'Certificado de No Adeudo',
    158: 'Certificado de Parámetros Urbanísticos y Edificatorios',
    134: 'Certificado de Posesión',
    194: 'Expedición de Partida de Nacimiento',
    220: 'Inscripción de Defunción',
    207: 'Inscripción de Matrimonio',
    188: 'Inscripción de Nacimiento',
    212: 'Separación Convencional',
}


# --------------------------------------------------------------------------- utilidades


def norm(texto: str) -> str:
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode()
    texto = texto.replace('"', '').replace("'", '')
    return re.sub(r'\s+', ' ', texto).lower().strip()


def sql_literal(valor: str) -> str:
    return "'" + valor.replace("'", "''") + "'"


def sql_array(valores: list[str]) -> str:
    if not valores:
        return "ARRAY[]::text[]"
    return 'ARRAY[' + ', '.join(sql_literal(v) for v in valores) + ']::text[]'


def id_tupa(numero: int) -> str:
    return str(uuid.uuid5(ESPACIO_UUID, f'tupa2023:{numero}'))


# --------------------------------------------------------------------------- PDF


def descargar_pdf(destino: Path) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    print(f'descargando TUPA 2023 -> {destino}')
    urllib.request.urlretrieve(URL_TUPA, destino)


def paginas_pdf(ruta_pdf: Path) -> list[str]:
    cache = CACHE / f'tupa_paginas_{ruta_pdf.stat().st_size}.json'
    if cache.exists():
        print(f'usando cache de texto: {cache}')
        return json.loads(cache.read_text(encoding='utf-8'))
    import pypdf

    print('extrayendo texto del PDF (pypdf)…')
    lector = pypdf.PdfReader(str(ruta_pdf))
    paginas = []
    for pagina in lector.pages:
        try:
            paginas.append(pagina.extract_text() or '')
        except Exception:
            paginas.append('')
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(paginas), encoding='utf-8')
    print(f'{len(paginas)} páginas extraídas -> {cache}')
    return paginas


def mapa_paginas(paginas: list[str]) -> dict[int, int]:
    mapa: dict[int, int] = {}
    for i, texto in enumerate(paginas):
        m = re.search(r'p[aá]g\.?\s*[:.]?\s*(\d{1,4})', texto[:300], re.I)
        if m:
            mapa.setdefault(int(m.group(1)), i)
    return mapa


# --------------------------------------------------------------------------- extracción


def denominacion(texto: str) -> str | None:
    if CABECERA not in texto:
        return None
    resto = texto.split(CABECERA, 1)[1]
    for linea in resto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith('Código'):
            continue
        linea = re.sub(r'^\s*\([A-D]\)\s*', '', linea)
        return linea.strip('" ').strip() or None
    return None


def extraer_costo(textos: list[str]) -> tuple[float | None, str, str]:
    """(monto, fuente, nota).

    * <=4 montos por página: son conceptos distintos de un mismo trámite
      (p. ej. derecho de búsqueda + copia fotostática) y se suman.
    * >4 montos con valores muy dispares (soles por m² o por tramo): es una
      tabla de tarifas; no se suma, se documenta el rango y el costo fijo
      queda en 0.00.
    """
    for k, texto in enumerate(textos):
        montos = [float(m.replace(',', ''))
                  for m in re.findall(r'Monto\s*-\s*S/\s*([\d.,]+)', texto)]
        if not montos:
            continue
        positivos = [m for m in montos if m > 0]
        tabla = (
            len(montos) >= 5
            and positivos
            and (max(montos) / min(positivos) >= 15 or len(set(montos)) >= 6)
        )
        if tabla:
            nota = (f'El TUPA fija un arancel variable según tabla de tarifas '
                    f'(desde S/ {min(positivos):.2f} hasta S/ {max(montos):.2f})')
            return None, 'tarifa_variable', nota
        return round(sum(montos), 2), 'monto_tupa', ''
    for k, texto in enumerate(textos):
        bloque = texto.split('Pago por derecho de tramitación', 1)
        bloque = bloque[1][:800] if len(bloque) > 1 else ''
        if bloque and re.search(r'gratuito', bloque, re.I):
            return 0.0, 'gratuito', ''
    # arancel proporcional (porcentaje): se documenta en la descripción
    for k, texto in enumerate(textos):
        for linea in texto.splitlines():
            if re.search(r'derecho de tramit', linea, re.I) and re.search(r'\d+[\.,]?\d*\s*%', linea):
                concepto = re.sub(r'\s+', ' ', linea).strip()
                nota = f'El TUPA fija un arancel proporcional: {concepto[:180]}'
                return None, 'proporcional', nota
    return None, '', ''


def extraer_plazo(texto: str) -> int | None:
    m = re.search(r'(\d+)\s*d[ií]as\s*h[aá]biles', texto, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)\s*d[ií]as\s*calendario', texto, re.I)
    if m:
        return int(m.group(1))
    if re.search(r'Aprobación automática', texto):
        return 1
    m = re.search(r'(\d+)\s*d[ií]as', texto, re.I)
    if m:
        return int(m.group(1))
    if re.search(r'inmediato|mismo d[ií]a', texto, re.I):
        return 1
    return None


def _unir_lineas(texto: str) -> list[str]:
    """Une líneas en mayúsculas partidas por salto de línea («… ORIENTACIÓN AL / …»)."""
    crudas = [re.sub(r'\s+', ' ', linea).strip() for linea in texto.splitlines()]
    unidas: list[str] = []
    for linea in crudas:
        conector = None
        if unidas:
            conector = re.search(r'\b(AL|A|DE|DEL|LA|EL|Y|EN|CON|POR|LOS|LAS|DO)\s*$', unidas[-1], re.I)
        if unidas and conector and unidas[-1].isupper() and linea.isupper():
            unidas[-1] = f'{unidas[-1]} {linea}'
        else:
            unidas.append(linea)
    return unidas


def extraer_area(textos: list[str]) -> str | None:
    for texto in textos:
        candidatas: list[str] = []
        for linea in _unir_lineas(texto):
            linea = re.split(r'Tel[eé]fono|Correo|Anexo|Horario|http|@|\d{3}-\d{4}', linea)[0]
            if ':' in linea and 'OFICINA' in linea.upper()[:30]:
                linea = linea.split(':')[0]
            linea = linea.strip(' -:')
            if len(linea) < 5 or len(linea) > 110:
                continue
            letras = [c for c in linea if c.isalpha()]
            if not letras or sum(c.isupper() for c in letras) / len(letras) < 0.85:
                continue
            if not ORG_RE.match(linea):
                continue
            limpia = re.sub(r'^(?:' + '|'.join(CARGOS) + r')?\s*[-:]?\s*', '', linea, flags=re.I)
            if limpia.upper() in GENERICAS or not ORG_RE.match(limpia):
                continue
            candidatas.append(limpia[:110])
        if candidatas:
            return candidatas[-1]
    return None


def extraer_requisitos(texto: str) -> list[str]:
    lineas = texto.splitlines()
    encontrados: list[str] = []
    actual: list[str] = []
    patron = re.compile(r'^\s*(\d{1,2})[\.\)]\s*[-–]?\s*(.{8,})')
    for linea in lineas:
        m = patron.match(linea)
        if m:
            if actual:
                encontrados.append(' '.join(actual).strip())
            actual = [m.group(2).strip()]
        elif actual and linea.strip() and len(linea.strip()) > 12:
            actual.append(linea.strip())
        elif actual:
            encontrados.append(' '.join(actual).strip())
            actual = []
    if actual:
        encontrados.append(' '.join(actual).strip())

    limpios: list[str] = []
    for req in encontrados:
        req = re.sub(r'\s+', ' ', req).strip(' -:')
        if 12 <= len(req) <= 220:
            limpios.append(req[:220])
    return limpios[:8]


def ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def pagina_datos(paginas: list[str], mapa: dict[int, int], numero: int) -> tuple[int, list[str]] | None:
    for candidata in (numero, numero - 1, numero - 2, numero - 3):
        idx = mapa.get(candidata)
        if idx is None:
            continue
        texto = paginas[idx]
        if denominacion(texto):
            textos = [texto]
            if idx + 1 < len(paginas):
                textos.append(paginas[idx + 1])
            return idx, textos
    return None


def buscar_global(nombre: str, paginas: list[str]) -> tuple[int, list[str], str, float] | None:
    mejor, mejor_ratio, mejor_idx = None, 0.0, None
    for j, texto in enumerate(paginas):
        denom = denominacion(texto)
        if not denom:
            continue
        r = ratio(nombre, denom)
        if r > mejor_ratio:
            mejor, mejor_ratio, mejor_idx = denom, r, j
    if mejor_idx is not None and mejor_ratio >= 0.62:
        textos = [paginas[mejor_idx]]
        if mejor_idx + 1 < len(paginas):
            textos.append(paginas[mejor_idx + 1])
        return mejor_idx, textos, mejor, mejor_ratio
    return None


# --------------------------------------------------------------------------- listado


def leer_listado(ruta: Path) -> list[dict]:
    filas: list[dict] = []
    seccion = 'Procedimientos administrativos'
    patron = re.compile(r'^\|\s*(\d+)\s*\|\s*(.+?)\s*\|\s*(\d+)\s*\|$')
    for linea in ruta.read_text(encoding='utf-8').splitlines():
        cab = re.match(r'^###\s*\d+\.\s*(.+)$', linea.strip())
        if cab:
            seccion = cab.group(1).strip()
            continue
        cab2 = re.match(r'^##\s+(SECCIÓN\s*\d+:\s*.+)$', linea.strip())
        if cab2:
            seccion = re.sub(r'^SECCIÓN\s*\d+:\s*', '', cab2.group(1)).strip()
            continue
        m = patron.match(linea.strip())
        if m:
            filas.append({
                'numero': int(m.group(1)),
                'nombre': re.sub(r'\s+', ' ', m.group(2)).strip(),
                'pagina': int(m.group(3)),
                'seccion': seccion,
            })
    return filas


def clasificar_tipo(nombre: str) -> str:
    t = norm(nombre)
    if 'licencia de funcionamiento' in t or 'funcionamiento' in t:
        return 'licencia_funcionamiento'
    if 'partida de nacimiento' in t or 'inscripcion de nacimiento' in t:
        return 'partida_nacimiento'
    if 'certificado domiciliario' in t or 'domiciliari' in t:
        return 'certificado_domicilio'
    if ('licencia de edificacion' in t or 'habilitacion urbana' in t
            or 'edificacion' in t or 'construccion' in t):
        return 'licencia_construccion'
    if any(k in t for k in ('tribut', 'impuesto', 'predial', 'arbitrio', 'alcabala',
                            'mora', 'tributos')):
        return 'pago_tributos'
    return 'otro'


def area_de_respaldo(nombre: str) -> str:
    t = norm(nombre)
    for clave, area in AREAS_POR_PALABRA:
        if norm(clave) in t:
            return area
    return AREA_POR_DEFECTO


# --------------------------------------------------------------------------- BD


def tramites_existentes(sin_db: bool) -> dict[str, list[dict]]:
    """Ids ya sembrados, agrupados por nombre (varios trámites pueden repetirlo).

    Se consumen de a uno para no reutilizar el mismo id dos veces.
    """
    if sin_db:
        return {}
    try:
        import asyncio
        import os

        import asyncpg
        from dotenv import load_dotenv

        load_dotenv(RAIZ / '.env')
        dsn = (
            f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
            f"@{os.environ.get('POSTGRES_HOST', 'localhost')}"
            f":{os.environ.get('POSTGRES_PORT', '5432')}/{os.environ['POSTGRES_DB']}"
        )

        async def _leer() -> list:
            conn = await asyncpg.connect(dsn=dsn)
            try:
                return await conn.fetch(
                    'SELECT id, nombre, descripcion, tipo, requisitos, costo, '
                    '       duracion_estimada_dias, area_responsable FROM tramites '
                    'ORDER BY creado_en, id'
                )
            finally:
                await conn.close()

        filas = asyncio.run(_leer())
        existentes: dict[str, list[dict]] = {}
        for fila in filas:
            existentes.setdefault(norm(fila['nombre']), []).append({
                'id': fila['id'], 'nombre': fila['nombre'],
                'descripcion': fila['descripcion'], 'tipo': fila['tipo'],
                'requisitos': list(fila['requisitos'] or []),
                'costo': fila['costo'], 'duracion': fila['duracion_estimada_dias'],
                'area': fila['area_responsable'],
            })
        return existentes
    except Exception as exc:  # noqa: BLE001 - el seed debe poder generarse sin BD
        print(f'  (sin base de datos: {exc})')
        return {}


# --------------------------------------------------------------------------- seed


def generar(args: argparse.Namespace) -> None:
    pdf = args.pdf
    if pdf is None:
        pdf = CACHE / 'tupa2023.pdf'
        if not pdf.exists():
            descargar_pdf(pdf)

    paginas = paginas_pdf(pdf)
    mapa = mapa_paginas(paginas)
    listado = leer_listado(args.listado)
    existentes = tramites_existentes(args.sin_db)
    print(f'procedimientos: {len(listado)} · existentes en BD: {len(existentes)}')

    filas_sql: list[str] = []
    actualizados, nuevos, sin_costo, reutilizados = 0, 0, 0, 0
    estadisticas = {'costo': 0, 'area': 0, 'plazo': 0, 'requisitos': 0}

    for fila in listado:
        encontro = pagina_datos(paginas, mapa, fila['pagina'])
        if encontro:
            idx, textos = encontro
            denom = denominacion(textos[0])
            r = ratio(fila['nombre'], denom)
            if r < 0.30:
                alt = buscar_global(fila['nombre'], paginas)
                if alt and alt[3] > max(r, 0.55):
                    idx, textos, denom = alt[0], alt[1], alt[2]
        else:
            alt = buscar_global(fila['nombre'], paginas)
            if alt:
                idx, textos, denom = alt[0], alt[1], alt[2]
            else:
                idx, textos, denom = None, [], None

        costo, fuente_costo, nota_costo = (None, '', '')
        plazo, area, requisitos = None, None, []
        if textos:
            costo, fuente_costo, nota_costo = extraer_costo(textos)
            plazo = extraer_plazo(textos[0])
            area = extraer_area(textos)
            requisitos = extraer_requisitos(textos[0])

        if costo is None:
            sin_costo += 1
        estadisticas['costo'] += costo is not None
        estadisticas['area'] += bool(area)
        estadisticas['plazo'] += plazo is not None
        estadisticas['requisitos'] += bool(requisitos)

        # Dos entradas del TUPA pueden compartir nombre: cada fila existente
        # se consume una sola vez (evita duplicar la clave primaria).
        cola = existentes.get(norm(fila['nombre']))
        existente = cola.pop(0) if cola else None
        prototipo_mapeado = False
        if existente is None and fila['numero'] in MAPEO_PROTOTIPOS:
            cola = existentes.get(norm(MAPEO_PROTOTIPOS[fila['numero']]))
            existente = cola.pop(0) if cola else None
            prototipo_mapeado = existente is not None
        if existente:
            id_tramite = str(existente['id'])
            nombre = existente['nombre']
            descripcion = existente['descripcion']
            tipo = existente['tipo']
            requisitos_finais = existente['requisitos'] or requisitos
            costo_final = costo if costo is not None else 0
            plazo_final = plazo if plazo is not None else (existente['duracion'] or 0)
            area_final = area or existente['area'] or area_de_respaldo(fila['nombre'])
            if nota_costo and nota_costo not in (existente['descripcion'] or ''):
                descripcion = (existente['descripcion'] or '').rstrip()
                descripcion += f' {nota_costo}.'
            if prototipo_mapeado and denom and norm(denom) != norm(nombre):
                if 'Denominación oficial del TUPA' not in descripcion:
                    descripcion = descripcion.rstrip()
                    descripcion += f' Denominación oficial del TUPA: «{denom}».'
            reutilizados += 1
        else:
            id_tramite = id_tupa(fila['numero'])
            nombre = fila['nombre'][:200]
            tipo = clasificar_tipo(fila['nombre'])
            requisitos_finais = requisitos
            costo_final = costo if costo is not None else 0
            plazo_final = plazo if plazo is not None else 0
            area_final = area or area_de_respaldo(fila['nombre'])
            nuevos += 1

            partes = [
                f"Procedimiento N.° {fila['numero']} del TUPA 2023 "
                f"(sección «{fila['seccion']}», pág. {fila['pagina']}).",
            ]
            if denom:
                partes.append(f"Denominación oficial del TUPA: «{denom}».")
            if nota_costo:
                partes.append(nota_costo + '.')
            elif fuente_costo == '':
                partes.append(
                    'El TUPA no indica monto fijo en soles para este procedimiento; '
                    'consulte el arancel vigente en el portal municipal.')
            descripcion = ' '.join(partes)

        if existente and (costo is not None or area or plazo is not None):
            actualizados += 1

        filas_sql.append(
            '('
            + sql_literal(id_tramite) + ',\n '
            + sql_literal(MUNICIPALIDAD_ID) + ',\n '
            + sql_literal(nombre) + ',\n '
            + sql_literal(descripcion) + ',\n '
            + sql_literal(tipo) + ',\n '
            + sql_array(requisitos_finais) + ',\n '
            + f'{float(costo_final or 0):.2f},\n '
            + f'{int(plazo_final or 0)},\n '
            + (sql_literal(area_final[:120]) if area_final else 'NULL')
            + ')'
        )

    cabecera = f"""-- =============================================================
-- seeds/tramites.sql
-- Catálogo de trámites del TUPA 2023 (fuente oficial gob.pe).
-- Generado por backend/scripts/generar_seed_tupa.py el 2026-10-16.
--
-- Fuentes:
--   * PDF del TUPA 2023 (gob.pe, archivo 4966732): costo, plazo,
--     área responsable y requisitos, por número de página impreso.
--   * Listado de referencia del vault municipal (252 entradas):
--     249 procedimientos (Sección 1) + 1 servicio en exclusividad
--     (Sección 2) + 2 formularios (Sección 3).
--
-- Cobertura de la extracción automática sobre las 252 entradas:
--   costo real: {estadisticas['costo']} · área responsable: {estadisticas['area']} ·
--   plazo: {estadisticas['plazo']} · requisitos: {estadisticas['requisitos']}
--   sin monto fijo en soles (arancel proporcional, tabla de tarifas o no
--   indicado): {sin_costo}
--
-- Notas:
--   * Es idempotente: usa ON CONFLICT (id) DO UPDATE. No borra filas.
--   * `area_responsable` es la última unidad orgánica indicada por el TUPA
--     en la página del procedimiento (la de aprobación). Cuando el TUPA solo
--     indica la unidad de presentación, se registra esa.
--   * 9 prototipos del seed inicial sí corresponden a un procedimiento del
--     TUPA (MAPEO_PROTOTIPOS): conservan su id y texto curado y toman
--     costo/plazo/área del PDF oficial. Los demás prototipos sin
--     equivalente en el TUPA se conservan aparte en la base de datos.
--   * La identidad municipal del entorno de datos es la Provincial de
--     Junín (fuentes del TUPA); el nombre del portal es Huancayo (D-12).
-- Regenerar: tools\\generar-seed-tupa.ps1
-- =============================================================

"""

    cuerpo = (
        'INSERT INTO tramites (id, municipalidad_id, nombre, descripcion, tipo, '
        'requisitos, costo, duracion_estimada_dias, area_responsable)\nVALUES\n'
        + ',\n'.join(filas_sql)
        + '\nON CONFLICT (id) DO UPDATE SET\n'
        '    nombre = EXCLUDED.nombre,\n'
        '    descripcion = EXCLUDED.descripcion,\n'
        '    tipo = EXCLUDED.tipo,\n'
        '    requisitos = EXCLUDED.requisitos,\n'
        '    costo = EXCLUDED.costo,\n'
        '    duracion_estimada_dias = EXCLUDED.duracion_estimada_dias,\n'
        '    area_responsable = EXCLUDED.area_responsable;\n'
    )

    args.salida.write_text(cabecera + cuerpo, encoding='utf-8')
    print(f'escrito: {args.salida}')
    print(f'filas: {len(filas_sql)} (nuevos {nuevos} · reutilizados {reutilizados} '
          f'· actualizados {actualizados})')
    print(f'costo {estadisticas["costo"]} · area {estadisticas["area"]} · '
          f'plazo {estadisticas["plazo"]} · requisitos {estadisticas["requisitos"]} · '
          f'sin costo fijo {sin_costo}')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', type=Path, help='PDF local del TUPA 2023')
    parser.add_argument('--listado', type=Path, default=LISTADO_DEFECTO)
    parser.add_argument('--salida', type=Path, default=SALIDA_DEFECTO)
    parser.add_argument('--sin-db', action='store_true')
    generar(parser.parse_args())


if __name__ == '__main__':
    main()
