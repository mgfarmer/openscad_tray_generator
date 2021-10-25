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

global wall_defs


def get_oscad_command(length, width, height, params):
    global args
    global wall_defs
    cmd = [args.oscad]
    cmd += wall_defs
    cmd += [
        "-D", f"Scale_Units={scale_units}",
        "-D", f"Tray_Length={length}",
        "-D", f"Tray_Width={width}",
        "-D", f"Tray_Height={height}",
    ]
    cmd += params
    return cmd

def get_slice_cmd(model):
    if sys.platform.startswith('win32'):
        return [r"slice.bat", model]
    return [r"./slice.sh", model]


def slice(tray_file_path_model, tray_file_path_gcode):
    if args.slice and os.path.exists(tray_file_path_model) and (args.reslice or not os.path.exists(tray_file_path_gcode)):
        slice_cmd = get_slice_cmd(tray_file_path_model)
        print("    ", f"Slicing: {tray_file_path_model}")
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
    if (not args.preview_only):
        cmd += ["-o", files['model']]
        _files += [files['model']]

    cmd += ["tray_generator.scad"]

    _filestr = " ".join(_files)
    print(
        f"({number_of_trays_processed} of {number_of_trays_total}) Generating: {_filestr}")

    if args.dryrun:
        print("    ", " ".join(cmd))
        if (args.slice):
            print("    ", " ".join(
                get_slice_cmd(files['model'])))
    else:
        print("    ", " ".join(cmd))
        out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             universal_newlines=True)
        print(out.stdout)

        if (out.returncode == 0):
            slice(files['model'],
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

            lsize = length/ldiv
            wsize = width/wdiv
            if lsize == wsize:
                # Square cup sizes are handled separately.
                continue

            # Don't create duplicate trays that are simpel rotated by 90 deg.
            if length == width:
                spec1 = f"{ldiv}x{wdiv}"
                spec2 = f"{wdiv}x{ldiv}"
                if spec1 in unique_sq_trays or spec2 in unique_sq_trays:
                    continue
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
                "folder": folder_path,
                "base": file_base,
                "png": f"{file_base}.png",
                "model": f"{file_base}.{args.export_model_as}",
                "gcode": f"{file_base}.gcode"
            }

            if (args.regen or not os.path.exists(files['model'])):
                if not os.path.exists(files['folder']):
                    os.makedirs(files['folder'])
                cmd = get_oscad_command(length, width, height,
                                        [
                                            "-D", "Build_Mode=\"Length_Width_Cups\"",
                                            "-D", f"Cup_Along_Length={ldiv}",
                                            "-D", f"Cups_Across_Width={wdiv}",
                                            "-o", files['png'],
                                        ])

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
                    "folder": folder_path,
                    "base": file_base,
                    "png": f"{file_base}.png",
                    "model": f"{file_base}.{args.export_model_as}",
                    "gcode": f"{file_base}.gcode"
                }

                if (args.regen or not os.path.exists(files['model'])):
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    cmd = get_oscad_command(length, width, height,
                                            [
                                                "-D", "Build_Mode=\"Square_Cups\"",
                                                "-D", f"Square_Cup_Size={cup_size}",
                                                "-o", files['png']
                                            ])

                    generate_tray(cmd, files)


