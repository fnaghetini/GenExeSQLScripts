# Convenção de data
DATE_CONVENTIONS = {'mm/dd/yyyy': ['101', '%m/%d/%Y'],
                    'yyyy.mm.dd': ['102', '%Y.%m.%d'],
                    'dd/mm/yyyy': ['103', '%d/%m/%Y'],
                    'dd.mm.yyyy': ['104', '%d.%m.%Y'],
                    'dd-mm-yyyy': ['105', '%d-%m-%Y'],
                    'mm-dd-yyyy': ['110', '%m-%d-%Y'],
                    'yyyy/mm/dd': ['111', '%Y/%m/%d'],
                    'yyyy-mm-dd': ['23', '%Y-%m-%d'],
                    'yyyy-dd-mm': ['31', '%Y-%d-%m'],
                    'mm-yyyy-dd': ['33', '%m-%Y-%d'],
                    'dd-yyyy-mm': ['35', '%d-%Y-%m']}

# Relação tabela -> chave primária
TABLE_KEY_RELATIONSHIP = {'DRILL_HOLE': ['hole_number'],
                          'DRILL_HOLE_COORDINATE': ['hole_number'],
                          'DRILL_HOLE_DIRECTION': ['hole_number', 'depth', 'test_type_code'],
                          'HOLE_ASSAY_SAMPLE': ['sample_number'],
                          'HOLE_INTERVAL': ['hole_number', 'depth_from'],
                          'UDEF_CORE_RECOVERY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_CORE_RECOVERY': ['hole_number', 'depth_from'],
                          'UDEF_GEOLOGY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOLOGY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOTECNIC': ['hole_number', 'depth_from'],
                          'UDEF_DHL_GEOTECHNIC': ['hole_number', 'depth_from'],
                          'UDEF_DHL_DENSITY': ['hole_number', 'depth_from'],
                          'UDEF_DHL_DENSITY_QAQC': ['sample_number'],
                          'UDEF_DHL_LOG_QAQC_MARK_LINE': ['hole_number', 'depth_from'],
                          'HOLE_ASSAY_STANDARDS': ['sample_number'],
                          'sstn_surface_samples': ['sample_number']}

# Limite de linhas para scripts
INSERT_SCRIPT_ROWS_LIMIT = 20_000
UPDATE_SCRIPT_ROWS_LIMIT = 10_000
