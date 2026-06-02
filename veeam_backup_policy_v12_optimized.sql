-- ============================================================================
-- VEEAM BACKUP & REPLICATION v12 - OPTIMIZED BACKUP POLICY EXTRACTION
-- ============================================================================
-- Purpose: Extract comprehensive backup job configuration and retention policies
-- Author: Consultor de Veeam
-- Date: 2026-06-02
-- ============================================================================

WITH job_details AS (
    SELECT
        j.id,
        j.name::text                                        AS job_name,
        j.description::text                                 AS job_description,
        j.type,
        CASE j.type
            WHEN 0     THEN 'VMware Backup'
            WHEN 1     THEN 'VMware Replication'
            WHEN 2     THEN 'VMware Copy'
            WHEN 24    THEN 'VMware Backup (CDP)'
            WHEN 28    THEN 'NAS Backup'
            WHEN 52    THEN 'Backup Copy (Agent)'
            WHEN 63    THEN 'Backup Copy'
            WHEN 65    THEN 'Backup Copy (Seed)'
            WHEN 70    THEN 'Backup to Tape'
            WHEN 100   THEN 'File to Tape'
            WHEN 4000  THEN 'Agent Backup (Windows)'
            WHEN 12000 THEN 'Agent Policy (Windows)'
            WHEN 12003 THEN 'Agent Policy (Linux)'
            WHEN 13000 THEN 'Agent Backup (Windows Managed)'
            WHEN 13003 THEN 'Agent Backup (Linux Managed)'
            WHEN 22000 THEN 'Plugin Backup'
            ELSE j.type::text
        END                                                 AS job_type,
        j.options::xml                                      AS options_xml,
        j.schedule::xml                                     AS schedule_xml,
        j.schedule_enabled,
        j.target_host_id,
        j.repository_id,
        j.is_deleted
    FROM
        public.bjobs j
    WHERE
        j.is_deleted = false
),
backup_strategy AS (
    SELECT
        id,
        CASE
            WHEN (xpath('//Algorithm/text()', options_xml))[1]::text = 'Increment'
                 AND (xpath('//FullBackupScheduleKind/text()', options_xml))[1]::text = 'Daily'
                 AND (xpath('//TransformFullToSyntethic/text()', options_xml))[1]::text = 'True'
                THEN 'Incremental + Synthetic Full Diario'
            WHEN (xpath('//Algorithm/text()', options_xml))[1]::text = 'Increment'
                 AND (xpath('//FullBackupScheduleKind/text()', options_xml))[1]::text = 'Monthly'
                 AND (xpath('//TransformFullToSyntethic/text()', options_xml))[1]::text = 'True'
                THEN 'Incremental + Synthetic Full Mensual'
            WHEN (xpath('//Algorithm/text()', options_xml))[1]::text = 'Increment'
                 AND (xpath('//FullBackupScheduleKind/text()', options_xml))[1]::text = 'Monthly'
                THEN 'Incremental + Full Activo Mensual'
            WHEN (xpath('//Algorithm/text()', options_xml))[1]::text IS NULL
                 AND (xpath('//FullBackupScheduleKind/text()', options_xml))[1]::text = 'Daily'
                THEN 'Full Diario'
            WHEN (xpath('//Algorithm/text()', options_xml))[1]::text IS NULL
                 AND (xpath('//FullBackupScheduleKind/text()', options_xml))[1]::text = 'Monthly'
                THEN 'Full Mensual'
            WHEN type IN (63, 65, 52)
                THEN 'Backup Copy'
            WHEN type IN (70, 100)
                THEN 'Backup to Tape'
            WHEN type IN (4000, 12000, 12003, 13000, 13003)
                THEN 'Agent Backup'
            WHEN type = 28
                THEN 'NAS Backup'
            WHEN type = 22000
                THEN 'Plugin Backup'
            ELSE 'Ver configuración manual'
        END AS tipo_respaldo,
        CASE
            WHEN (xpath('//OptionsDaily/Kind/text()', schedule_xml))[1]::text = 'Everyday'
                THEN 'Lunes a Domingo'
            ELSE COALESCE(
                array_to_string(
                    xpath('//OptionsDaily/Days/DayOfWeek/text()', schedule_xml)::text[], ', '
                ),
                'No configurado'
            )
        END AS dias_ejecucion,
        COALESCE(
            split_part(
                (xpath('//OptionsDaily/Time/text()', schedule_xml))[1]::text, 'T', 2
            ),
            'No configurado'
        ) AS hora_ejecucion
    FROM
        job_details
),
retention_config AS (
    SELECT
        id,
        COALESCE(
            (xpath('//RetainCycles/text()', options_xml))[1]::text,
            (xpath('//SimpleRetentionRestorePoints/text()', options_xml))[1]::text,
            (xpath('//RetainDays/text()', options_xml))[1]::text,
            'No configurado'
        )::text AS retencion_disco,
        COALESCE(
            (xpath('//GfsPolicy/@IsEnabled', options_xml))[1]::text,
            'false'
        )::boolean AS gfs_enabled,
        NULLIF(
            (xpath('//Weekly/@KeepBackupsForNumberOfWeeks', options_xml))[1]::text,
            ''
        )::integer AS gfs_semanal,
        NULLIF(
            (xpath('//Monthly/@KeepBackupsForNumberOfMonths', options_xml))[1]::text,
            ''
        )::integer AS gfs_mensual,
        NULLIF(
            (xpath('//Yearly/@KeepBackupsForNumberOfYears', options_xml))[1]::text,
            ''
        )::integer AS gfs_anual,
        COALESCE(
            (xpath('//StorageEncryptionEnabled/text()', options_xml))[1]::text,
            'false'
        )::boolean AS encriptacion,
        COALESCE(
            (xpath('//EnableDeduplication/text()', options_xml))[1]::text,
            'false'
        )::boolean AS deduplicacion
    FROM
        job_details
),
host_info AS (
    SELECT
        id,
        name::text AS vcenter_host,
        CASE type
            WHEN 1  THEN 'vCenter'
            WHEN 6  THEN 'ESXi'
            WHEN 10 THEN 'Veeam Server'
            ELSE type::text
        END AS host_type
    FROM
        public.hosts
),
repository_info AS (
    SELECT
        id,
        name::text AS repositorio_nombre,
        path::text AS repositorio_ruta,
        CASE type
            WHEN 0  THEN 'Windows Repository'
            WHEN 8  THEN 'ONTAP Snapshot'
            WHEN 10 THEN 'Scale-out Backup Repository (SOBR)'
            WHEN 12 THEN 'Azure Blob Storage'
            WHEN 35 THEN 'Linux Repository'
            ELSE type::text
        END AS repositorio_tipo
    FROM
        public.backuprepositories
)
-- ============================================================================
-- MAIN QUERY - POLITICA DE BACKUPS
-- ============================================================================
SELECT
    j.job_name,
    j.job_description,
    j.job_type,
    bs.tipo_respaldo,
    bs.dias_ejecucion,
    bs.hora_ejecucion,
    j.schedule_enabled,
    rc.retencion_disco,
    rc.gfs_enabled,
    rc.gfs_semanal,
    rc.gfs_mensual,
    rc.gfs_anual,
    rc.encriptacion,
    rc.deduplicacion,
    h.vcenter_host,
    h.host_type,
    r.repositorio_nombre,
    r.repositorio_ruta,
    r.repositorio_tipo,
    -- Columnas adicionales de auditoría
    CASE
        WHEN rc.gfs_enabled THEN 'GFS Configurado'
        ELSE 'Sin GFS'
    END AS politica_retencion,
    CASE
        WHEN rc.encriptacion THEN '✓ Encriptado'
        ELSE 'Sin Encriptación'
    END AS seguridad,
    CASE
        WHEN rc.deduplicacion THEN '✓ Deduplicación Activa'
        ELSE 'Deduplicación Desactiva'
    END AS optimizacion_almacenamiento
FROM
    job_details j
    LEFT JOIN backup_strategy bs         ON j.id = bs.id
    LEFT JOIN retention_config rc        ON j.id = rc.id
    LEFT JOIN host_info h                ON j.target_host_id = h.id
    LEFT JOIN repository_info r          ON j.repository_id = r.id
ORDER BY
    j.job_type, j.job_name;
