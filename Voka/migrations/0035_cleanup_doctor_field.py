from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Voka', '0034_alter_appointment_options_and_more'),  # или твоя последняя миграция
    ]

    operations = [
        migrations.RunSQL(
            """
            SET @exists := (
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'Voka_appointment' AND COLUMN_NAME = 'doctor_ru_id'
            );
            SET @q := IF(@exists > 0, 'ALTER TABLE Voka_appointment DROP COLUMN doctor_ru_id', 'SELECT 1');
            PREPARE stmt FROM @q;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;

            SET @exists := (
                SELECT COUNT(*)
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'Voka_appointment' AND COLUMN_NAME = 'doctor_en_id'
            );
            SET @q := IF(@exists > 0, 'ALTER TABLE Voka_appointment DROP COLUMN doctor_en_id', 'SELECT 1');
            PREPARE stmt FROM @q;
            EXECUTE stmt;
            DEALLOCATE PREPARE stmt;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]