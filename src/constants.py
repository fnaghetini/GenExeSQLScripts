# Relação tabela -> chave primária
TABLE_KEY_RELATIONSHIP = {'DRILL_HOLE': ['HOLE_NUMBER'],
                          'DRILL_HOLE_COORDINATE': ['HOLE_NUMBER'],
                          'DRILL_HOLE_DIRECTION': ['HOLE_NUMBER', 'DEPTH'],
                          'HOLE_ASSAY_SAMPLE': ['SAMPLE_NUMBER'],
                          'HOLE_INTERVAL': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_CORE_RECOVERY': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_GEOLOGY': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_DHL_GEOLOGY': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_DHL_GEOTECNIC': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_DHL_DENSITY': ['HOLE_NUMBER', 'depth_from'],
                          'UDEF_DHL_DENSITY_QAQC': ['HOLE_NUMBER', 'depth_from']}
