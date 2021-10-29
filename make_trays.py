import re
import os.path
import sys
import math
import argparse
import subprocess
import json
import logging
import platform
import shutil

def get_oscad_command(length, width, height, params):
    global args
    global wall_defs
    # First, the executable...
    cmd = [openscad_exec]


    # Then the thickness parameters, which are computed from the unit base
    cmd += wall_defs

    cmd += ["-D", f"Scale_Units={scale_units}"]

    # Then the primary object dimensions, global to all objects
    if (length is not None):
        cmd += ["-D", f"Tray_Length={length}"]

    if (width is not None):
        cmd += ["-D", f"Tray_Width={width}"]

    if (height is not None):
        cmd += ["-D", f"Tray_Height={height}"]

    # And finally, the remaining parameters (specific to each object)
    cmd += params

    return cmd

def make_files_dict(folder_path, file_base):
    files = {
        "folder": folder_path,
        "base": file_base,
        "png": f"{file_base}.png",
        "model": f"{file_base}.{args.export_model_as}",
        "gcode": f"{file_base}.gcode"
    }
    return files

def get_output_folder(subfolder):
    if (args.flat):
        return f"{args.output_folder}"

    return f"{args.output_folder}/{subfolder}"

def get_slice_cmd(model):
    if sys.platform.startswith('win32'):
        return [r"slice.bat", model]
    return [r"./slice.sh", model]

# Ensure floats with ".0" are converted to ints for inclusion in strings
# So we get 5x5 instead of 5.0x5.0.
def numstr(number):
    if number == math.floor(number):
        return int(number)
    return number


def get_lw_str(length, width, height=None):
    if height is not None:
        return f"{numstr(length)}x{numstr(width)}x{numstr(height)}"
    return f"{numstr(length)}x{numstr(width)}"


def slice(files, count_only, force_slice):
    global number_of_objects_sliced

    tray_file_path_model = files['model']
    tray_file_path_gcode = files['gcode']
    if not args.dryrun and not count_only:
        if not os.path.exists(files['folder']):
            os.makedirs(files['folder'])

    if force_slice or args.slice and os.path.exists(tray_file_path_model) and (args.reslice or not os.path.exists(tray_file_path_gcode)):
        number_of_objects_sliced += 1
        slice_cmd = get_slice_cmd(tray_file_path_model)
        if not count_only:
            print("    ", f"Slicing:   {tray_file_path_model}")
        if not args.dryrun and not count_only:
            logging.info("Slicing:", slice_cmd)
            slicer = subprocess.run(slice_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)

            if args.show_output or slicer.returncode != 0:
                if slicer.stdout:
                    print(slicer.stdout)
                if slicer.stderr:
                    print(slicer.stderr)


def render_object(cmd, files, count_only):
    global args
    global number_of_objects
    global number_of_objects_total
    global number_of_objects_generated

    if (count_only):
        number_of_objects += 1

    _files = [files['png']]

    cmd += ['-o', files['png']]
    if (not args.preview_only):
        cmd += ['-o', files['model']]
        _files += [files['model']]

    cmd += ["tray_generator.scad"]

    if (args.regen or not os.path.exists(files['model'])):
        number_of_objects_generated += 1
        _filestr = " ".join(_files)
        if not count_only:
            print(f"Generating: ({number_of_objects_generated} of {number_of_objects_total}):")
            print(f"     Rendering: {files['model']}")

        if not args.dryrun and not count_only:
            if not os.path.exists(files['folder']):
                os.makedirs(files['folder'])
            logging.info("Render:", cmd)
            out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 universal_newlines=True)

            if args.show_output or out.returncode != 0:
                if out.stdout:
                    print(out.stdout)
                if out.stderr:
                    print(out.stderr)

            if (out.returncode != 0):
                print("Error! Aborting this object...")
                return

        return args.slice
    return False

issued_cmds = []
def generate_object(cmd, files, count_only):
    global issued_cmds
    if (cmd in issued_cmds):
        # Duplicate command generated, no need to do it again.
        return;
    force_slice = render_object(cmd, files, count_only)
    slice(files, count_only, force_slice)
    issued_cmds += [cmd]


def get_cup_str(lcups, wcups):
    # Putting "1x1_cups" just doesn't make much sense.
    if lcups == 1 and wcups == 1:
        return ""
    return f"_{lcups}x{wcups}_cups"

