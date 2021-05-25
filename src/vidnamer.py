#!/usr/bin/env python
"""
VidNamer: Video renamer for GoPro® video files
Copyright 2021 Ashutosh Tadkase

License:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

This product and/or service is not affiliated with, endorsed by or in any 
way associated with GoPro Inc. or its products and services. GoPro, HERO 
and their respective logos are trademarks or registered trademarks of GoPro, Inc.
"""

import os
import tkinter as tk
from tkinter import (
    BooleanVar,
    simpledialog,
    messagebox,
    filedialog,
    ttk,
    StringVar,
    Label,
    Entry,
)
import shutil


class VidNamer:
    def __init__(
        self,
        get_user_input_per_group=True,
        copy_instead_of_move=False,
        create_new_dir_per_group=True,
        check_dir_merge=False,
        check_automated_numbering=False,
    ):
        self.get_user_input_per_group = get_user_input_per_group
        self.copy_instead_of_move = copy_instead_of_move
        self.create_new_dir_per_group = create_new_dir_per_group
        self.check_dir_merge = check_dir_merge
        self.check_automated_numbering = check_automated_numbering

    @staticmethod
    def get_group_dict(
        dirpath, group_regex=r"G[A-Z]([0-9][0-9])([0-9]+)", reverse_group=False
    ):
        """Get group dict inside the path"""
        import re

        f = [
            filename
            for filename in os.listdir(dirpath)
            if os.path.isfile(os.path.join(dirpath, filename))
            and filename.endswith(("mp4", "MP4"))
        ]
        group_dict = (
            {}
        )  # Dictionary containing group to chapter and file mapping. Useful for splitting groups and renaming.
        for filename in f:
            match = re.match(group_regex, filename)
            if match:
                chapter, group = match.groups()
                if reverse_group:
                    group, chapter = match.groups()
                # TODO - Pitfall- should add dirpath too to the filename
                if group not in group_dict:
                    group_dict[group] = [(chapter, filename)]
                else:
                    group_dict[group].append((chapter, filename))
        return group_dict

    def rename_group(self, dirpath):
        error = False
        if dirpath is None or dirpath == "":
            messagebox.showerror(
                title="No directory specified", message="Please specify directory!"
            )
            return True
        group_dict = self.get_group_dict(dirpath)
        if not group_dict:
            messagebox.showerror(
                title="No videos found",
                message="No compatible videos found in provided directory!",
            )
            return True
        print(group_dict)
        prev_group_prefix = None
        for group, file_list in group_dict.items():
            group_prefix = prev_group_prefix if prev_group_prefix else group

            # 1. Check if user wants to provide custom input per group
            if self.get_user_input_per_group:
                print("Checking user input per flag")
                group_prefix = simpledialog.askstring(
                    title="Custom prefix for renaming",
                    prompt=(
                        "Found new video group (starting at path "
                        f"{os.path.join(dirpath, group_dict[group][0][1])})."
                        " Replace initial value if you need custom prefix"
                    ),
                    initialvalue=group_prefix,
                )
                prev_group_prefix = group_prefix if group_prefix != group else None
                if not group_prefix:
                    # User pressed cancel
                    print("Operation canceled. Exiting")
                    break

            # 2. Create new directory if required
            new_directory = dirpath
            if self.create_new_dir_per_group:
                print("Creating new dir per flag")
                new_directory = os.path.join(dirpath, group_prefix)
                try:
                    os.mkdir(new_directory)
                except:
                    merge_existing = "yes"

                    if self.check_dir_merge:
                        print("Creating new dir per flag")
                        merge_existing = messagebox.askquestion(
                            title="Directory exists",
                            message=f"Found existing directory at {new_directory}. Do you want to merge contents?",
                        )
                    if merge_existing == "no":
                        # TODO - Currently just skipping group on canceling.
                        # Need to enter UI loop for getting an alternative path
                        print(f"Operation Canceled. Skipping group {group}")
                        continue

            # 3. Now copy all video files into selected directory!
            new_chapter = None
            for chapter, filename in file_list:
                # Chapter needs to be bumped up to the max chapter in the new dir if overlapping files exist
                new_filename = (
                    f"{group_prefix}_{chapter}.MP4"
                    if new_chapter is None
                    else f"{group_prefix}_{new_chapter}.MP4"
                )
                source_path = os.path.join(dirpath, filename)
                dest_path = os.path.join(new_directory, new_filename)
                if os.path.exists(dest_path):
                    overwrite_existing = "no"
                    if self.check_automated_numbering:
                        overwrite_existing = messagebox.askquestion(
                            title="File exists",
                            message=f"Found existing video at {dest_path}. "
                            f"Do you want to overwrite it with {source_path}?"
                            "\nIf you select 'No', an automated indexing scheme will be used",
                        )
                    else:
                        print("Using automated numbering per flag")
                    if overwrite_existing == "no":
                        # new_filename needs to be set to one index higher than the existing files
                        existing_group_dict = self.get_group_dict(
                            new_directory,
                            rf"({group_prefix})_([0-9]+).MP4",
                            reverse_group=True,
                        )
                        print(existing_group_dict)
                        # Find highest index
                        value_tuples = list(existing_group_dict.values())[0]

                        max_index = max(
                            [int(group_tuple[0]) for group_tuple in value_tuples]
                        )
                        new_chapter = max_index + 1
                        new_filename = (
                            f"{group_prefix}_{chapter}.MP4"
                            if new_chapter is None
                            else f"{group_prefix}_{new_chapter}.MP4"
                        )
                        dest_path = os.path.join(new_directory, new_filename)

                        if os.path.exists(dest_path):
                            # TODO - Currently just skipping group on canceling.
                            # Need to enter UI loop for getting an alternative path
                            print(f"Internal Error. Exiting")
                            break
                    elif overwrite_existing is None:
                        print(f"Skipping file: {filename}")
                        continue

                    print(dest_path)
                if self.copy_instead_of_move:
                    shutil.copy2(source_path, dest_path)
                else:
                    print("Moving per flag")
                    shutil.move(source_path, dest_path)

                if new_chapter:
                    new_chapter = new_chapter + 1
        return error


