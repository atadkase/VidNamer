# VidNamer
## A tool for renaming GoPro® video files
The [naming schema used by GoPro® cameras](https://community.gopro.com/t5/en/GoPro-Camera-File-Naming-Convention/ta-p/390220) is unintuitive for video editing. After agonizing over the 
filenames for a long time when working with a larger project, I decided to write a script to make the 
names more useable. This tool is an extension of that script. 
Cameras older than HERO8 Black are not supported. Please file an issue if you need it.

## Installation
I recommend using the script directly with Python with the following command:
```shell
py vidnamer.py
```
If you do not have python installed, please follow instructions here: [Download Python](https://www.python.org/downloads/)

It will launch an interactive GUI which can be used to automatically rename your video files.
I've written this to be OS independent and I've tested it manually on Windows 10. YMMV for other platforms.

If you do not want to install python, you can grab a compiled executable zip here: [Download VidNamer for Windows](https://github.com/atadkase/VidNamer/releases/download/v1.0/vidnamer_v1.0_windows.zip)

Github does not provide a permanent URL for the latest artifact, so I have to update this link manually. 

## Using the tool
### Backup all files before using this tool!
I cannot stress the importance of backing up your files more. This tool is not written to production standards and may have bugs. Use it at your own risk.

Now that we've gotten the disclaimer out of the way, we can talk about the operation of the tool.
The tool has a simple UI:
![VidNamer_ui](/screenshots/ui_pic.JPG "VidNamer UI")

The `Browse Directory` button allows you to select the directory containing the videos. The tool will not process directories inside that directory. Please file an issue if you need recursion.

You can then set each of the following options:

- `Ask for custom prefix per video group`: For each new video group the tool detects, it will prompt for a custom prefix to add to the video name. The prefix will be suffixed by the chapter numbers from the source video files for getting the new names.
- `Create a new directory per video group`: This will create a new directory for each new group and move the renamed files to that directory.
- `Copy videos instead of moving`: I highly recommend keeping this box checked unless you have your files backed up somewhere. If you uncheck this, the tool will just rename the files, but if the filenames clash, it may overwrite existing files based on your selection. If you do not have any clashing names, it is much faster to disable this option.
- `Use auto numbering scheme for filename conflicts`: Only disable this if you know that you want to overwrite existing files. If this option is enabled the tool will read the latest files in the target directory and autoincrement the chapter index to avoid filename conflicts.
- `Ask before writing to an existing directory`: Will prompt the user when the target directory already exists.

Once you've selected your target options, you can hit `Start Renaming!` and wait for the completion dialog box.

## Contributing
I am accepting contributions to this project. If you want to add a feature or fix a bug, please create a GitHub issue and a corresponding Pull Request from your fork. 

## Donations
If this tool helped you save time, please consider donating to any of the COVID-19 relief efforts in India. Every bit helps: [Donation Link](https://www.ketto.org/fundraiser/mission-oxygen-helping-hospitals-to-save-lives?payment=form)

## Attributions
A big thank you to [JackMcKew](https://github.com/JackMcKew) for the Pyinstaller-Windows Action which is being used to build the project's Windows executables.

This product and/or service is not affiliated with, endorsed by or in any 
way associated with GoPro Inc. or its products and services. GoPro, HERO 
and their respective logos are trademarks or registered trademarks of GoPro, Inc.

## License
Copyright 2021 Ashutosh Tadkase

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
