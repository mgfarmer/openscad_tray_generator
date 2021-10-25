import re
import os.path
import sys
import shutil
import math
import argparse
import subprocess
from os import path

global args
global number_of_trays
global number_of_trays_processed

global scale_units

def get_slice_cmd(model):
    return [r"slice.bat", model]

def slice(tray_file_path_3mf, tray_file_path_gcode):
    if args.slice and os.path.exists(tray_file_path_3mf) and (args.regen or not os.path.exists(tray_file_path_gcode)):
        slice_cmd = get_slice_cmd(tray_file_path_3mf)
        print("    ", f"Slicing: {tray_file_path_3mf}")
        print("    ", " ".join(slice_cmd))
        slicer = subprocess.run(slice_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True)
        print(slicer.stdout)
        if (slicer.returncode):
            print(slicer.stderr)

def generate_tray(cmd, files):
    global args
    global number_of_trays
    global number_of_trays_processed
    global number_of_trays_total

    _files = [files['png']]
    if (not args.preview):
        cmd += ["-o", files['3mf']]
        _files += [files['3mf']]

    cmd += ["tray_generator.scad"]

    _filestr = " ".join(_files)
    print(
        f"({number_of_trays_processed} of {number_of_trays_total}) Generating: {_filestr}")

    if args.dryrun:
        print("    ", " ".join(cmd))
        if (args.slice):
            print("    ", " ".join(
                get_slice_cmd(files['3mf'])))
    else:
        print("    ", " ".join(cmd))
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                universal_newlines=True)
        print(out.stdout)

        if (out.returncode == 0):
            slice(files['3mf'],
                    files['gcode'])
        else:
            print(out.stderr)

def create_incremental_division_variants(length, width, height, count_only):
    global args
    global number_of_trays
    global number_of_trays_processed
    global number_of_trays_total

    ldivs = math.floor(length/args.length_div_minimum_size)
    wdivs = math.floor(width/args.width_div_minimum_size)

    unique_sq_trays = []

    for ldiv in range(1, ldivs+1):
        if (ldiv in args.length_skip_divs):
            continue
        for wdiv in range(1, wdivs+1):
            if (wdiv in args.width_skip_divs):
                continue

            lsize = length/ldiv;
            wsize = width/wdiv;
            if lsize == wsize:
                # Square cup sizes are handled separately.
                continue;

            # Don't create duplicate trays that are simpel rotated by 90 deg.
            if length == width:
                spec1 = f"{ldiv}x{wdiv}"
                spec2 = f"{wdiv}x{ldiv}"
                if spec1 in unique_sq_trays or spec2 in unique_sq_trays:
                    continue;
                unique_sq_trays += [spec1, spec2]

            number_of_trays += 1
            if (count_only):
                continue
            number_of_trays_processed += 1
            ht = height

            if (math.floor(height) == height):
                # Don't use a .0 decimal for integer heights in file names
                ht = math.floor(height)

            folder_path = f"trays/{length}-{args.units}-L/{width}-{args.units}-W/{ht}-{args.units}-H"
            file_base = f"{folder_path}/tray_{length}x{width}x{ht}_{ldiv}x{wdiv}_cups"
            files = {
                "folder": f"trays/{length}-{args.units}-L/{width}-{args.units}-W/{ht}-{args.units}-H",
                "base": file_base,
                "png": f"{file_base}.png",
                "3mf": f"{file_base}.3mf",
                "gcode": f"{file_base}.gcode"
            }

            if (args.regen or not os.path.exists(files['3mf'])):
                if not os.path.exists(files['folder']):
                    os.makedirs(files['folder'])
                cmd = [args.oscad, "-D", "Build_Mode=\"Length_Width_Cups\"",
                        "-D", f"Scale_Units={scale_units}",
                        "-D", f"Tray_Length={length}",
                        "-D", f"Tray_Width={width}",
                        "-D", f"Tray_Height={height}",
                        "-D", f"Cup_Along_Length={ldiv}",
                        "-D", f"Cups_Across_Width={wdiv}",
                        "-o", files['png'],
                        ]

                generate_tray(cmd, files)