def create_incremental_division_variants(length, width, height, count_only):
    global args

    ldivs = math.floor(length/args.length_div_minimum_size)
    wdivs = math.floor(width/args.width_div_minimum_size)

    # A record of square trays we've generated, so we don't do duplicates...
    unique_sq_objects = []

    #for ldiv in range(1, ldivs+1, 2 if (scale_units < 25) else 1):
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
                if spec1 in unique_sq_objects or spec2 in unique_sq_objects:
                    continue
                unique_sq_objects += [spec1, spec2]

            ht = height

            if (math.floor(height) == height):
                # Don't use a .0 decimal for integer heights in file names
                ht = math.floor(height)

            folder_path = get_output_folder(
                f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{ht}-{unit_name}-H")
            file_base = f"{folder_path}/tray_{get_lw_str(length,width,height)}{get_cup_str(ldiv,wdiv)}"
            files = make_files_dict(folder_path, file_base)

            cmd = get_oscad_command(length, width, height,
                                    [
                                        "-D", "Build_Mode=\"Length_Width_Cups\"",
                                        "-D", f"Cup_Along_Length={ldiv}",
                                        "-D", f"Cups_Across_Width={wdiv}",
                                    ])

            generate_object(cmd, files, count_only)

def create_square_cup_tray_variations(length, width, height, count_only):
    global args

    cup_sizes = None
    if not args.square_cup_sizes:
        cup_sizes = range(1,int(max(max_length,max_width)))
    else:
        cup_sizes = args.square_cup_sizes

    for cup_size in cup_sizes:
        if cup_size <= length or cup_size <= width:
            if length % cup_size == 0 and width % cup_size == 0:

                lcups = math.floor(length / cup_size)
                wcups = math.floor(width / cup_size)

                folder_path = get_output_folder(
                    f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{numstr(height)}-{unit_name}-H")
                file_base = f"{folder_path}/tray_{get_lw_str(length,width,height)}{get_cup_str(lcups,wcups)}"
                files = make_files_dict(folder_path, file_base)

                cmd = get_oscad_command(length, width, height,
                                        [
                                            "-D", "Build_Mode=\"Square_Cups\"",
                                            "-D", f"Square_Cup_Size={cup_size}",
                                        ])

                generate_object(cmd, files, count_only)


def create_simple_tray(length, width, height, count_only):
    global args

    folder_path = get_output_folder(
        f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{numstr(height)}-{unit_name}-H")
    file_base = f"{folder_path}/tray_{get_lw_str(length,width,height)}"
    files = make_files_dict(folder_path, file_base)

    cmd = get_oscad_command(length, width, height,
                            [
                                "-D", "Build_Mode=\"Just_the_Tray\"",
                            ])

    generate_object(cmd, files, count_only)


def create_json_presets(count_only):
    global args
    global json_presets

    if json_presets is None:
        return

    for i in json_presets['parameterSets']:
        if args.presets is not None:
            if not i in args.presets:
                continue

        folder_path = get_output_folder("presets")

        file_base = f"{folder_path}/{i}"
        files = make_files_dict(folder_path, file_base)
        cmd = get_oscad_command(None, None, None,
                                [
                                    '-p', f"{args.json}",
                                    '-P', i
                                ])
        generate_object(cmd, files, count_only)


def create_json_customs(length, width, height, count_only):
    global args
    global json_customs

    if json_customs is None:
        return

    for i in json_customs['customColRows']:
        if args.json_custom_defs is not None:
            if not i in args.json_custom_defs:
                continue

        expression = json_customs['customColRows'][i]['Custom_Col_Row_Ratios']
        #exp = re.sub("\s+", '', expression)# .translate(str.maketrans('', '', ' \n\t\r'))
        folder_path = get_output_folder(
            f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{numstr(height)}-{unit_name}-H")
        file_base = f"{folder_path}/tray_{i}_{get_lw_str(length,width,height)}"
        files = make_files_dict(folder_path, file_base)

        cmd = get_oscad_command(length, width, height,
                                [
                                    '-D', 'Build_Mode=\"Custom_Divisions_per_Column_or_Row\"',
                                    '-D', f"Custom_Col_Row_Ratios={expression}",
                                ])
        generate_object(cmd, files, count_only)

    for i in json_customs['customDivisions']:
        if args.json_custom_defs is not None:
            if not i in args.json_custom_defs:
                continue

        expression = json_customs['customDivisions'][i]['Custom_Division_List']
        folder_path = get_output_folder(
            f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W/{numstr(height)}-{unit_name}-H")
        file_base = f"{folder_path}/tray_{i}_{get_lw_str(length,width,height)}"
        files = make_files_dict(folder_path, file_base)

        cmd = get_oscad_command(length, width, height,
                                [
                                    '-D', 'Build_Mode=\"Custom_Ratio_Divisions\"',
                                    '-D', f"Custom_Division_List={expression}",
                                ])
        generate_object(cmd, files, count_only)

def create_lids(length, width, count_only):
    global args

    folder_path = get_output_folder(
        f"{numstr(length)}-{unit_name}-L/{numstr(width)}-{unit_name}-W")

    # Recessed Lid
    file_base = f"{folder_path}/tray_lid_recessed_{get_lw_str(length,width)}"

    files = make_files_dict(folder_path, file_base)
    cmd = get_oscad_command(length, width, None,
                            [
                                "-D", "Build_Mode=\"Tray_Lid\"",
                                "-D", f"Lid_Thickness=0",
                            ])
    generate_object(cmd, files, count_only)

    # Non Recessed Lid
    file_base = f"{folder_path}/tray_lid_finger_{get_lw_str(length,width)}"
    files = make_files_dict(folder_path, file_base)
    cmd = get_oscad_command(length, width, 0.0,
                            [
                                "-D", "Build_Mode=\"Tray_Lid\"",
                                "-D", f"Lid_Style=\"Finger_Holes\"",
                            ])
    generate_object(cmd, files, count_only)

    # Interlocking Lid
    file_base = f"{folder_path}/tray_lid_interlocking_finger_{get_lw_str(length,width)}"
    files = make_files_dict(folder_path, file_base)
    cmd = get_oscad_command(length, width, 0.0,
                            [
                                "-D", "Build_Mode=\"Tray_Lid\"",
                                "-D", f"Lid_Style=\"Finger_Holes\"",
                                "-D", f"Interlocking_Lid=true",
                            ])
    generate_object(cmd, files, count_only)

    # Bar Handle Lid
    # file_base = f"{folder_path}/tray_lid_handle_{get_lw_str(length,width)}"
    # files = make_files_dict(folder_path, file_base)
    # cmd = get_oscad_command(length, width, 0.0,
    #                         [
    #                             "-D", "Build_Mode=\"Tray_Lid\"",
    #                             "-D", f"Lid_Style=\"Bar_Handle\"",
    #                         ])
    # generate_object(cmd, files, count_only)

def enumerate_tray_sizes():
    global max_length
    global max_width

    max_length = 0;
    max_width = 0;

    if args.dimensions:
        sizes = []
        for elem in args.dimensions:
            lxw = elem.split('x')
            if len(lxw) < 2:
                print("Invalid dimension specified for --dimensions. Need LxW or LxWxH, got", elem)
            
            length = float(lxw[0])
            width = float(lxw[1])

            max_length = max(max_length, length)
            max_width = max(max_width, width)

            if len(lxw) == 2:
                if not args.heights:
                    print("When using --dimensions with LxW expressions, you must also provide heights using --heights, or use LxWxH expressions")
                    sys.exit(1)
                for height in args.heights:
                    sizes += [[length, width, height]]

            if len(lxw) == 3:
                sizes += [[length, width, float(lxw[2])]]

        # TODO: What if we fall thru here? Is that a valid and useful case
        return sizes

    else:
        sizes = []
        for length in args.lengths:
            for width in args.widths:

                max_length = max(max_length, length)
                max_width = max(max_width, width)

                if width > length:
                    # This prevents duplicate trays
                    continue
                for height in args.heights:
                    sizes += [[length, width, height]]
        return sizes

def enumerate_objects(count_only):
    global args

    sizes = enumerate_tray_sizes()
    if args.info:
        print("These tray sizes will be considered:")
        print(sizes)

    handled_lids = []
    for s in sizes:
        length = s[0]
        width = s[1]
        height = s[2]
        if args.auto_squares or args.auto_divisions:
            if (args.auto_squares):
                create_square_cup_tray_variations(
                    length, width, height, count_only)

            if (args.auto_divisions):
                create_incremental_division_variants(
                    length, width, height, count_only)

        else:
            create_simple_tray(length, width, height, count_only)

        create_json_customs(length, width, height, count_only)

        if (args.auto_lids):
            if not [length,width] in handled_lids:
                create_lids(length, width, count_only)
                handled_lids += [length,width]

    create_json_presets(count_only)

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

# https://stackoverflow.com/a/27434050/45206
class LoadFromFile (argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            # parse arguments in the file and store them in the target namespace
            parser.parse_args(f.read().split(), namespace)

def make_args():
    global parser
    global args

    parser = argparse.ArgumentParser(
    description='Preview, render, and slice tray variations.  This script can generate a vast library of storage trays ready to be printed.  Slicing is handled by a "slice" batch/shell script that you need to implement for your slicer (that way this script does not need to know the details on how to invoke every possible slicer).',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', '--info', type=str2bool, nargs="?", default=False, const=True,
                    help="Print more verbose information.")

    parser.add_argument('--show_output', type=str2bool, nargs="?", default=False, const=True,
                        help="Print output from subprocesses")

    parser.add_argument('--arg_file', type=open, action=LoadFromFile,
                    help="Specify a file that contains all the command line parameter, and use them instead.")

    g1 = parser.add_argument_group('Tray Parameters')

    g1.add_argument('-u', '--units', type=str, default="inch",
                    help='Tray dimensional units, options are "inch", "cm", or a numeric value. All dimensional parameters are expressed at this scale.  Fundamentally, openscad is unitless but most slicers assume that 1 unit is 1mm.  Specifying "inch" is the same as speciying "25.4", and "cm" is "10.0".  However, if you want to work in, say, Rack Units (RU), will need to specify the scale numerically as "ru=44.5"')

    g1.add_argument('-l', '--lengths', nargs="+", type=float,
                    default=[4, 6, 8],
                    help="Specifies a list of the tray lengths to generate. Can be fractional.  Your longest tray should be specified in the lengths, not the width.  Tray widths greater then the length will not be generated.")

    g1.add_argument('-w', '--widths', nargs="+", type=float,
                    default=[2, 4, 6, 8],
                    help="Specifies a list of the tray widths to generate. Can be fractional.  Tray widths greater than the length will not be generated.")

    g1.add_argument('-t', '--heights', type=float,
                    nargs="+", default=[],
                    help="Specifies a list of all the tray heights to generate. Can be fractional.")

    g1.add_argument('-x', '--dimensions', type=str, nargs="+", default=[],
                    help='Specify a fixed list of dimensions to create as a list of "LxW" string or "LxWxH" strings (but not both). If the H term is not provided then heights specific by --heights will be used.')

    g1.add_argument('--json', type=str, default="",
                    help="Load custom tray definitions from this OpenSCAD preset file.  All presets will be generated unless (see --preset)")

    g1.add_argument('--presets', type=str, nargs="+", default=[],
                    help="Generate only specified preset(s) from the specified json preset file (see --json)")

    g1.add_argument('--json_custom', type=str, 
                    help="Specify a json file containing custom layout expressions. All layouts will be generated unless (see --json_custom_defs)")

    g1.add_argument('--json_custom_defs', type=str, nargs="+",
                    help="Generate only specified preset(s) from the specified json_custom file (see --json_custom)")
    



    g0 = parser.add_argument_group('Generation Control Options')

    g0.add_argument('--oscad', type=str, nargs="+",
                        help="The openscad executable.  The default value assumes it is in your path.  Otherwise specify the full path to the executable.")

    g0.add_argument('-o', '--output_folder', type=str, default=r"",
                    help="Place all generated files into this folder.")

    g0.add_argument('--flat', type=str2bool, nargs="?", default=False, const=True,
                    help="When set to True, organize generated files into a folder structure based on size.  When False, all files will go into the top level folder.")

    g0.add_argument('-d', '--dryrun', type=str2bool, nargs="?", default=False, const=True,
                    help="Dry run.  Just print the commands that will be executed.")

    g0.add_argument('-c', '--count_only', type=str2bool, nargs="?", default=False, const=True,
                    help="Like --dryrun, but just report the count of trays that would be generated.")

    g0.add_argument('--doit', type=str2bool, nargs="?", default=False, const=True,
                    help="Don't confirm starting generation of trays (a potentially long running operation).")

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

    g0.add_argument('--auto_lids', type=str2bool, nargs="?", default=False, const=True,
                    help="Automatically generate lids to fit generated tray sizes")




    g2 = parser.add_argument_group('Tray Divisions',
                                   "Options in this section control how divisions (or cups) are created in the tray.")

    g2.add_argument('--auto_squares', type=str2bool, nargs="?", default=False, const=True,
                    help="Automatically generate cup divisions for square cups");

    g2.add_argument('--square_cup_sizes', nargs="+", type=float, default=[],
                    help='Square cup sizes to create for each tray. This is a list of square sizes that will be created for \
                            each tray.  This is only done when when the cup size is a integer multiple of both the length and \
                            width of the tray being created. For example, a 6x4 tray will not generate square cups of size 3 because \
                            4/3 is not an integer. Specify an empty list to skip generating square cups (though some may still be \
                            created from the "divions" parameters below.  Can be fractional.  If not provided then all unit sizes will \
                            be created.  Requires --auto_squares')

    g2.add_argument('--auto_divisions', type=str2bool, nargs="?", default=False, const=True,
                    help="Automatically generate divisions unit incremental  length/width cups")

    g2.add_argument("--length_div_minimum_size", type=float,
                    help="When generating tray length divisions (i.e. trays with 1, 2, 3, etc.. divisions) \
                        stop creating divisions when they become smaller than this value. \
                        Default minimum size is 1 inch or 3 cm, depending on --unit choice.")

    g2.add_argument('--length_skip_divs', nargs="+", type=float,
                    help="List of divisions to skip.  If you really do not want trays with a specific number of length divisions, specify them in this list.", default=[])

    g2.add_argument("--width_div_minimum_size", type=float,
                    help="When generating tray width divisions (i.e. trays with 1, 2, 3, etc.. divisions) \
                        stop creating divisions when they become smaller than this value. \
                        Default minimum size is 1 inch or 3 cm, depending on --unit choice.")

    g2.add_argument('--width_skip_divs', nargs="+", type=float,
                    help="List of dimensions to skip. If you really do not want trays with a specific number of width divisions, specify them in this list.", default=[])

    g3 = parser.add_argument_group('Wall and Interlock Dimensions')

    g3.add_argument('--wall_dimensions', nargs="+", type=float,
                    help="Specifies how thick the outer wall, floor, and dividers will be.  If only one number is provided, it wil be used for all three dminesions. If 2 numbers are provided the first will be the wall and floor thickness and the second will be the divider thickness.  Specify all three for ultimate flexability")

    g3.add_argument('--interlock_dimensions', nargs="+", type=float,
                    help="interlocking dimensions")

    args = parser.parse_args()

def determine_units():
    global unit_name
    global scale_units

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

    # pattern for matching "<unit_name>=<scale-factor>"
    pattern = re.compile('(\w+)=(.*)')
    m = pattern.match(args.units)
    if m:
        unit_name = m.group(1)
        scale_units = float(m.group(2))

    if args.info:
        print(f"Units: '{unit_name}' scale: {scale_units} mm/{unit_name}")

def parse_app_defaults(filename):
    global openscad_exec
    global args

    #if args.info:
    print(f"Reading app defaults from: {filename}")

    with open(filename) as f:
        defaults = json.load(f)

    if defaults.get("openscad_exec"):
        openscad_exec = defaults.get('openscad_exec', openscad_exec)


def is_tool(name):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            return False
    return True


def find_prog(prog):
    cmd = "where" if platform.system() == "Windows" else "which"
    return subprocess.call([cmd, prog])

def main():
    global args

    # Total number of objects in the library
    global number_of_objects

    # Total number of objects that will be generated during the run.
    global number_of_objects_total

    # Count of object generated while running, for progrss reporting.
    global number_of_objects_generated

    # Count of object sliced while running, for progrss reporting.
    global number_of_objects_sliced

    global scale_units
    global unit_name
    global wall_defs
    global json_presets
    global json_customs
    global openscad_exec

    openscad_exec = 'openscad'
    defaults_file = 'config.json'

    if os.path.exists(defaults_file):
        parse_app_defaults(defaults_file)

    make_args()

    if args.oscad:
        openscad_exec = args.oscad

    if args.count_only:
        args.dryrun = True

    if not args.count_only and args.output_folder == "":
        print("You need to specify an output folder (-o <folder>) so I know where to put everything.")
        sys.exit(0)

    if not args.dimensions and not (args.lengths and args.widths and args.heights):
        print("You need to specify dimensions of the tray(s) you want to create using")
        print("--dimension/--heights, or --lengths, --widths, and --height.")
        print('For instance, try "--dimension 2x4x1"')
        print('Use "-h" to get more help.')
        sys.exit(0)


    json_presets = None
    if (args.json != ""):
        f = open(args.json)
        json_presets = json.load(f)

    json_customs = None
    if args.json_custom is not None:
        f = open(args.json_custom)
        json_customs = json.load(f)


    determine_units()

    if not args.length_div_minimum_size:
        args.length_div_minimum_size = 1 if scale_units > 25 else 3
    if not args.width_div_minimum_size:
        args.width_div_minimum_size = 1 if scale_units > 25 else 3

    # These are default values in mm, scaled to user units.
    wall_t = 1.75/scale_units
    floor_t = 1.75/scale_units
    div_t = 1.75/scale_units
    intr_h = 1.75/scale_units
    intr_r = 1.78/scale_units
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
            intr_r = args.interlock_dimensions[1]
        if len(args.interlock_dimensions) > 1:
            intr_r = args.interlock_dimensions[1]
        if len(args.interlock_dimensions) > 2:
            intr_g = args.interlock_dimensions[1]

    wall_defs = [
        "-D", f"Tray_Wall_Thickness={wall_t:.3f}",
        "-D", f"Floor_Thickness={floor_t:.3f}",
        "-D", f"Divider_Wall_Thickness={div_t:.3f}",
        "-D", f"Corner_Roundness=1.0",
        "-D", f"Interlock_Height={intr_h:.3f}",
        "-D", f"Interlock_Gap={intr_g:.3f}",
        "-D", f"Interlock_Divider_Wall_Recess={intr_r:.3f}"
    ]

    # Check that we can resolve an OpenSCAD executable
    if not os.path.exists(openscad_exec):
        openscad_path = shutil.which(openscad_exec)
        if not openscad_path:
            print(f"An OpenSCAD executable could not be resolved!")
            print(f"Check your config.json, --oscad param, or your PATH")
        else:
            if args.info:
                print(f"OpenSCAD: {openscad_path} (from your path)")
    else:
        if args.info:
            print(f"OpenSCAD: {openscad_exec}")

    number_of_objects = 0
    number_of_objects_generated = 0
    number_of_objects_sliced = 0
    number_of_objects_total = 0

    # First rip through the generator and just count the number
    # of elements that will be generated.
    enumerate_objects(count_only=True)

    count_summary =  f"Number of objects declared:         {number_of_objects}\n"
    count_summary += f"Number of objects to be gen/sliced: {number_of_objects_generated}, {number_of_objects_sliced}\n"
    count_summary += f"Number of objects existing:         {number_of_objects-number_of_objects_generated}\n"

    if args.count_only:
        print("Count Summary:")
        print(count_summary)
        sys.exit(0)

    if number_of_objects == 0:
        print(count_summary)
        print("This probably wasn't what you were expecting!")
        sys.exit(0)

    if number_of_objects_generated == 0 and number_of_objects_sliced == 0:
        print("All your work is already done!")
        print("Use --regen and/or --reslice if you need to.")
        print(count_summary)
        sys.exit(0)

    if (not args.dryrun and number_of_objects > 0 and not args.doit):
        print("This is what is going to happen:")
        print(count_summary)
        print('You can disable this prompt with "--doit"')
        confirm = input("Are you ready to do this? [Y/n]: ")
        if confirm.lower().startswith('n'):
            print("OK, maybe next time...")
            sys.exit(0)

    # Record the total since running the generator will still
    # increment the number_of_objects variable.
    number_of_objects_total = number_of_objects_generated

    # Reset these so the report properly during generation
    number_of_objects_generated = 0
    number_of_objects_sliced = 0

    # Now do the real work...
    enumerate_objects(count_only=False)

    count_summary = f"Number of objects declared:         {number_of_objects}\n"
    count_summary += f"Number of objects to be gen/sliced: {number_of_objects_generated}, {number_of_objects_sliced}\n"
    count_summary += f"Number of objects existing:         {number_of_objects-number_of_objects_generated}\n"

    print("\nSummary:")
    print(count_summary)

if __name__ == "__main__":
    main()
