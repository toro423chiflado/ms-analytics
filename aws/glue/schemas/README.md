# Esquemas JSON para Glue (manual)

Estos archivos siguen el formato de "Edit schema as JSON" de AWS Glue.

Uso recomendado:

1. Crear database en Glue (por ejemplo `urate_analytics`).
2. Crear una tabla por dataset y pegar el JSON correspondiente.
3. Apuntar cada tabla al prefijo S3 correcto (`s3://<bucket>/raw/...`).
4. Validar que los nombres de columna coincidan con el header real del CSV.

Notas:

- Se incluye un esquema por cada CSV esperado (hasta 9 tablas).
- Si una columna real difiere, actualiza nombre/tipo en Glue.