def create_square_cup_tray_variations(length, width, height, count_only):
    global args
    global number_of_trays
    global number_of_trays_processed
    global number_of_trays_total

    for cup_size in args.square_cup_sizes:
        if cup_size <= length or cup_size <= width:
            if length % cup_size == 0 and width % cup_size == 0:
                number_of_trays += 1

                if (count_only):
                    continue

                lcups = math.floor(length / cup_size)
                wcups = math.floor(width / cup_size)

                number_of_trays_processed += 1
                ht = height

                if (math.floor(height) == height):
                    # Don't use a .0 decimal for integer heights in file names
                    ht = math.floor(height)

                folder_path = f"trays/{length}-{args.units}-L/{width}-{args.units}-W/{ht}-{args.units}-H"
                file_base = f"{folder_path}/tray_{length}x{width}x{ht}_{lcups}x{wcups}_cups"
                files = {
                    "folder": f"trays/{length}-{args.units}-L/{width}-{args.units}-W/{ht}-{args.units}-H",
                    "base": file_base,
                    "png": f"{file_base}.png",
                    "3mf": f"{file_base}.3mf",
                    "gcode": f"{file_base}.gcode"
                }

                if (args.regen or not os.path.exists(files['3mf'])):
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    cmd = [args.oscad, "-D", "Build_Mode=\"Square_Cups\"", 
                        "-D", f"Scale_Units={scale_units}", 
                        "-D", f"Tray_Length={length}",
                        "-D", f"Tray_Width={width}",
                        "-D", f"Tray_Height={height}",
                        "-D", f"Square_Cup_Size={cup_size}",
                        "-o", files['png'], 
                    ]
                    generate_tray(cmd, files)

def enumerate_trays(count_only):
    global args

    length = args.min_length;
    while (length <= args.max_length):
        if not length in args.length_skip_dims:
            width = args.min_width;
            while (width <= args.max_width):
                if not width in args.width_skip_dims:
                    for height in args.tray_heights:
                        create_square_cup_tray_variations(
                            length, width, height, count_only)
                        create_incremental_division_variants(
                            length, width, height, count_only)
                width += args.width_incr
        length += args.length_incr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Make tray variations.')

    parser.add_argument('--units', type=str, default="inch",
                        help="Units, options are 'inch', 'cm'")

    parser.add_argument('--dryrun', type=bool, default=True,
                        help="Dry run.  Just print what will generated")

    parser.add_argument('--preview', type=bool, default=True,
                        help="Only generate preview images (faster for testing)")

    parser.add_argument('--regen', type=bool, default=False,
                        help="Force regeneration even if file exists")

    parser.add_argument('--slice', type=bool, default=True,
                        help="Slice the model file to gcode.")

    parser.add_argument('--oscad', type=str, default=r"openscad.com",
                        help="Full path to openscad.exe (use if not in yourpath)")

    parser.add_argument('--square_cup_sizes', nargs="+", type=float, default=[1, 2, 4, 6, 8],
                        help="Cup sizes to create for each tray")

    parser.add_argument('--min_length', type=float,
                        help="Minimum length of trays to generate", default=2)
    parser.add_argument('--length_incr', nargs="+", type=float,
                        help="Length increment from min to max", default=1)
    parser.add_argument('--max_length', type=float,
                        help="Maximum length of trays to generate", default=8)
    parser.add_argument('--length_skip_dims', nargs="+", type=float,
                        help="List of dimensions to skip", default=[3, 7])
    parser.add_argument("--length_div_incr", type=float,
                        nargs="+", default=1.0)
    parser.add_argument("--length_div_minimum_size", type=float,
                        default=1.0)
    parser.add_argument('--length_skip_divs', nargs="+", type=float,
                        help="List of dimensions to skip", default=[7])

    parser.add_argument('--min_width', type=float,
                        help="Minimum width of trays to generate", default=2)
    parser.add_argument('--width_incr', nargs="+", type=float,
                        help="Length increment from min to max", default=1)
    parser.add_argument('--max_width', type=float,
                        help="Maximum width of trays to generate", default=8)
    parser.add_argument('--width_skip_dims', nargs="+", type=float,
                        help="List of dimensions to skip", default=[3,7])
    parser.add_argument("--width_div_minimum_size", type=float,
                        default=1.0)
    parser.add_argument('--width_skip_divs', nargs="+", type=float,
                        help="List of dimensions to skip", default=[7])

    parser.add_argument("--tray_heights", type=float,
                        nargs="+", default=[0.75, 1.0, 1.5, 2.0])

    args = parser.parse_args()

    scale_units = 25.4
    if (args.units == "inch"):
        scale_units = 25.4
    if (args.units == "cm"):
        scale_units = 10.0

    number_of_trays = 0;
    number_of_trays_processed = 0;

    enumerate_trays(True);
    print(f"Number of trays to be created: {number_of_trays}")
    number_of_trays_total = number_of_trays

    # Now do the real work...
    enumerate_trays(False);
