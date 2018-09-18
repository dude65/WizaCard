#!/usr/bin/env python3
import logging
import os
import shutil
import sys


# Copy new files (does not delete or rewrite old content)
# FIXME copy files vs directory
def copy_files_recursively(src, dest, local_logger):
    logger.info("Entering source directory %s, destination directory %s", src, dest)
    for file in os.listdir(src):
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest, file)

        if os.path.isdir(src_path):
            if os.path.isdir(dest_path):
                logger.info("Directory %s exists, descending into the directory.", file)
                copy_files_recursively(src_path, dest_path, local_logger.getChild(file))
            else:
                logger.info("Copying directory %s", file)
                shutil.copytree(src_path, dest_path)
        else:
            new_name = compute_next_name(dest, file)

            if new_name is None:
                logger.info("File %s already exists.", file)
                continue
            elif new_name == file:
                logger.info("Copying %s.", file)
            else:
                logger.info("Copying %s as %s.", file, new_name)

            dest_file = os.path.join(dest, new_name)
            shutil.copy2(src_path, dest_file)


# TODO resolving names and content in cycle, check if files are same
def compute_next_name(dest, name):
    if os.path.exists(os.path.join(dest, name)):
        return None

    return name


print("Welcome! WizaCard program copies your precious files into your selected destination.")
print("However, in the future this piece of program should be a part of solution for automatic backup of photos "
      "from SD cards that will be running on Raspberry Pi.")
print("This project exists thanks to the fact that somebody stupid has lost his own camera in a couch during "
      "the way home from a vacation.")
print("========================")
print("Specify source directory:")
src = sys.stdin.readline().rstrip('\n')
print("Source directory is: " + src)

print("Specify destination directory:")
dest = sys.stdin.readline().rstrip('\n')
print("Destination directory is: " + dest)

print("Thank you. Backing up your files...")


h = logging.StreamHandler(sys.stdout)
h.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger("FileBackup")
logger.setLevel(logging.DEBUG)
logger.addHandler(h)

copy_files_recursively(src, dest, logger)

print("Done")