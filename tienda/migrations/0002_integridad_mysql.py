from django.db import migrations


def asegurar_integridad(apps, schema_editor):
    connection = schema_editor.connection
    if connection.vendor != 'mysql':
        return
    models = list(apps.get_models(include_auto_created=True))
    q = schema_editor.quote_name
    with connection.cursor() as cursor:
        tables = set(connection.introspection.table_names(cursor))
        # Comprobar datos antes de cambiar el motor o agregar restricciones.
        for model in models:
            if model._meta.db_table not in tables:
                continue
            for field in model._meta.local_fields:
                if not field.is_relation or not field.db_constraint or not field.remote_field:
                    continue
                target = field.remote_field.model
                if target._meta.db_table not in tables:
                    continue
                cursor.execute(
                    f'SELECT COUNT(*) FROM {q(model._meta.db_table)} s '
                    f'LEFT JOIN {q(target._meta.db_table)} t '
                    f'ON s.{q(field.column)} = t.{q(field.target_field.column)} '
                    f'WHERE s.{q(field.column)} IS NOT NULL '
                    f'AND t.{q(field.target_field.column)} IS NULL'
                )
                if cursor.fetchone()[0]:
                    raise RuntimeError(f'Hay referencias huérfanas en {model._meta.db_table}.{field.column}; corregir antes de migrar.')
        for table in sorted(tables):
            cursor.execute('SELECT ENGINE FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s', [table])
            if cursor.fetchone()[0].upper() != 'INNODB':
                schema_editor.execute(f'ALTER TABLE {q(table)} ENGINE=InnoDB')
        # MyISAM ignora FOREIGN KEY: restaurarlas después de convertir las tablas.
        for model in models:
            if model._meta.db_table not in tables:
                continue
            constraints = connection.introspection.get_constraints(cursor, model._meta.db_table)
            for field in model._meta.local_fields:
                if not field.is_relation or not field.db_constraint or not field.remote_field:
                    continue
                if field.remote_field.model._meta.db_table not in tables:
                    continue
                if any(v.get('foreign_key') and v['columns'] == [field.column] for v in constraints.values()):
                    continue
                schema_editor.execute(schema_editor._create_fk_sql(model, field, '_fk_fase4'))


class Migration(migrations.Migration):
    atomic = False
    dependencies = [('tienda', '0001_initial')]
    operations = [migrations.RunPython(asegurar_integridad, reverse_code=migrations.RunPython.noop)]
