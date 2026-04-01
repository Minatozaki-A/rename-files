from pathlib import Path
from core.actions import (find_ssd_mount_point,
                        get_name_directories,
                        get_name_files,
                        organize_for_depth_and_alphabetical,
                        resolve_name_file,
                        resolve_name_directory)
# from core.scanner import scanner_structure_directories
from core.config_loader import get_cached_config_value

def main():

    config_path = Path.cwd() / "config.json"
    mount_label = get_cached_config_value(config_path, "mount_point_label")
    ignore_list = get_cached_config_value(config_path, "ignore") or []

    ssd_path = find_ssd_mount_point(mount_label)

    if not ssd_path:
        print(f"Error: Drive with label not found: {mount_label}")
        return


    files = organize_for_depth_and_alphabetical(
        get_name_files(ssd_path, config_path, "ignore_directories", ignore_list))


    for file in files:
        print(f"{file}->\n{resolve_name_file(file)}")

    directories = organize_for_depth_and_alphabetical(
        get_name_directories(ssd_path, config_path, "ignore_directories", ignore_list))

    for directory in directories:
        print(f"{directory}->\n{resolve_name_directory(directory)}")


if __name__ == "__main__":
    main()
