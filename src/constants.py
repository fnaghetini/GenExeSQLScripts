# Convenção de data
DATE_CONVENTION = 103

# Relação tabela -> chave primária
TABLE_KEY_RELATIONSHIP = {'DRILL_HOLE': ['hole_number'],
                          'DRILL_HOLE_COORDINATE': ['hole_number'],
                          'DRILL_HOLE_DIRECTION': ['hole_number', 'depth', 'test_type_code'],
                          'HOLE_ASSAY_SAMPLE': ['sample_number'],
                          'HOLE_INTERVAL': ['hole_number', 'depth_from'],
                          'UDEF_CORE_RECOVERY': ['hole_number', 'depth_from'],
                          'UDEF_GEOLOGY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOLOGY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOTECNIC': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOTECHNIC': ['hole_number', 'depth_from'],
                          'UDEF_DHL_DENSITY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_DENSITY_QAQC': ['sample_number'],
                          'UDEF_DHL_LOG_QAQC_MARK_LINE': ['hole_number', 'depth_from']}

# Limite de linhas para scripts
INSERT_SCRIPT_ROWS_LIMIT = 20_000
UPDATE_SCRIPT_ROWS_LIMIT = 10_000
