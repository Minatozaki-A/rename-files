from pathlib import Path
import argparse
import logging
from core.actions import (find_ssd_mount_point,
                        get_name_directories,
                        get_name_files,
                        organize_for_depth_and_alphabetical,
                        rename_files_and_directories)
# from core.scanner import scanner_structure_directories
from core.config_loader import get_cached_config_value


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Rename your files and directories")
    parser.add_argument('--run', action='store_true', help='Run the script')
    args = parser.parse_args()

    dry_run = not args.run

    config_path = Path.cwd() / "config.json"
    mount_label = get_cached_config_value(config_path, "mount_point_label")
    ignore_list = get_cached_config_value(config_path, "ignore") or []

    ssd_path = find_ssd_mount_point(mount_label)

    if not ssd_path:
        logging.error("Drive with label '%s' not found in disk partitions", mount_label)
        return


    files = organize_for_depth_and_alphabetical(
        get_name_files(ssd_path, config_path, "ignore_directories", ignore_list))

    directories = organize_for_depth_and_alphabetical(
        get_name_directories(ssd_path, config_path, "ignore_directories", ignore_list))

    """for file in files:
        new_path_file = resolve_name_path(file)
        if new_path_file and new_path_file != file:
            if dry_run:
                print(f"[Simulation]:{file.name} -> {new_path_file.name}")
            else:
                print(f"[Execution]:{file.name} -> {new_path_file.name}")
                file.rename(new_path_file)"""
    rename_files_and_directories(files, dry_run)
    rename_files_and_directories(directories, dry_run)

    """for directory in directories:
        new_path_directory = resolve_name_path(directory)
        if new_path_directory and new_path_directory != directory:
            if dry_run:
                print(f"{directory.name} -> {new_path_directory.name}")
            else:
                print(f"[Execution]:{directory.name} -> {new_path_directory.name}")
                directory.rename(new_path_directory)"""

if __name__ == "__main__":
    main()
