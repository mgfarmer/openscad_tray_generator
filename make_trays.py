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

class MakeTrays:

    args = None

    def get_oscad_command(self,length, width, height, params):
        # First, the executable...
        cmd = [self.config['openscad_exec']]


        # Then the thickness parameters, which are computed from the unit base
        cmd += self.config['wall_defs']

        cmd += ["-D", f"Scale_Units={self.config['scale_units']}"]

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

    def make_files_dict(self, folder_path, file_base):
        files = {
            "folder": folder_path,
            "base": file_base,
            "png": f"{file_base}.png",
            "model": f"{file_base}.{self.config['model_format']}",
            "gcode": f"{file_base}.gcode"
        }
        return files

    def get_output_folder(self, subfolder):
        if self.config['flat'] == True:
            return f"{self.config['output_folder']}"

        return f"{self.config['output_folder']}/{subfolder}"

    def get_slice_cmd(model):
        if sys.platform.startswith('win32'):
            return [r"slice.bat", model]
        return [r"./slice.sh", model]

    # Ensure floats with ".0" are converted to ints for inclusion in strings
    # So we get 5x5 instead of 5.0x5.0.
    def numstr(self, number):
        if number == math.floor(number):
            return int(number)
        return number

    def get_lw_str(self, length, width, height=None):
        if height is not None:
            return f"{self.numstr(length)}x{self.numstr(width)}x{self.numstr(height)}"
        return f"{self.numstr(length)}x{self.numstr(width)}"

    def slice(self, files, count_only, force_slice):
        tray_file_path_model = files['model']
        tray_file_path_gcode = files['gcode']
        if not self.args.dryrun and not count_only:
            if not os.path.exists(files['folder']):
                os.makedirs(files['folder'])

        if force_slice or self.args.slice and os.path.exists(tray_file_path_model) and (self.args.reslice or not os.path.exists(tray_file_path_gcode)):
            self.number_of_objects_sliced += 1
            slice_cmd = self.get_slice_cmd(tray_file_path_model)
            if not count_only:
                print("    ", f"Slicing:   {tray_file_path_model}")
                self.result['slices'] += [files['gcode']]
            if not self.args.dryrun and not count_only:
                logging.info("Slicing:", slice_cmd)
                slicer = subprocess.run(slice_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        universal_newlines=True)

                if self.args.show_output or slicer.returncode != 0:
                    if slicer.stdout:
                        print(slicer.stdout)
                    if slicer.stderr:
                        print(slicer.stderr)


    def render_object(self, cmd, files, count_only):
        if (count_only):
            self.number_of_objects += 1

        _files = [files['png']]

        cmd += ['-o', files['png']]
        if (not self.args.preview_only):
            cmd += ['-o', files['model']]
            _files += [files['model']]

        cmd += ["tray_generator.scad"]

        if (self.args.regen or not os.path.exists(files['model'])):
            self.number_of_objects_generated += 1
            _filestr = " ".join(_files)
            if not count_only:
                print(
                    f"Generating: ({self.number_of_objects_generated} of {self.number_of_objects_total}):")
                print(f"     Rendering: {files['model']}")
                self.result['models'] += [files['model']]
            if not self.args.dryrun and not count_only:
                if not os.path.exists(files['folder']):
                    os.makedirs(files['folder'])
                logging.info("Render:", cmd)
                out = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)

                if self.args.show_output or out.returncode != 0:
                    if out.stdout:
                        print(out.stdout)
                    if out.stderr:
                        print(out.stderr)

                if (out.returncode != 0):
                    print("Error! Aborting this object...")
                    return

            return self.args.slice
        return False

    def generate_object(self, cmd, files, count_only):
        if (cmd in self.issued_cmds):
            # Duplicate command generated, no need to do it again.
            return;
        force_slice = self.render_object(cmd, files, count_only)
        slice(files, count_only, force_slice)
        self.issued_cmds += [cmd]


    def get_cup_str(self, lcups, wcups):
        # Putting "1x1_cups" just doesn't make much sense.
        if lcups == 1 and wcups == 1:
            return ""
        return f"_{lcups}x{wcups}_cups"

    def create_incremental_division_variants(self, length, width, height, count_only):
        ldivs = math.floor(length/self.config['length_div_minimum_size'])
        wdivs = math.floor(width/self.config['width_div_minimum_size'])

        # A record of square trays we've generated, so we don't do duplicates...
        unique_sq_objects = []

        #for ldiv in range(1, ldivs+1, 2 if (scale_units < 25) else 1):
        for ldiv in range(1, ldivs+1):

            if (ldiv in self.config['length_skip_divs']):
                continue
            for wdiv in range(1, wdivs+1):
                if (wdiv in self.config['width_skip_divs']):
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

                folder_path = self.get_output_folder(
                    self.get_output_path(length, width, height))
                file_base = f"{folder_path}/tray_{self.get_lw_str(length,width,height)}{self.get_cup_str(ldiv,wdiv)}"
                files = self.make_files_dict(folder_path, file_base)

                cmd = self.get_oscad_command(length, width, height,
                                        [
                                            "-D", "Build_Mode=\"Length_Width_Cups\"",
                                            "-D", f"Cup_Along_Length={ldiv}",
                                            "-D", f"Cups_Across_Width={wdiv}",
                                        ])

                self.generate_object(cmd, files, count_only)

    def get_output_path(self, length, width, height):
        return f"{self.numstr(length)}_{self.config['unit_name']}_long/{self.numstr(width)}_{self.config['unit_name']}_wide/{self.numstr(height)}_{self.config['unit_name']}_high"

    def create_square_cup_tray_variations(self, length, width, height, count_only):
        cup_sizes = None
        if not self.config['square_cup_sizes']:
            cup_sizes = range(1,int(max(self.max_length,self.max_width)))
        else:
            cup_sizes = self.config['square_cup_sizes']

        for cup_size in cup_sizes:
            if cup_size <= length or cup_size <= width:
                if length % cup_size == 0 and width % cup_size == 0:

                    lcups = math.floor(length / cup_size)
                    wcups = math.floor(width / cup_size)

                    folder_path = self.get_output_folder(
                        self.get_output_path(length, width, height))
                    file_base = f"{folder_path}/tray_{self.get_lw_str(length,width,height)}{self.get_cup_str(lcups,wcups)}"
                    files = self.make_files_dict(folder_path, file_base)

                    cmd = self.get_oscad_command(length, width, height,
                                            [
                                                "-D", "Build_Mode=\"Square_Cups\"",
                                                "-D", f"Square_Cup_Size={cup_size}",
                                            ])

                    self.generate_object(cmd, files, count_only)


    def create_simple_tray(self, length, width, height, count_only):
        folder_path = self.get_output_folder(
            self.get_output_path(length, width, height))
        file_base = f"{folder_path}/tray_{self.get_lw_str(length,width,height)}"
        files = self.make_files_dict(folder_path, file_base)

        cmd = self.get_oscad_command(length, width, height,
                                [
                                    "-D", "Build_Mode=\"Just_the_Tray\"",
                                ])

        self.generate_object(cmd, files, count_only)


    def create_openscad_presets(self, count_only):
        if self.config['openscad_presets_json'] is None:
            return

        # Check that names in the list are actually in the file and report otherwise
        for i in self.config['openscad_presets_json']['parameterSets']:
            if self.config['openscad_preset_names']:
                if not i in self.config['openscad_preset_names']:
                    continue

            folder_path = self.get_output_folder("presets")

            file_base = f"{folder_path}/{i}"
            files = self.make_files_dict(folder_path, file_base)
            cmd = self.get_oscad_command(None, None, None,
                                    [
                                        '-p', f"{self.config['openscad_presets_file']}",
                                        '-P', i
                                    ])
            self.generate_object(cmd, files, count_only)


    def create_custom_layouts(self, length, width, height, count_only):
        if self.config['custom_layouts_json'] is None:
            return

        for i in self.config['custom_layouts_json']['customColRows']:
            if self.config['custom_layout_names'] is not None:
                if not i in self.config['custom_layout_names']:
                    continue

            expression = self.config['custom_layouts_json']['customColRows'][i]['Custom_Col_Row_Ratios']
            #exp = re.sub("\s+", '', expression)# .translate(str.maketrans('', '', ' \n\t\r'))
            folder_path = self.get_output_folder(
                self.get_output_path(length, width, height))
            file_base = f"{folder_path}/tray_{i}_{self.get_lw_str(length,width,height)}"
            files = self.make_files_dict(folder_path, file_base)

            cmd = self.get_oscad_command(length, width, height,
                                    [
                                        '-D', 'Build_Mode=\"Custom_Divisions_per_Column_or_Row\"',
                                        '-D', f"Custom_Col_Row_Ratios={expression}",
                                    ])
            self.generate_object(cmd, files, count_only)

        for i in self.config['custom_layouts_json']['customDivisions']:
            if self.config['custom_layout_names'] is not None:
                if not i in self.config['custom_layout_names']:
                    continue

            expression = self.config['custom_layouts_json']['customDivisions'][i]['Custom_Division_List']
            folder_path = self.get_output_folder(
                self.get_output_path(length, width, height))
            file_base = f"{folder_path}/tray_{i}_{self.get_lw_str(length,width,height)}"
            files = self.make_files_dict(folder_path, file_base)

            cmd = self.get_oscad_command(length, width, height,
                                    [
                                        '-D', 'Build_Mode=\"Custom_Ratio_Divisions\"',
                                        '-D', f"Custom_Division_List={expression}",
                                    ])
            self.generate_object(cmd, files, count_only)

    def create_lids(self, length, width, count_only):
        folder_path = self.get_output_folder(
            f"{self.numstr(length)}-{self.config['unit_name']}-L/{self.numstr(width)}-{self.config['unit_name']}-W")

        styles = self.config['lid_styles']

        if not styles or "recessed" in styles:
            # Recessed Lid
            file_base = f"{folder_path}/tray_lid_recessed_{self.get_lw_str(length,width)}"

            files = self.make_files_dict(folder_path, file_base)
            cmd = self.get_oscad_command(length, width, None,
                                    [
                                        "-D", "Build_Mode=\"Tray_Lid\"",
                                        "-D", f"Lid_Style=\"Finger_Holes\"",
                                        "-D", f"Lid_Thickness=0",
                                    ])
            self.generate_object(cmd, files, count_only)

        if not styles or "regular" in styles:
                # Non Recessed Lid
            file_base = f"{folder_path}/tray_lid_finger_{self.get_lw_str(length,width)}"
            files = self.make_files_dict(folder_path, file_base)
            cmd = self.get_oscad_command(length, width, 0.0,
                                    [
                                        "-D", "Build_Mode=\"Tray_Lid\"",
                                        "-D", f"Lid_Style=\"Finger_Holes\"",
                                    ])
            self.generate_object(cmd, files, count_only)

        if not styles or "stackable" in styles:
            # Interlocking Lid
            file_base = f"{folder_path}/tray_lid_interlocking_finger_{self.get_lw_str(length,width)}"
            files = self.make_files_dict(folder_path, file_base)
            cmd = self.get_oscad_command(length, width, 0.0,
                                    [
                                        "-D", "Build_Mode=\"Tray_Lid\"",
                                        "-D", f"Lid_Style=\"Finger_Holes\"",
                                        "-D", f"Interlocking_Lid=true",
                                    ])
            self.generate_object(cmd, files, count_only)

    def enumerate_tray_sizes(self):
        self.max_length = 0;
        self.max_width = 0;

        if self.config['dimensions']:
            sizes = []
            for elem in self.config['dimensions']:
                lxw = elem.split('x')
                if len(lxw) < 2:
                    print("Invalid dimension specified for 'dimensions'. Need LxW or LxWxH, got", elem)
                
                length = float(lxw[0])
                width = float(lxw[1])

                self.max_length = max(self.max_length, length)
                self.max_width = max(self.max_width, width)

                if len(lxw) == 2:
                    if not self.args.heights:
                        print("When using 'dimensions' with LxW expressions, you must also provide heights using 'heights', or use LxWxH expressions")
                        sys.exit(1)
                    for height in self.args.heights:
                        sizes += [[length, width, height]]

                if len(lxw) == 3:
                    sizes += [[length, width, float(lxw[2])]]

            # TODO: What if we fall thru here? Is that a valid and useful case
            return sizes

        else:
            sizes = []
            for length in self.args.lengths:
                for width in self.args.widths:

                    self.max_length = max(self.max_length, length)
                    self.max_width = max(self.max_width, width)

                    if width > length:
                        # This prevents duplicate trays
                        continue
                    for height in self.args.heights:
                        sizes += [[length, width, height]]
            return sizes

    def enumerate_objects(self, count_only):
        global args

        sizes = self.enumerate_tray_sizes()
        if not count_only and self.args.info:
            print("These tray sizes will be considered:")
            print("    ", sizes)

        handled_lids = []
        for s in sizes:
            length = s[0]
            width = s[1]
            height = s[2]
            if self.config['make_square_cups'] or self.config['make_divisions']:
                if (self.config['make_square_cups']):
                    self.create_square_cup_tray_variations(
                        length, width, height, count_only)

                if (self.config['make_divisions']):
                    self.create_incremental_division_variants(
                        length, width, height, count_only)

            else:
                self.create_simple_tray(length, width, height, count_only)

            self.create_custom_layouts(length, width, height, count_only)

            if (self.config['make_lids']):
                if not [length,width] in handled_lids:
                    self.create_lids(length, width, count_only)
                    handled_lids += [length,width]

        self.create_openscad_presets(count_only)

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

    def make_args(self):

        parser = argparse.ArgumentParser(
        description='Preview, render, and slice tray variations.  This script can generate a vast library of storage trays ready to be printed.  Slicing is handled by a "slice" batch/shell script that you need to implement for your slicer (that way this script does not need to know the details on how to invoke every possible slicer).',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-c', '--config', type=str,
                            help="Specify a file that contains a partial or complete library configuration.")

        parser.add_argument('-i', '--info', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Print more verbose information.")

        parser.add_argument('--show_output', type=self.str2bool, nargs="?", default=False, const=True,
                            help="Print output from subprocesses")

        parser.add_argument('--arg_file', type=open, action=self.LoadFromFile,
                        help="Specify a file that contains all the command line parameter, and use them instead.")

        g1 = parser.add_argument_group('Tray Parameters')

        g1.add_argument('-u', '--units', type=str,
                        help='Tray dimensional units, options are "in", "cm", or a numeric value. All dimensional \
                            parameters are expressed at this scale.  Fundamentally, openscad is unitless but most \
                            slicers assume that 1 unit is 1mm.  Specifying "in" is the same as speciying "25.4", \
                            and "cm" is "10.0".  However, if you want to work in, say, Rack Units (RU), will \
                            need to specify the scale numerically as "ru=44.5"')

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
                        help='Specify a fixed list of dimensions to create as a list of "LxW" string or "LxWxH" strings. If the H term is not provided then heights specified by --heights is required.')

        g1.add_argument('--openscad_presets_file', type=str, default="",
                        help="Load custom tray definitions from this OpenSCAD preset file.  All presets will be generated unless (see --preset)")

        g1.add_argument('--openscad_preset_names', type=str, nargs="+",
                        help="Generate only specified preset(s) from the specified json preset file (see --json)")

        g1.add_argument('--custom_layouts_file', type=str, 
                        help="Specify a json file containing custom layout expressions. Al l layouts will be generated unless (see --custom_layout_names)")

        g1.add_argument('--custom_layout_names', type=str, nargs="+",
                        help="Generate only specified preset(s) from the specified json_custom file (see --custom_layouts_file)")


        g0 = parser.add_argument_group('Generation Control Options')

        g0.add_argument('--oscad', type=str, nargs="+",
                            help="The openscad executable.  The default value assumes it is in your path.  Otherwise specify the full path to the executable.")

        g0.add_argument('-o', '--output_folder', type=str, default=r"",
                        help="Place all generated files into this folder.")

        g0.add_argument('--flat', type=self.str2bool, nargs="?", default=False, const=True,
                        help="When set to True, organize generated files into a folder structure based on size.  When False, all files will go into the top level folder.")

        g0.add_argument('-d', '--dryrun', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Dry run.  Just print the commands that will be executed.")

        g0.add_argument('--count_only', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Like --dryrun, but just report the count of trays that would be generated.")

        g0.add_argument('--doit', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Don't confirm starting generation of trays (a potentially long running operation).")

        g0.add_argument('-p', '--preview_only', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Only generate preview images (faster for testing).  This is fairly fast so you can visually review what will be generated and sliced.")

        g0.add_argument('--model_format', type=str,
                        help="Instruct openscad to export the rendered tray in this format.  Using 3MF is highly recommeneded.  Using STL is not recommended because OpenSCAD has trouble generating well-formed STL files. You may need to run repair utilities on it.  You can specify any other format supported by OpenSCAD to meet your needs.")

        g0.add_argument('--regen', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Force regeneration even if file exists.  Normally model files will not be re-rendered if they already exist, saving time.  But if you need to regenerate the file to effect a change, you can set this flag.")

        g0.add_argument('-s', '--slice', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Slice the model file to gcode.  With this option enabled, call the slice script to slice the generated model file to gcode.  You need to ensure the slice script works properly for your slicer of choice.  The name of the model file is passed to the script.")

        g0.add_argument('--reslice', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Reslice the model file to gcode even if it already exits.  Normally gcode files are not resliced if they exist.  Use this option for force reslicing.  This is useful it you changed a slicing profile and need to reslice everything.")

        g0.add_argument('--make_lids', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Automatically generate lids to fit generated tray sizes")

        g0.add_argument('--lid_styles', type=str, nargs="+", 
                        help="Make only listed styles.  If not provide all style will made. Options are 'recessed', 'regular', and 'stackable'")


        g2 = parser.add_argument_group('Tray Divisions',
                                    "Options in this section control how divisions (or cups) are created in the tray.")

        g2.add_argument('--make_square_cups', type=self.str2bool, nargs="?", default=False, const=True,
                        help="Automatically generate cup divisions for square cups");

        g2.add_argument('--square_cup_sizes', nargs="+", type=float, default=[],
                        help='Square cup sizes to create for each tray. This is a list of square sizes that will be created for \
                                each tray.  This is only done when when the cup size is a integer multiple of both the length and \
                                width of the tray being created. For example, a 6x4 tray will not generate square cups of size 3 because \
                                4/3 is not an integer. Requires --make_square_cups')

        g2.add_argument('--make_divisions', type=self.str2bool, nargs="?", default=False, const=True,
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

        g3.add_argument('--wall_height_scale', type=float,
                        help="Scale the dvider wall height. 1.0 = Full height (minus interlock), 0.0 = no walls at all (but that seems kind of pointless)")

        g3.add_argument('--interlock_dimensions', nargs="+", type=float,
                        help="interlocking dimensions")


        self.args = parser.parse_args()

    def determine_units(self):

        if self.config['unit_name']:
            if global_config.get("scales", {}).get(self.config['unit_name']):
                self.config['scale_units'] = global_config.get(
                    "scales", {}).get(self.config['unit_name'])
            else:
                if (self.isfloat(self.config['unit_name'])):
                    self.config['unit_name'] = "flibit"
                    self.config['scale_units'] = float(
                        self.args.units)

            # pattern for matching "<unit_name>=<scale-factor>"
            pattern = re.compile('(\w+)=(.*)')
            m = pattern.match(self.config['unit_name'])
            if m:
                self.config['unit_name'] = m.group(1)
                self.config['scale_units'] = float(m.group(2))

        if self.args.info:
            print(
                f"Units: '{self.config['unit_name']}' scale: {self.config['scale_units']} mm/{self.config['unit_name']}")

    def get_global_config(self):
        global global_config

        filename = "make_trays.json"
        if not os.path.exists(filename):
            print(f"{filename} does not exist. Cannot continue!")
            sys.exit(1)

        if self.args.info:
            print(f"Reading application data from: {filename}")

        with open(filename) as g:
            global_config = json.load(g)

    def get_config_value(self, key, arg, default=None, asList=False):
        result = None
        if global_config and global_config.get(key):
            result = global_config.get(key)
        if self.config_json and self.config_json.get(key):
            result = self.config_json.get(key)
        if arg:
            return arg
        
        if result:
            if asList:
                return result.split()

            return result

        return default

    def get_configuration(self):
        filename = self.args.config

        self.get_global_config()

        if filename and not os.path.exists(filename):
            sys.exit(f"Specified config file does not exist: {filename}")

        if self.args.info:
            print(f"Reading configuration from: {filename}")

        if filename:
            with open(filename) as f:
                self.config_json = json.load(f)

        self.config['openscad_exec'] = self.get_config_value(
            "openscad_exec", self.args.oscad, "openscad")
        self.config['unit_name'] = self.get_config_value(
            'units', self.args.units, "in")
        self.config['model_format'] = self.get_config_value(
            'model_format', self.args.model_format, "3mf")
        self.config['output_folder'] = self.get_config_value(
            'output_folder', self.args.output_folder)

        print(f"output_folder {self.config['output_folder']}")
        # Check that we can resolve an OpenSCAD executable
        if not os.path.exists(self.config['openscad_exec']):
            openscad_path = shutil.which(self.config['openscad_exec'])
            if not openscad_path:
                print(f"An OpenSCAD executable could not be resolved!")
                print(f"Check your config.json, --oscad param, or your PATH")
            else:
                if self.args.info:
                    print(f"OpenSCAD: {openscad_path} (from your path)")
        else:
            if self.args.info:
                print(f"OpenSCAD: {self.config['openscad_exec']}")

        if not self.args.count_only and self.config['output_folder'] is None:
            sys.exit(
                "You need to specify an output folder (-o <folder>) so I know where to put everything.")

        self.config['dimensions'] = self.get_config_value(
            "dimensions", self.args.dimensions, asList=True)
        self.config['lengths'] = self.get_config_value(
            "lengths", self.args.lengths, asList=True)
        self.config['widths'] = self.get_config_value(
            "widths", self.args.widths, asList=True)
        self.config['heights'] = self.get_config_value(
            "heights", self.args.heights, asList=True)

        self.determine_units()
        self.setup_other_dimensions()

        self.config['openscad_presets_json'] = None
        filename = self.get_config_value(
            "openscad_presets_file", self.args.openscad_presets_file)

        if filename and not os.path.exists(filename):
            print(f"Specified openscad preset file does not exist: {filename}")
            sys.exit(0)

        if filename:
            f = open(filename)
            self.config['openscad_presets_json'] = json.load(f)
            self.config['openscad_presets_file'] = filename

        self.config['openscad_preset_names'] = self.get_config_value(
            "openscad_preset_names", self.args.openscad_preset_names, asList=True)

        if not self.config['openscad_presets_json'] and self.config['openscad_preset_names']:
            print("Warning: Openscad presets were specified, but no OpenSCAD preset file was specified")

        if self.config['openscad_presets_json'] and self.config['openscad_preset_names']:
            for i in self.config['openscad_preset_names']:
                if not i in self.config['openscad_presets_json']['parameterSets']:
                    print(
                        f"Warning: OpenSCAD preset named '{i}' is not present in {self.config['openscad_presets_file']}")

        self.config['custom_layouts_json'] = None
        filename = self.get_config_value(
            "custom_layouts_file", self.args.custom_layouts_file)

        if filename and not os.path.exists(filename):
            print(f"Specified custom layout file does not exist: {filename}")
            sys.exit(0)

        if filename:
            f = open(filename)
            self.config['custom_layouts_json'] = json.load(f)
            self.config['custom_layouts_file'] = filename

        self.config['custom_layout_names'] = self.get_config_value(
            "custom_layout_names", self.args.custom_layout_names, asList=True)

        # TODO check layout names against those in the file

        self.config['length_div_minimum_size'] = self.get_config_value(
            "length_div_minimum_size", self.args.length_div_minimum_size)
        # if not specified anywhere, make a reasonable default based on chosen unit scale
        if not self.config['length_div_minimum_size']:
            self.config['length_div_minimum_size'] = 1 if self.config['scale_units'] > 25 else 3

        self.config['length_skip_divs'] = self.get_config_value(
            "length_skip_divs", self.args.length_skip_divs, [], asList=True)

        self.config['width_div_minimum_size'] = self.get_config_value(
            "width_div_minimum_size", self.args.width_div_minimum_size)
        # if not specified anywhere, make a reasonable default based on chosen unit scale
        if not self.config['width_div_minimum_size']:
            self.config['width_div_minimum_size'] = 1 if self.config['scale_units'] > 25 else 3

        self.config['width_skip_divs'] = self.get_config_value(
            "width_skip_divs", self.args.width_skip_divs, [], asList=True)

        self.config['flat'] = self.get_config_value(
            "flat", self.args.flat, False)

        self.config['make_square_cups'] = self.get_config_value(
            "make_square_cups", self.args.make_square_cups, False)

        self.config['square_cup_sizes'] = self.get_config_value(
            "square_cup_sizes", self.args.square_cup_sizes, asList=True)

        self.config['make_divisions'] = self.get_config_value(
            "make_divisions", self.args.make_divisions, False)

        self.config['make_lids'] = self.get_config_value(
            "make_lids", self.args.make_lids, False)

        self.config['lid_styles'] = self.get_config_value(
            "lid_styles", self.args.lid_styles, asList=True)

    def setup_other_dimensions(self):
        # Get the values from the config.json.
        self.config['wall_height_scale'] = self.get_config_value(
            "wall_height_scale", self.args.wall_height_scale)

        dims = self.get_config_value("default_dim_in_mm", None)
        if dims:
            wall_t = dims.get("wall", 1.75) / self.config['scale_units']
            floor_t = dims.get("floor", 1.75) / self.config['scale_units']
            div_t = dims.get("division", 1.75) / self.config['scale_units']
            intr_h = dims.get("interlock_height", 1.75) / \
                self.config['scale_units']
            intr_r = dims.get("interlock_recess", 1.75) / \
                self.config['scale_units']
            intr_g = dims.get("interlock_gap", 1.75) / \
                self.config['scale_units']

        wall_dims = self.get_config_value(
            "wall_dimensions", self.args.wall_dimensions)
        if wall_dims:
            if len(wall_dims) == 1:
                wall_t = wall_dims[0]
                floor_t = wall_dims[0]
                div_t = wall_dims[0]
            elif len(wall_dims) == 2:
                wall_t = wall_dims[0]
                floor_t = wall_dims[0]
                div_t = wall_dims[1]
            elif len(wall_dims) >= 3:
                wall_t = wall_dims[0]
                floor_t = wall_dims[1]
                div_t = wall_dims[2]

        interlock_dims = self.get_config_value(
            "interlock_dimensions", self.args.interlock_dimensions)
        if (interlock_dims is not None):
            if len(interlock_dims) >= 1:
                intr_h = interlock_dims[0]
                intr_r = interlock_dims[1]
            if len(interlock_dims) > 1:
                intr_r = interlock_dims[1]
            if len(interlock_dims) > 2:
                intr_g = interlock_dims[2]

        self.config['wall_defs'] = [
            "-D", f"Tray_Wall_Thickness={wall_t:.3f}",
            "-D", f"Floor_Thickness={floor_t:.3f}",
            "-D", f"Divider_Wall_Thickness={div_t:.3f}",
            "-D", f"Corner_Roundness=1.0",
            "-D", f"Interlock_Height={intr_h:.3f}",
            "-D", f"Interlock_Gap={intr_g:.3f}",
            "-D", f"Interlock_Divider_Wall_Recess={intr_r:.3f}",
            "-D", f"Divider_Wall_Height_Scale={self.config['wall_height_scale']}"
        ]
        print(self.config['wall_defs'])


    def __init__(self):
        self.config = {}

        self.result = { 
            'models': [],
            'slices': []
        }

        self.number_of_objects = 0
        self.number_of_objects_total = 0
        # Count of object generated while running, for progrss reporting.
        self.number_of_objects_generated = 0
        # Count of object sliced while running, for progrss reporting.
        self.number_of_objects_sliced = 0

        self.issued_cmds = []

        self.make_args()

        self.config_json = {}

        self.get_configuration()

        if self.args.count_only:
            self.args.dryrun = True

        self.max_length = 0
        self.max_width = 0


    def make(self):
        if self.args.info:
            print(f"Will generate {self.config['model_format']} files.")

        self.number_of_objects = 0
        self.number_of_objects_generated = 0
        self.number_of_objects_sliced = 0
        self.number_of_objects_total = 0

        print("Accumulating work units...")

        # First rip through the generator and just count the number
        # of elements that will be generated.
        self.enumerate_objects(count_only=True)

        count_summary = f"Number of objects declared:         {self.number_of_objects}\n"
        count_summary += f"Number of objects existing:         {self.number_of_objects-self.number_of_objects_generated}\n"
        count_summary += f"Number of objects to be gen/sliced: {self.number_of_objects_generated}, {self.number_of_objects_sliced}\n"

        if self.args.count_only:
            print("Count Summary:")
            print(count_summary)
            sys.exit(0)

        if self.number_of_objects == 0:
            print(count_summary)
            message = "This probably wasn't what you were expecting!\n\
You probably need to specify dimensions of the tray(s) you want to create using\n\
--dimension/--heights, or --lengths, --widths, and --height.\n\
For instance, try \"--dimension 2x4x1\"\n\
Use \"-h\" to get more help."
            sys.exit(message)

        if self.number_of_objects_generated == 0 and self.number_of_objects_sliced == 0:
            print("All your work is already done!")
            print("Use --regen and/or --reslice if you need to.")
            print(count_summary)
            sys.exit(0)

        if (not self.args.dryrun and self.number_of_objects > 0 and not self.args.doit):
            print("This is what is going to happen:")
            print(count_summary)
            print('You can disable this prompt with "--doit"')
            confirm = input("Are you ready to do this? [Y/n]: ")
            if confirm.lower().startswith('n'):
                print("OK, maybe next time...")
                sys.exit(0)

        # Record the total since running the generator will still
        # increment the number_of_objects variable.
        self.number_of_objects_total = self.number_of_objects_generated

        # Reset these so the report properly during generation
        self.number_of_objects_generated = 0
        self.number_of_objects_sliced = 0

        # Now do the real work...
        self.enumerate_objects(count_only=False)

        count_summary = f"Number of objects declared:         {self.number_of_objects}\n"
        count_summary += f"Number of objects to be gen/sliced: {self.number_of_objects_generated}, {self.number_of_objects_sliced}\n"
        count_summary += f"Number of objects existing:         {self.number_of_objects-self.number_of_objects_generated}\n"

        print("\nSummary:")
        print(count_summary)

if __name__ == "__main__":
    maker = MakeTrays()
    maker.make()
