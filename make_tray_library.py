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
global number_of_trays_total

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

def numstr(number):
    if number == math.floor(number):
        return int(number)
    return number

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

    number_of_trays_processed += 1

    _filestr = " ".join(_files)
    print(
        f"({number_of_trays_processed} of {number_of_trays_total}) Generating: {_filestr}")

    if args.dryrun:
        print("    ", " ".join(cmd))
        if (args.slice):
            print("    ", " ".join(
                get_slice_cmd(files['model'])))
    else:
        if not os.path.exists(files['folder']):
            os.makedirs(files['folder'])


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

    ldivs = math.floor(length/args.length_div_minimum_size)
    wdivs = math.floor(width/args.width_div_minimum_size)

    # A record of square trays we've generated, so we don't do duplicates...
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

            
            if (count_only):
                number_of_trays += 1
                continue

            ht = height

            if (math.floor(height) == height):
                # Don't use a .0 decimal for integer heights in file names
                ht = math.floor(height)

            folder_path = f"{args.folder}/{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{ht}-{unit_name}-H"
            if (args.flat):
                folder_path = f"{args.folder}"

            file_base = f"{folder_path}/tray_{numstr(length)}x{numstr(width)}x{numstr(ht)}_{ldiv}x{wdiv}_cups"
            files = {
                "folder": folder_path,
                "base": file_base,
                "png": f"{file_base}.png",
                "model": f"{file_base}.{args.export_model_as}",
                "gcode": f"{file_base}.gcode"
            }

            if (args.regen or not os.path.exists(files['model'])):
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

    for cup_size in args.square_cup_sizes:
        if cup_size <= length or cup_size <= width:
            if length % cup_size == 0 and width % cup_size == 0:

                if (count_only):
                    number_of_trays += 1
                    continue

                lcups = math.floor(length / cup_size)
                wcups = math.floor(width / cup_size)

                ht = height

                if (math.floor(height) == height):
                    # Don't use a .0 decimal for integer heights in file names
                    ht = math.floor(height)

                folder_path = f"{args.folder}/{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{numstr(ht)}-{unit_name}-H"
                if (args.flat):
                    folder_path = f"{args.folder}"

                file_base = f"{folder_path}/tray_{numstr(length)}x{numstr(width)}x{numstr(ht)}_{lcups}x{wcups}_cups"
                files = {
                    "folder": folder_path,
                    "base": file_base,
                    "png": f"{file_base}.png",
                    "model": f"{file_base}.{args.export_model_as}",
                    "gcode": f"{file_base}.gcode"
                }

                if (args.regen or not os.path.exists(files['model'])):
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
    global number_of_trays_total

    folder_path = f"{args.folder}/{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W"
    if (args.flat):
        folder_path = f"{args.folder}"

    if (count_only):
        number_of_trays += 3
        return

    # Recessed Lid
    file_base = f"{folder_path}/tray_lid_recessed_{numstr(length)}x{numstr(width)}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
        cmd = get_oscad_command(length, width, 0.0,
                                [
                                    "-D", "Build_Mode=\"Tray_Lid\"",
                                    "-D", f"Lid_Thickness=0",
                                    "-o", files['png'],
                                ])
        generate_tray(cmd, files)

    # Non Recessed Lid
    file_base = f"{folder_path}/tray_lid_finger_{numstr(length)}x{numstr(width)}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
        cmd = get_oscad_command(length, width, 0.0,
                                [
                                    "-D", "Build_Mode=\"Tray_Lid\"",
                                    "-D", f"Lid_Style=\"Finger_Holes\"",
                                    "-o", files['png'],
                                ])
        generate_tray(cmd, files)

    # Bar Handle Lid
    file_base = f"{folder_path}/tray_lid_handle_{numstr(length)}x{numstr(width)}"
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    if (args.regen or not os.path.exists(files['model'])):
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

# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Preview, render, and slice tray variations.  This script can generate a vast library of storage trays ready to be printed.  Slicing is handled by a "slice" batch/shell script that you need to implement for your slicer (that way this script does not need to know the details on how to invoke every possible slicer).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    g1 = parser.add_argument_group('Tray Sizes')

    g1.add_argument('-u', '--units', type=str, default="inch",
                    help='Tray dimensional units, options are "inch", "cm", or a numeric value. All dimensional parameters are expressed at this scale.  Fundamentally, openscad is unitless but most slicers assume that 1 unit is 1mm.  Specifying "inch" is the same as speciying "25.4", and "cm" is "10.0".  However, if you want to work in, say, Rack Units (RU), will need to specify the scale numerically as "ru=44.5"')

    g1.add_argument('-l', '--lengths', nargs="+", type=float,
                    default=[4, 6],
                    help="Specifies a list of the tray lengths to generate. Can be fractional.")

    g1.add_argument('-w', '--widths', nargs="+", type=float,
                    default=[2, 4],
                    help="Specifies a list of the tray widths to generate. Can be fractional.")

    g1.add_argument('-t', '--heights', type=float,
                    nargs="+", default=[0.75, 1.0, 1.5, 2.0],
                    help="Specifies a list of all the tray heights to generate. Can be fractional.")

    g0 = parser.add_argument_group('Generation Control Options')
    g0.add_argument('-o', '--oscad', type=str, default=r"openscad",
                        help="The openscad executable.  The default value assumes it is in your path.  Otherwise specify the full path to the executable.")

    g0.add_argument('-f', '--folder', type=str, default=r"trays",
                    help="Place all generated files into this folder.")

    g0.add_argument('--flat', type=str2bool, nargs="?", default=False, const=True,
                    help="When set to True, organize generated files into a folder structure based on size.  When False, all files will go into the top level folder.")

    g0.add_argument('-d', '--dryrun', type=str2bool, nargs="?", default=False, const=True,
                    help="Dry run.  Just print the commands that will be executed.")

    g0.add_argument('-p', '--preview_only', type=str2bool, nargs="?", default=False, const=True,
                    help="Only generate preview images (faster for testing).  This is fairly fast so you can visually review what will be generated and sliced.")

    g0.add_argument('-e', '--export_model_as', type=str, default="3mf",
                    help="Instruct openscad to export the rendered tray in this format.  Using 3MF is highly recommeneded.  Using STL is not recommended because OpenSCAD has trouble generating well-formed STL files. You may need to run repair utilities on it.  You can specify any other format supported by OpenSCAD to meet your needs.")

    g0.add_argument('--regen', type=str2bool, nargs="?", default=False, const=True,
                    help="Force regeneration even if file exists.  Normally model files will not be re-rendered if they already exist, saving time.  But if you need to regenerate the file to effect a change, you can set this flag.")

    g0.add_argument('-s', '--slice', type=str2bool, nargs="?", default=False, const=True,
                    help="Slice the model file to gcode.  With this option enabled, call the slice script to slice the generated model file to gcode.  You need to ensure the slice script works properly for your slicer of choice.  The name of the model file is passed to the script.")

    g0.add_argument('--reslice', type=str2bool, nargs="?", default=False, const=True,
                    help="Reslice the model file to gcode even if it already exits.  Normally gcode files are not resliced if they exist.  Use this option for force reslicing.  This is useful it you changed a slicing profile and need to reslice everything.")

    g2 = parser.add_argument_group('Tray Divisions',
                                   "Options in this section control how divisions (or cups) are created in the tray.")

    g2.add_argument('--square_cup_sizes', nargs="+", type=float, default=[1, 2, 3, 4, 5, 6, 8],
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
                    help="Specifies how thick the outer wall, floor, and dividers will be.  If only one number is provided, it wil be used for all three dminesions. If 2 numbers are provided the first will be the wall and floor thickness and the second will be the divider thickness.  Specify all three for ultimate flexability")

    g3.add_argument('--interlock_dimensions', nargs="+", type=float,
                    help="interlocking dimensions")


    args = parser.parse_args()

    pattern = re.compile('(\w+)=(.*)')

    scale_units = 25.4
    unit_name="in"

    if (args.units == "inch"):
        scale_units = 25.4
        unit_name = "in"
    if (args.units == "cm"):
        scale_units = 10.0
        unit_name = "cm"
    if (isfloat(args.units)):
        unit_name = "flibits"
        scale_units = float(args.units)

    m = pattern.match(args.units)
    if m:
        unit_name = m.group(1)
        scale_units = float(m.group(2))

    # These are default values in mm, scaled to user units.
    wall_t = 1.75/scale_units
    floor_t = 1.75/scale_units
    div_t = 1.75/scale_units
    intr_h = 1.75/scale_units
    intr_g = 0.08/scale_units

    # Now process user overrides from the command line.
    if (args.wall_dimensions is not None):
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

    if (args.interlock_dimensions is not None):
        if len(args.interlock_dimensions) >= 1:
            intr_h = args.interlock_dimensions[0]
        if len(args.interlock_dimensions) > 1:
            intr_g = args.interlock_dimensions[1]

    wall_defs = [
        "-D", f"Tray_Wall_Thickness={wall_t:.3f}",
        "-D", f"Floor_Thickness={floor_t:.3f}",
        "-D", f"Divider_Wall_Thickness={div_t:.3f}",
        "-D", f"Corner_Roundness=0.5",
        "-D", f"Interlock_Height={intr_h:.3f}",
        "-D", f"Interlock_Gap={intr_g:.3f}"
    ]


    number_of_trays = 0
    number_of_trays_processed = 0

    # First rip through the generator and just count the number
    # of elements that will be generated.
    enumerate_trays(True)
    print(f"Number of trays to be created: {number_of_trays}")

    # Record the total since running the generator will still
    # increment the number_of_trays variable.
    number_of_trays_total = number_of_trays

    # Now do the real work...
    enumerate_trays(False)
