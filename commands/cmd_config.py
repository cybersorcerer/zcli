import sys
from commands.cmd_utils import (
    read_config,
    create_directory,
    get_default_profile,
    get_zcli_property,
)

CONFIG_CACHE_DIR = ".config/zcli"

JOBS_NOTIFICATION_SERVER = "http://mvsb.ruv.de:8176"
GLOBAL_CSI = "SMPE.GLOBAL.CSI"

config_file_path: str = create_directory(CONFIG_CACHE_DIR)

CONFIG = read_config(f"{config_file_path}/zcli.json")

if CONFIG:
    DEFAULT_ZOSMF_PROFILE: str = get_default_profile(
        config=CONFIG, profile_type="zosmf"
    )
    FILES_CACHE_DIR: str = get_zcli_property(config=CONFIG, prop_name="files_cache")
    if FILES_CACHE_DIR == "":
        FILES_CACHE_DIR = ".local/zcli/.cache/files"

    DATASET_CACHE_DIR: str = get_zcli_property(config=CONFIG, prop_name="dataset_cache")
    if DATASET_CACHE_DIR == "":
        DATSET_CACHE_DIR = ".local/zcli/.cache/datasets"

    JOBS_CACHE_DIR: str = get_zcli_property(config=CONFIG, prop_name="jobs_cache")
    if JOBS_CACHE_DIR == "":
        JOBS_CACHE_DIR = ".local/zcli/.cache/jobs"

    CERT_PATH: str = get_zcli_property(config=CONFIG, prop_name="cert_path")

else:
    sys.stderr.write(
        f"ZCLI-MAIN-003S Unable to read {config_file_path}/zcli.json, terminating rc = 16\n"
    )
    sys.exit(16)
