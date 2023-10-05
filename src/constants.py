# log files paths
GENERATE_SCRIPTS_LOG_PATH = 'log/generate_scripts.log'
EXECUTE_SCRIPTS_LOG_PATH = 'log/execute_scripts.log'

# Date conventions
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

# Table-key relationship
TABLE_KEY_RELATIONSHIP = {'drill_hole': ['hole_number'],
                          'drill_hole_coordinate': ['hole_number', 'coord_type_code'],
                          'drill_hole_direction': ['hole_number', 'depth', 'test_type_code'],
                          'hole_interval': ['hole_number', 'depth_from'],
                          'hole_assay_sample': ['sample_number'],
                          'hole_assay_standards': ['sample_number'],
                          'sstn_surface_samples': ['sample_number'],
                          'udef_core_recovery': ['hole_number', 'depth_from'],
                          'udef_dhl_core_recovery': ['hole_number', 'depth_from'],
                          'udef_geology': ['hole_number', 'depth_from'],
                          'udef_dhl_geology': ['hole_number', 'depth_from'],
                          'udef_dhl_geotecnic': ['hole_number', 'depth_from'],
                          'udef_dhl_geotechnic': ['hole_number', 'depth_from'],
                          'udef_dhl_density': ['hole_number', 'depth_from'],
                          'udef_dhl_density_qaqc': ['hole_number', 'depth_from', 'assay_type'],
                          'udef_dhl_log_qaqc_mark_line': ['hole_number', 'depth_from'],
                          'udef_dhl_alteration': ['hole_number', 'depth_from']}

# Row limits for script types
INSERT_SCRIPT_ROWS_LIMIT = 20_000
UPDATE_SCRIPT_ROWS_LIMIT = 10_000
DELETE_SCRIPT_ROWS_LIMIT = 10_000