def create_lids(length, width, count_only):
    global args
    global number_of_trays
    global number_of_trays_processed
    global number_of_trays_total

    folder_path = f"trays/{length}-{args.units}-L/{width}-{args.units}-W"

    # We are creating 3 lid variations
    number_of_trays += 3
    if (count_only):
        return

    # Recessed Lid
    file_base = f"{folder_path}/tray_lid_recessed_{length}x{width}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        cmd = get_oscad_command(length, width, 0.0,
                                [
                                    "-D", "Build_Mode=\"Tray_Lid\"",
                                    "-D", f"Lid_Thickness=0",
                                    "-o", files['png'],
                                ])
        generate_tray(cmd, files)

    # Non Recessed Lid
    file_base = f"{folder_path}/tray_lid_finger_{length}x{width}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        cmd = get_oscad_command(length, width, 0.0,
                                [
                                    "-D", "Build_Mode=\"Tray_Lid\"",
                                    "-D", f"Lid_Style=\"Finger_Holes\"",
                                    "-o", files['png'],
                                ])
        generate_tray(cmd, files)

    # Bar Handle Lid
    file_base = f"{folder_path}/tray_lid_handle_{length}x{width}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        cmd = get_oscad_command(length, width, 0.0,
                                [
                                    "-D", "Build_Mode=\"Tray_Lid\"",
                                    "-D", f"Lid_Style=\"Bar_Handle\"",
                                    "-o", files['png'],
                                ])
        generate_tray(cmd, files)


