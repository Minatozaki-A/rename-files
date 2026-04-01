from pathlib import Path
from core.actions import (find_ssd_mount_point,
                        get_name_directories,
                        get_name_files,
                        organize_for_depth_and_alphabetical,
                        resolve_name_path)
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

    directories = organize_for_depth_and_alphabetical(
        get_name_directories(ssd_path, config_path, "ignore_directories", ignore_list))

    for file in files:
        new_path_file = resolve_name_path(file)
        if new_path_file and new_path_file != file:
            print(f"{file}->\n{new_path_file}")
            # file.rename(new_path_file)

    

    for directory in directories:
        new_path_directory = resolve_name_path(directory)
        if new_path_directory and new_path_directory != directory:
            print(f"{new_path_directory}")
            # directory.rename(new_path_directory)

if __name__ == "__main__":
    main()