# Tkinter gui for interactive folder utility
root = tk.Tk()
# root.withdraw()
root.geometry("")
root.title("VidNamer")
# Code from: https://stackoverflow.com/questions/51877124/how-to-select-a-directory-and-store-it-into-a-variable-in-tkinter/51877299
def getVideoDirectory():
    directory = filedialog.askdirectory()
    videoDirectory.set(directory)


def renameVideos():
    btnBrowse.config(state="disabled")
    btnStartRename.config(state="disabled")
    app.check_automated_numbering = not bool(use_automated_numbering_scheme.get())
    app.check_dir_merge = bool(check_before_dir_merge.get())
    app.get_user_input_per_group = bool(user_input_per_group.get())
    app.copy_instead_of_move = bool(copy_instead_of_move.get())
    app.create_new_dir_per_group = bool(new_dir_per_group.get())
    error = app.rename_group(videoDirectory.get())

    if not error:
        messagebox.showinfo(root, message="Videos Renamed!")
    btnBrowse.config(state="enabled")
    btnStartRename.config(state="enabled")


videoDirectory = StringVar()
enter_dir_label = Label(root, text="Enter directory").grid(row=0, column=0)
enter_dir_textbox = Entry(root, textvariable=videoDirectory).grid(row=0, column=1)


# Browse Button
btnBrowse = ttk.Button(root, text="Browse Directory", command=getVideoDirectory)
btnBrowse.grid(row=0, column=3)


# Check boxes for renaming Options

# Check for user input per new group detected. If disabled, VidNamer will reverse 
# chapter and group and automatically generate new series.
# Defaults to True
user_input_per_group = BooleanVar(value=True)
ttk.Checkbutton(
    root, text="Ask for custom prefix per video group", variable=user_input_per_group
).grid(row=1, column=1)

# Check if user wants to create a new directory per video group. Defaults to true.
new_dir_per_group = BooleanVar(value=True)
ttk.Checkbutton(
    root, text="Create a new directory per video group", variable=new_dir_per_group
).grid(row=2, column=1)

# Check if user wants to make a copy instead of moving
copy_instead_of_move = BooleanVar(value=True)
ttk.Checkbutton(
    root,
    text="Copy videos instead of moving\n[Recommended if not backed up]",
    variable=copy_instead_of_move,
).grid(row=3, column=1)


# Check if user wants to check before merging directories
use_automated_numbering_scheme = BooleanVar(value=True)
ttk.Checkbutton(
    root,
    text="Use auto numbering scheme for filename conflicts",
    variable=use_automated_numbering_scheme,
).grid(row=4, column=1)

# Check if user wants to check before merging directories
check_before_dir_merge = BooleanVar(value=False)
ttk.Checkbutton(
    root,
    text="Ask before writing to an existing directory",
    variable=check_before_dir_merge,
).grid(row=5, column=1)


backup_label = Label(root, text="Backup Files Before Use!!!", fg="Red")
backup_label.grid(row=6, column=1)
# Rename Button
btnStartRename = ttk.Button(root, text="Start Renaming!", command=renameVideos)
btnStartRename.grid(row=7, column=1)

app = VidNamer()

root.mainloop()
