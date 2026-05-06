# ms-analytics

Ingesta de datos para URATE con estrategia **pull 100%** de registros por microservicio.

Estructura base alineada a la rubrica:

- 3 contenedores Docker Python (uno por microservicio).
- Carga de archivos CSV/JSON a bucket S3.
- Insumos para catalogo en AWS Glue.
- Consultas y vistas para AWS Athena.
- Documento base para diagrama Entidad/Relacion del data catalog.

## Estructura

```text
ms-analytics/
  containers/
    ingest-users/
    ingest-content/
    ingest-reviews/
  aws/
    glue/
    athena/
  docs/
    er/
```

## Flujo de despliegue sugerido

1. Build de cada contenedor.
2. Push de imagenes a Docker Hub.
3. Pull de imagenes desde la MV "ingesta" en AWS.
4. Ejecucion de jobs de ingesta por cron/systemd/docker compose.

## Nota

Cada contenedor tiene su propio `Dockerfile`, `requirements.txt` y script `src/main.py` para que puedas publicarlos por separado.

## Alineacion con `docker-compose.db.yml`

- `ingest-users` -> PostgreSQL (`auth_db`) en puerto `5432`.
- `ingest-content` -> MySQL (`academic_db`) en puerto `3306`.
- `ingest-reviews` -> MongoDB (`reviews_db`) en puerto `27017`.

Si analytics corre en otra MV, usa la IP privada de la MV de bases como `DB_HOST` en cada `.env`.
Semáforo de dificultad y accesibilidad, Incluye los 3 contenedores de ingesta y queries Athena.
