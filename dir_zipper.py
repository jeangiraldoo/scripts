from zipfile import ZipFile as Zip, ZIP_STORED
import os, shutil

"""
This script compresses the contents of a directory into a ZIP
file based on a file-count threshold.

If the number of files exceeds the threshold, it creates a ZIP
archive instead of simply copying the files.

For example, if you need to upload several files to a service
that only accepts one file per submission, running this script
will automatically bundle them into a single ZIP archive.
"""

opts = {
    "threshold": 2,
    "output_dir": "C:/Users/jeanp/Desktop/"
}

script_abs_path = os.path.abspath(__file__).replace("\\", "/")
script_name = os.path.basename(script_abs_path)

dir_abs_path = os.path.dirname(script_abs_path)
dir_name = os.path.basename(dir_abs_path)
dir_content = list(filter(lambda file: file != script_name and True, os.listdir(dir_abs_path)))

modes = {
    "zip": {
        "files": lambda obj: [file for file in dir_content if file not in obj.namelist()],
        "handler": lambda obj: (lambda file: obj.write(file, arcname=file)),
    },
    "move": {
        "files": lambda _: dir_content,
        "handler": lambda _: (lambda file: shutil.copy(file, opts['output_dir'])),
    }
}

mode = "move" if len(dir_content) <= opts["threshold"] else "zip"
mode_data = modes[mode]
zip_obj = (mode == "zip") and Zip(f"{opts['output_dir']}/{dir_name}.zip", "a", ZIP_STORED)

files, handler = mode_data["files"](zip_obj), mode_data["handler"](zip_obj)
for file in files: handler(file)
if zip_obj: zip_obj.close()

print("\n".join([
    f"Operation: {mode}",
    f"Threshold: {opts['threshold']}",
    f"Total files: {len(files)}",
    "",
    *sorted(files, key=lambda name: "." in name)
]))
