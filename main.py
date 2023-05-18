from subprocess import check_output
import configparser
from FloorplanToBlenderLib import (
    IO,
    config,
    const,
    execution,
    floorplan,
    stacking,
)  # floorplan to blender lib
import os
import sys
"""
Create Blender Project from floorplan
This file contains a simple example implementation of creations of 3d models from
floorplans. You will need blender and an image of a floorplan to make this work.

FloorplanToBlender3d
"""


"""
Purpose of function below is to check if Folder "Target" exists and create the directory 
if it doesn't exist. And also for naming the final output like "floorplan.blend"

target_base = /Target/ + floorplan
target_path = Target/floorplan + .blend
"""
def create_blender_project(data_paths):
    if not os.path.exists("." + target_folder):
        os.makedirs("." + target_folder)

    target_base = target_folder + const.TARGET_NAME
    target_path = target_base + const.BASE_FORMAT
    target_path = (
        IO.get_next_target_base_name(target_base, target_path) + const.BASE_FORMAT
    )

    # Create blender project
    check_output(
        [
            blender_install_path,
            "-noaudio",  # this is a dockerfile ubuntu hax fix
            "--background",
            "--python",
            blender_script_path,
            program_path,  # Send this as parameter to script
            target_path,
        ]
        + data_paths
    )

    outformat = config.get(
        const.SYSTEM_CONFIG_FILE_NAME, "SYSTEM", const.STR_OUT_FORMAT
    ).replace('"', "")
    # Transform .blend project to another format!
    if outformat != ".blend":
        check_output(
            [
                blender_install_path,
                "-noaudio",  # this is a dockerfile ubuntu hax fix
                "--background",
                "--python",
                "./Blender/blender_export_any.py",
                "." + target_path,
                outformat,
                target_base + outformat,
            ]
        )
        print("Object created at:" + program_path + target_base + outformat)

    print("Project created at: " + program_path + target_path)
    command = blender_install_path + " " + target_path
    check_output(command)


if __name__ == "__main__":
    """
    Do not change variables in this file but rather in ./config.ini or ./FloorplanToBlenderLib/const.py
    """
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    blender_install_path = ""
    data_folder = const.BASE_PATH
    target_folder = const.TARGET_PATH
    blender_install_path = config.get_default_blender_installation_path()
    floorplans = []
    image_paths = []
    program_path = os.path.dirname(os.path.realpath(__file__))
    blender_script_path = const.BLENDER_SCRIPT_PATH
    data_paths = list()

    # Detect where/if blender is installed on pc
    auto_blender_install_path = (
        IO.blender_installed()
    )  

    if auto_blender_install_path is not None:
        blender_install_path = auto_blender_install_path

    print(
        "Blender installation path "
        + blender_install_path
        + " "
    )

    print("Selected image: " + image_path)
    configp = configparser.ConfigParser()
    config_path = "./Configs/default.ini"
    configp.read(config_path)
    configp.set('IMAGE', 'image_path', '"' + image_path + '"')

    with open(config_path, 'w') as config_file:
        configp.write(config_file)
    
    floorplans.append(floorplan.new_floorplan(config_path))


    print(
        "This program is about to run and create blender3d project."
    )
      

    print("")
    print("Generating datafiles in folder: Data")
    print("")
    print("Cleaning datafiles")
    print("")
    print("Cleaned all cached data")

    IO.clean_data_folder(data_folder)
    if len(floorplans) > 1:
        data_paths.append(execution.simple_single(f) for f in floorplans)
    else:
        data_paths = [execution.simple_single(floorplans[0])]

    print("")
    print("Blender project created.")
    print("")

    if isinstance(data_paths[0], list):
        for paths in data_paths:
            create_blender_project(paths)
    else:
        create_blender_project(data_paths)




