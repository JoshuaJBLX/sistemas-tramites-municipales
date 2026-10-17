"""Genera el dataset sintético de evaluación (G-21 / P2-18).

Método declarado en `documentacion/06-prueba-de-concepto/04-dataset-de-consultas-sinteticas.md`
(respuesta -> contexto -> pregunta, estilo Sterling), aplicado aquí de forma
reproducible sobre el catálogo real del TUPA sembrado en la base de datos.

Salida: `documentacion/06-prueba-de-concepto/dataset-poc.csv`
Columnas: id, intencion_objetivo, pregunta, tramite_esperado_id, tramite_esperado_nombre
"""

import asyncio
import csv
import os
import random
import sys
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / 'documentacion' / '06-prueba-de-concepto' / 'dataset-poc.csv'
SEMILLA = 20261016

PLANTILLAS = {
    'consultar_requisitos': [
        '¿Qué documentos necesito para {nombre}?',
        '¿Cuáles son los requisitos de {nombre}?',
        'Quiero hacer {nombre}, ¿qué piden?',
        'Para {nombre} ¿qué papeles llevo?',
        'Requisitos del trámite {nombre}.',
        'Me falta saber qué llevar para {nombre}.',
        'oye, para {nombre} ¿qué papeles piden?',
        'porfa ¿qué documentos piden en {nombre}?',
        'Necesito ayuda con {nombre}: ¿qué documentos debo presentar?',
        '¿Qué llevar para {nombre} la primera vez?',
    ],
    'consultar_costo': [
        '¿Cuánto cuesta {nombre}?',
        '¿Cuál es el costo de {nombre}?',
        '¿Cuánto es el arancel de {nombre}?',
        'Para {nombre} ¿cuánto hay que pagar?',
        'Precio del trámite {nombre}.',
        '¿El {nombre} sale caro?',
        'oye ¿cuánto es para {nombre}?',
        'porfa dime cuánto cuesta {nombre}',
        'Necesito ayuda con {nombre}: ¿cuánto debo pagar?',
        '¿Cuánto pagan en {nombre} según el TUPA?',
    ],
    'consultar_estado': [
        '¿Cómo saber el estado de mi {nombre}?',
        '¿Dónde consulto el estado de {nombre}?',
        'Seguimiento del trámite {nombre}.',
        'Ya subí mi {nombre}, ¿cómo veo si está listo?',
        '¿Qué pasos llevo en {nombre}?',
        'oye ¿dónde veo si ya avanzó mi {nombre}?',
        'porfa ¿cómo checo el estado de {nombre}?',
        'Necesito ayuda con {nombre}: ¿dónde consulto si avanzó?',
        '¿Hay forma de saber en qué va mi {nombre}?',
        'Quiero revisar el estado de mi {nombre}.',
    ],
    'consultar_ubicacion': [
        '¿Dónde hago {nombre}?',
        '¿En qué oficina tramito {nombre}?',
        '¿A qué unidad voy para {nombre}?',
        'Ubicación del área que atiende {nombre}.',
        '¿Dónde presento los papeles de {nombre}?',
        'oye ¿dónde queda {nombre}?',
        'porfa dime a qué oficina voy para {nombre}',
        'Necesito ayuda con {nombre}: ¿a quién le pregunto?',
        '¿Cuál es la dirección para hacer {nombre}?',
        '¿En qué local municipal atienden {nombre}?',
    ],
}

QUERY = """
    SELECT id, nombre
    FROM tramites
    WHERE area_responsable IS NOT NULL
    ORDER BY nombre
    LIMIT 50
"""


async def main() -> None:
    load_dotenv(RAIZ / '.env')
    conn = await asyncpg.connect(
        host=os.environ['POSTGRES_HOST'],
        port=int(os.environ['POSTGRES_PORT']),
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD'],
        database=os.environ['POSTGRES_DB'],
    )
    try:
        filas = await conn.fetch(QUERY)
    finally:
        await conn.close()

    rng = random.Random(SEMILLA)
    filas_csv = []
    contador = 1
    for intencion, plantillas in PLANTILLAS.items():
        for fila in filas:
            plantilla = plantillas[contador % len(plantillas)]
            pregunta = plantilla.format(nombre=fila['nombre'])
            filas_csv.append(
                {
                    'id': f'poc-{contador:04d}',
                    'intencion_objetivo': intencion,
                    'pregunta': pregunta,
                    'tramite_esperado_id': fila['id'],
                    'tramite_esperado_nombre': fila['nombre'],
                }
            )
            contador += 1

    rng.shuffle(filas_csv)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SALIDA, 'w', encoding='utf-8', newline='') as fh:
        escritor = csv.DictWriter(
            fh,
            fieldnames=[
                'id',
                'intencion_objetivo',
                'pregunta',
                'tramite_esperado_id',
                'tramite_esperado_nombre',
            ],
        )
        escritor.writeheader()
        escritor.writerows(filas_csv)

    por_intencion: dict[str, int] = {}
    for fila in filas_csv:
        por_intencion[fila['intencion_objetivo']] = (
            por_intencion.get(fila['intencion_objetivo'], 0) + 1
        )
    print(f'Escritas {len(filas_csv)} consultas en {SALIDA}')
    print('Distribución:', por_intencion)


if __name__ == '__main__':
    asyncio.run(main())