def enumerate_trays(count_only):
    global args

    for length in args.lengths:
        for width in args.widths:
            for height in args.heights:
                create_square_cup_tray_variations(
                    length, width, height, count_only)
                create_incremental_division_variants(
                    length, width, height, count_only)
            create_lids(length, width, count_only)


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Preview, render, and slice tray variations.  This script can generate a vast library of storage trays ready to be printed.  Slicing is handled by a "slice" batch/shell script that you need to implement for your slicer (that way this script does not need to know the details on how to invoke every possible slicer).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-o', '--oscad', type=str, default=r"openscad",
                        help="The openscad executable.  The default value assumes it is in your path.  Otherwise specify the full path to the executable.")

    g1 = parser.add_argument_group('Tray Sizes')

    g1.add_argument('-u', '--units', type=str, default="inch",
                    help='Tray dimensional units, options are "inch", "cm", or a numeric value. All dimensional parameters are expressed at this scale.  Fundamentally, openscad is unitless but most slicers assume that 1 unit is 1mm.  Specifying "inch" is the same as speciying "25.4", and "cm" is "10.0".  However, if you want to work in, say, Rack Units (RU), will need to specify the scale numerically as 44.5')

    g1.add_argument('-l', '--lengths', nargs="+", type=float,
                    default=[4, 6, 8],
                    help="Specifies a list of the tray lengths to generate. Can be fractional.")

    g1.add_argument('-w', '--widths', nargs="+", type=float,
                    default=[2, 4, 6, 8],
                    help="Specifies a list of the tray widths to generate. Can be fractional.")

    g1.add_argument('-t', '--heights', type=float,
                    nargs="+", default=[0.75, 1.0, 1.5, 2.0],
                    help="Specifies a list of all the tray heights to generate. Can be fractional.")

    g0 = parser.add_argument_group('Generation Control Options')
    g0.add_argument('-d', '--dryrun', type=bool, default=True,
                    help="Dry run.  Just print the commands that will be executed.")

    g0.add_argument('-p', '--preview_only', type=bool, default=False,
                    help="Only generate preview images (faster for testing).  This is fairly fast so you can visually review what will be generated and sliced.")

    g0.add_argument('-e', '--export_model_as', type=str, default="3mf",
                    help="Instruct openscad to export the rendered tray in this format.  Using 3MF is highly recommeneded.  Using STL is not recommended because OpenSCAD has trouble generating well-formed STL files. You may need to run repair utilities on it.  You can specify any other format supported by OpenSCAD to meet your needs.")

    g0.add_argument('--regen', type=bool, default=False,
                    help="Force regeneration even if file exists.  Normally model files will not be re-rendered if they already exist, saving time.  But if you need to regenerate the file to effect a change, you can set this flag.")

    g0.add_argument('-s', '--slice', type=bool, default=False,
                    help="Slice the model file to gcode.  With this option enabled, call the slice script to slice the generated model file to gcode.  You need to ensure the slice script works properly for your slicer of choice.  The name of the model file is passed to the script.")

    g0.add_argument('--reslice', type=bool, default=True,
                    help="Reslice the model file to gcode even if it already exits.  Normally gcode files are not resliced if they exist.  Use this option for force reslicing.  This is useful it you changed a slicing profile and need to reslice everything.")

    g2 = parser.add_argument_group('Tray Division',
                                   "Options in this section control how divisions (or cups) are created in the tray.")

    g2.add_argument('--square_cup_sizes', nargs="+", type=float, default=[1, 2, 4, 6, 8],
                    help='Square cup sizes to create for each tray. This is a list of square sizes that will be created for each tray.  This is only done when when the cup size is a integer multiple of both the length and width of the tray being created. For example, a 6x4 tray will not generate square cups of size 3 because 4/3 is not an integer. Specify an empty list to skip generating square cups (though some may still be created from the "divions" parameters below.  Can be fractional.')

    g2.add_argument("--length_div_minimum_size", type=float,
                    default=1.0,
                    help="When generating tray length divisions (i.e. trays with 1, 2, 3, etc.. divisions) stop creating divisions when they become smaller than this value.")

    g2.add_argument('--length_skip_divs', nargs="+", type=float,
                    help="List of divisions to skip.  If you really don't want trays with a specific number of length divisions, specify them in this list.", default=[])

    g2.add_argument("--width_div_minimum_size", type=float,
                    default=1.0,
                    help="When generating tray width divisions (i.e. trays with 1, 2, 3, etc.. divisions) stop creating divisions when they become smaller than this value.")

    g2.add_argument('--width_skip_divs', nargs="+", type=float,
                    help="List of dimensions to skip. If you really don't want trays with a specific number of width divisions, specify them in this list.", default=[])

    g3 = parser.add_argument_group('Wall and Interlock Dimensions')

    g3.add_argument('--wall_dimensions', nargs="+", type=float,
                    default=[1.75],
                    help="Specifies how thick the outer wall, floor, and dividers will be.  If only one number is provided, it wil be used for all three dminesions. If 2 numbers are provided the first will be the wall and floor thickness and the second will be the divider thickness.  Specify all three for ultimate flexability")

    g3.add_argument('--interlock_dimensions', nargs="+", type=float,
                    default=[1.75, 0.08])


    args = parser.parse_args()

    scale_units = 25.4
    if (args.units == "inch"):
        scale_units = 25.4
    if (args.units == "cm"):
        scale_units = 10.0
    if (isfloat(args.units)):
        scale_units = float(args.units)

    wall_t = 0
    floor_t = 0
    div_t = 0
    intr_h = 0
    intr_g = 0

    if len(args.wall_dimensions) == 1:
        wall_t = args.wall_dimensions[0]
        floor_t = args.wall_dimensions[0]
        div_t = args.wall_dimensions[0]
    elif len(args.wall_dimensions) == 2:
        wall_t = args.wall_dimensions[0]
        floor_t = args.wall_dimensions[0]
        div_t = args.wall_dimensions[1]
    elif len(args.wall_dimensions) >= 3:
        wall_t = args.wall_dimensions[0]
        floor_t = args.wall_dimensions[1]
        div_t = args.wall_dimensions[2]

    wall_defs = [
        "-D", f"Tray_Wall_Thickness={(wall_t/scale_units):.3f}",
        "-D", f"Floor_Thickness={(floor_t/scale_units):.3f}",
        "-D", f"Divider_Wall_Thickness={(div_t/scale_units):.3f}",
        "-D", f"Corner_Roundness=0.5",
        "-D", f"Interlock_Height={(args.interlock_dimensions[0]/scale_units):.3f}",
        "-D", f"Interlock_Gap={(args.interlock_dimensions[1]/scale_units):.3f}"
    ]


    number_of_trays = 0
    number_of_trays_processed = 0

    enumerate_trays(True)
    print(f"Number of trays to be created: {number_of_trays}")
    number_of_trays_total = number_of_trays

    # Now do the real work...
    enumerate_trays(False)
