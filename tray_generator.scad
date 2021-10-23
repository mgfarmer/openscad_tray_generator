// Specifies the measurement system and scale you want to use for your trays.  All dimensions below will be in these units.  There are presets called "imperal defaults" and "metric defaults" that make good starting points. 
Scale_Units = 25.4; // [25.4:inch, 10.0:cm]

// Specifies the tray length in the select unit scale
Tray_Length = 4.0; // [1.0:1.0:10.0]

// Specifies the tray width in the select unit scale
Tray_Width = 2.0; // [1.0:1.0:10]

// Specifies the tray height in the select unit scale
Tray_Height = 1.0; // [0.0:0.25:8]

// Create a lid for your tray.  The lid will use the same floor thickness and interlock thickness as the tray.
Create_A_Lid = false;

// Select a build mode, then use the controls in the same named tabs to specify generation parameters
Build_Mode = "Square Cups"; // ["Just the Tray", "Square Cups", "Length/Width Cups", "Length/Width Cup Ratios", "Custom Divisions per Column or Row", "Custom Ratio Divisions", "Tray Lid"]

/* [Square Cups] */
// If not 0, specifies the size of square cups to be create, both tray_length and tray_width should be a multiple of this value.  If your tray is 8x4 and you use a cup size of 1 you will get 32 cups. 
Square_Cup_Size = 1; //[1.0:0.5:10]

/* [Length/Width Cups] */
// This create the specified number of equal length cups along the length of the tray.
Cup_Along_Length = 1; //[1.0:1.0:10]

// This create the specified number of equal width cups across the width of the tray.
Cups_Across_Width = 1; //[1.0:1.0:10]

/* [Length/Width Cup Ratios] */
// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal length divisions, and [1,1,2] makes 2 equal length small divisions and one division that is twice as long.
Lengthwise_Cup_Ratios = [1,1,1,1,1];

// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal width divisions, and [1,1,2] makes 2 equal width small divisions and one divisions that is twice as wide.
Widthwise_Cup_Ratios = [1,1,1,1,1];

/* [Custom Divisions per Column or Row] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
Custom_Col_Row_Ratios = [ "|", 3, 1, 2, 1, "-", 3, 1, 1, 1, "-", 2, 1, 2, "-", 1];

// M2-M3: ["|", 5, 2.5, 2, 3, 3, 3, "*", 3, "*", 3, "*", 3, "*", 2, "*", 5]
// M4:    ["|", 5, 2.5, 2, 3, 3, 3, "*", 4, "*", 4, "*", 3, "*", 2, "*", 5]

/* [Custom Ratio Divisions] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
Custom_Division_List = [ "-", 0.333, 0.0, 0.666, "-", 0.666, 0.333, 1.0, "|", 0.333, 0.333, 1.0, "|", 0.666, 0.0, 0.666 ];
//[[ "-", 0.66, [0.0, 0.66]],[ "|", 0.66, [0.66, 1.0]]];

/* [Wall Thickness Parameters] */
// Specifies how thick the outer wall of the tray will be
Tray_Wall_Thickness = 0.07; // [0.05:0.01:0.50]

// Specifies how thick the floor will be.
Floor_Thickness = 0.07; // [0.05:0.01:0.50]

// Specifies how thick each internal cup divider will be.
Divider_Wall_Thickness = 0.07; // [0.05:0.01:0.50]

// Specifies the "roundess" of tray corners Set to 0 for square corners. Set to 1.0 for the most rounding.  This is a ratio of the wall thickness.
Corner_Roundness = 0.5; // [0.00:0.01:1.00]

/* [Lid Parameters] */
Lid_Style = "No Handle"; // ["No Handle", "Finger Holes", "Block Handle", "Bar Handle"]
Lid_Thickness = 0.07; // [0.05:0.01:0.50]
Finger_Hole_Style = "Square"; // ["Square", "Round", "Diamond"]

// Center-to-center distance between the finger holes
Finger_Hole_Separation = 2.0; // [1.0:0.25:8.0]

// Make them big enough for your fingers
Finger_Hole_Diameter = 0.5; // [0.5:0.05:2.5]

// The Heght of the handle, above the lid surface.
Block_Handle_Height = 0.375; // [0.25:0.005:1.5]

// The length of the handle
Block_or_Bar_Handle_Length = 1.0; // [0.5:0.25:5.0]

//The width of the block handle, or the diameter of the bar handle.
Block_Width_or_Bar_Diameter = 0.25; // [0.25:0.05:5.0]

// Rotate the handle around the center point of the lid.
Rotate_Handle = 0.0; // [ 0.00 : 45.00 : 180.00]

/* [Interlocking Parameters] */
// Specifies the height of the interlock panel extruded below the tray (and also the distance that the top of the dividers are below the upper tray edge. Specify 0 for non-interlocking stackers. You can still stack them, they just won't interlock.).
Interlock_Height = 0.1; // [0.0:0.01:0.25]

// Specifies the gap between the interlock extrusion and the inner face of the outer wall of the tray. Largers values will give a looser fit.
Interlock_Gap = 0.003;  // [0.0:0.001:0.020]

// Create scaled versions of all user paramters
scaled_tray_length = Scale_Units * Tray_Length;
scaled_tray_width = Scale_Units * Tray_Width;
scaled_tray_height = Scale_Units * Tray_Height;
scaled_wall_thickness = Scale_Units * Tray_Wall_Thickness;
scaled_floor_thickness = Scale_Units * Floor_Thickness;
scaled_divider_thickness = Scale_Units * Divider_Wall_Thickness;
scaled_corner_radius = Scale_Units * Corner_Roundness * Tray_Wall_Thickness; 
scaled_interlock_gap = Scale_Units * Interlock_Gap;
scaled_interlock_height = Scale_Units * Interlock_Height;

scaled_lid_thickness = Scale_Units * Lid_Thickness;
scaled_finger_hole_separation = Scale_Units * Finger_Hole_Separation;
scaled_finger_hole_diameter = Scale_Units * Finger_Hole_Diameter;
scaled_block_handle_length = Scale_Units * Block_or_Bar_Handle_Length;
scaled_block_handle_width = Scale_Units * Block_Width_or_Bar_Diameter;
scaled_block_handle_height = Scale_Units * Block_Handle_Height;

// A function to add up the elements of an vector.
function add(v, i = 0, r = 0) = i < len(v) ? add(v, i + 1, r + v[i]) : r;

function make_normalized_divs(ratios) = (
    let (total = add(ratios))
    let (mult = 1.0/total)
    let (divs = [ for(i=ratios) (i*mult) ])
    [ for(i=[len(divs)-1:-1:1]) add(divs, i, 0)]
);

module mkshell (length, width, height, wall, radius, offset=0, offset2=0) {
    // length => length of the shell
    // width => width of the shell
    // height => height of the shell
    // radius => corner radius (corresponds to wall thickness)
    
    // offset => shrinks the resulting shell by this amount in
    // both length and width (but not height).  This param is used 
    // to build the inner-cavity that is subtracted from the outer
    // shell in order to create the tray.
    
    // offset2 => used when building the "bottom" tray that is 
    // subrated from the top tray to create the stacking inter-
    // lock.  It expands the outer wall (to ensure overlap) and
    // shrinks the inner wall (to ensure a tight, but not too
    // tight, fit between the trays.
    
    l = length - offset;
    w = width - offset;
    h = height;
    
    
    cube([l-((radius+offset2/2)*2),w-offset2,h], center=true); 
    cube([l-offset2,w-((radius+offset2/2)*2),h], center=true); 
    if (radius > 0) {
        // Create the rounded corners
        translate([l/2-radius-offset2/2, w/2-radius-offset2/2, 0]) {
          cylinder(h, r=radius, center=true, $fn=20);
        }
        translate([-l/2+radius+offset2/2, w/2-radius-offset2/2, 0]) {
          cylinder(h, r=radius, center=true, $fn=20);
        }
        translate([l/2-radius-offset2/2, -w/2+radius+offset2/2, 0]) {
          cylinder(h, r=radius, center=true, $fn=20);
        }
        translate([-l/2+radius+offset2/2, -w/2+radius+offset2/2, 0]) {
          cylinder(h, r=radius, center=true, $fn=20);
        }
    }
}


/*
    Someday it might be nice to combine the make_l_div() and make_w_div modules into
    a single module so I don't have to duplicate code between then.  But for now
    these work without having to conditionally figure out the geometries.
 */
module make_l_div(pos, from=0, to=1.0, hscale=1.0) {
    // pos is a normalized position, from 0.0 to 1.0
    // from is a normalized start point, default 0.0 is one wall
    // end is a normalized end point, default 1.0 is the other wall
    // hscale can be used to scale the height of the division wall
    wid = scaled_tray_width-(scaled_divider_thickness);
    wpos = (wid*pos) - (wid/2);
    _length = (scaled_tray_length - scaled_wall_thickness);
    lstart = (_length*from) - (_length/2);
    lend = (_length*to) - (_length/2);
    llen = (lend - lstart); //to-from) * scaled_tray_length; // + (scaled_divider_thickness/2);
    hdiv = (scaled_tray_height-scaled_interlock_height) * hscale;
    union() {
        translate([lstart+(llen/2),wpos,hdiv/2]) {
            cube([llen,scaled_divider_thickness,hdiv], center=true);
        }
        translate([lstart,wpos,hdiv/2]) {
            cylinder(hdiv, r=scaled_divider_thickness/2, center=true, $fn=20);
        }
        translate([lend,wpos,hdiv/2]) {
            cylinder(hdiv, r=scaled_divider_thickness/2, center=true, $fn=20);
        }
    }
}

module make_w_div(pos, from=0, to=1.0, hscale=1.0) {
    // pos is a normalized position, from 0.0 to 1.0
    // from is a normalized start point, default 0.0 is one wall
    // end is a normalized end point, default 1.0 is the other wall
    // hscale can be used to scale the height of the division wall
    llen = scaled_tray_length-scaled_divider_thickness;
    lpos = (llen*pos) - (llen/2);
    wstart = (scaled_tray_width*from) - (scaled_tray_width/2);
    wend = (scaled_tray_width*to) - (scaled_tray_width/2);
    wlen = (to-from) * scaled_tray_width;
    hdiv = (scaled_tray_height-scaled_interlock_height) * hscale;
    translate([lpos,wstart+(wlen/2),hdiv/2]) {
        union() {
            cube([scaled_divider_thickness,wlen, hdiv], center=true);
            cylinder(hdiv, r=scaled_divider_thickness/2, center=true, $fn=20);
            if (from > 0.0) {
                translate([0,wstart,0]) {
                    cylinder(hdiv, r=scaled_divider_thickness/2, center=true, $fn=20);
                }
            }

            if (to < 1.0) {
                translate([0,wend,0]) {
                    cylinder(hdiv, r=scaled_divider_thickness/2, center=true, $fn=20);
                }
            }

        }
    }
}

module make_div(dir, pos, from=0, to=1.0, hscale=1.0) {
    if (dir == "-" || dir == "length") {
        make_l_div(pos, from, to, hscale);
    }
    if (dir == "|" || dir == "width") {
        make_w_div(pos, from, to, hscale);
    }
}

module make_lid() {
    difference() {
        union() {
            translate([0,0,scaled_lid_thickness/2]) {
                mkshell(scaled_tray_length, scaled_tray_width, scaled_lid_thickness, scaled_wall_thickness, scaled_corner_radius); 
            };
            if (scaled_interlock_height > 0) {
                translate([0,0, -scaled_interlock_height/2+0.001]) {
                    mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height, 
                    scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
                }
            }
            rotate([0,0,Rotate_Handle]) {
                if (Lid_Style == "Block Handle") {
                    translate([0,0, scaled_lid_thickness+scaled_block_handle_height/2 - 0.001]) {
                        cube([scaled_block_handle_length, scaled_block_handle_width, scaled_block_handle_height], center=true);
                    }
                }
                if (Lid_Style == "Bar Handle") {
                    translate([0,0, (scaled_lid_thickness + scaled_block_handle_width)/2]) {
                        rotate([0,90,0]) {
                            cylinder(scaled_block_handle_length, r=scaled_block_handle_width/2, center=true);
                        }
                    }
                }
            }
        }
        if (Lid_Style == "Finger Holes") {
            rotate([0,0,Rotate_Handle]) {
                height = scaled_lid_thickness+scaled_interlock_height*2;
                translate ([scaled_finger_hole_separation/2, 0, 0]) {
                    if (Finger_Hole_Style == "Round") {
                        cylinder(height, r=scaled_finger_hole_diameter/2, center=true);
                    }
                    if (Finger_Hole_Style == "Square") {
                        cube([scaled_finger_hole_diameter, scaled_finger_hole_diameter, height], center=true);
                    }
                    if (Finger_Hole_Style == "Diamond") {
                        rotate([0,0,45]) {
                            cube([scaled_finger_hole_diameter, scaled_finger_hole_diameter, height], center=true);
                        }
                    }
                }
                translate ([-scaled_finger_hole_separation/2, 0, 0]) {
                    if (Finger_Hole_Style == "Round") {
                        cylinder(height, r=scaled_finger_hole_diameter/2, center=true);
                    }
                    if (Finger_Hole_Style == "Square") {
                        cube([scaled_finger_hole_diameter, scaled_finger_hole_diameter, height], center=true);
                    }
                    if (Finger_Hole_Style == "Diamond") {
                        rotate([0,0,45]) {
                            cube([scaled_finger_hole_diameter, scaled_finger_hole_diameter, height], center=true);
                        }
                    }
                }
            }
        }
    }
}

module make_tray() {
    union() {
        translate([0,0,scaled_tray_height/2]) {
            difference() {
                // Main outer shell
                mkshell(scaled_tray_length, scaled_tray_width, scaled_tray_height, scaled_wall_thickness, scaled_corner_radius); 
                translate([0,0,scaled_floor_thickness]) {
                    // Subtract inner space..
                    mkshell(scaled_tray_length, scaled_tray_width, scaled_tray_height, 
                        scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2);
                }
            };
        };
        if (scaled_interlock_height > 0) {
            translate([0,0, -scaled_interlock_height/2+0.001]) {
                mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height, 
                scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
            }
        }
    }
}

module make_dividers(divs, orient="length", from=0, to=1.0, hscale=1.0) {
    // divs is a normalized array of 
    // positions for each divider to create.
    for ( i = divs ){
        make_div(orient, i, from, to, hscale);
    }
}

module make_equal_cups(num_divs, orient="length") {
    increment = 1.0/num_divs;
    for ( i = [increment : increment : (1.0-increment)] ){
        make_div(orient, i);
    }
}

module test_tray() {
    union() {
        make_tray();
        make_cups([1, 1, 2]);
        make_cups([1, 1, 2],"width");
    }
}

module make_cups(ratios, orient="length", from=0.0, to=1.0, hscale=1.0) {
    total = add(ratios);
    mult = 1.0/total;
    divs = [ for(i=ratios) (i*mult) ];
    divs2 = make_normalized_divs(ratios);
    make_dividers(divs2, orient, from, to, hscale);
}

if (Build_Mode == "Just the Tray") {
    make_tray();
}

if (Build_Mode == "Square Cups") {
    lcups = Tray_Length/Square_Cup_Size;
    wcups = Tray_Width/Square_Cup_Size;
    union() {
        make_tray();
        make_equal_cups(lcups, "width");
        make_equal_cups(wcups, "length");
    }
}

if (Build_Mode == "Length/Width Cups") {
    union() {
        make_tray();
        if (Cup_Along_Length > 0) {
            make_equal_cups(Cup_Along_Length, "width");
        }
        if (Cups_Across_Width > 0) {
            make_equal_cups(Cups_Across_Width, "length");
        }
    }
}

if (Build_Mode == "Length/Width Cup Ratios") {
    union() {
        make_tray();
        if (Cup_Along_Length > 0) {
            make_cups(Lengthwise_Cup_Ratios, "width");
            //make_cups([1,2,1,2,1], "width");
        }
        if (Cups_Across_Width > 0) {
            make_cups(Widthwise_Cup_Ratios, "length");
        }
    }
}

function sub_vect(vect, start) = [for( i = [start : 1 : len(vect)-1]) vect[i] ];

module make_walls(section, mode, walls, divisions) {
    if (section < len(divisions)-1) {
        from = divisions[section];
        to = divisions[section+1];
        if (is_num(walls[2])) {
            ratios = [ for( i = [1 : 1 : walls[1]]) walls[1+i] ];
            make_cups(ratios, mode, from, to);
            wall_specs = sub_vect(walls, 2 + walls[1]); 
            make_walls(section+1, mode, wall_specs, divisions);
        }
        else {
            ratios = [ for( i = [1 : 1 : walls[1]]) 1 ];
            make_cups(ratios, mode, from, to);
            wall_specs = sub_vect(walls, 2); 
            make_walls(section+1, mode, wall_specs, divisions);
        }
    }
}

if (Build_Mode == "Custom Divisions per Column or Row") {
    union() {
        make_tray();
        mode = Custom_Col_Row_Ratios[0];
        other_mode = (mode == "|")?"-":"|";
        divs = Custom_Col_Row_Ratios[1];
        if (is_num(Custom_Col_Row_Ratios[2])) {
            ratios = [ for( i = [0 : 1 : divs-1]) Custom_Col_Row_Ratios[2+i] ];
            make_cups(ratios, mode);
            divisions = concat( [0.0], make_normalized_divs(ratios), [1.0]);
            start = 2 + divs;
            wall_specs = sub_vect(Custom_Col_Row_Ratios, start);
            make_walls(0, other_mode, wall_specs, divisions);
        }
        else {
            make_equal_cups(divs, mode);
            divisions = concat( [0.0], make_normalized_divs([ for( i = [0 : 1 : divs-1]) 1 ]), [1.0]);
            wall_specs = sub_vect(Custom_Col_Row_Ratios, 2);
            make_walls(0, other_mode, wall_specs, divisions);
        }
    }
}

module make_custom_div(div_list) {
    if (len(div_list) > 3) {
        dir = div_list[0];
        pos = div_list[1];
        from = div_list[2];
        to = div_list[3];
        make_div(dir, pos, from, to);
        next_list = sub_vect(div_list, 4);
        make_custom_div(next_list);
    }
}

if (Build_Mode == "Custom Ratio Divisions") {
    union() {
        make_tray();
        make_custom_div(Custom_Division_List);
    }
}

if (Build_Mode == "Tray Lid") {
    make_lid();
}

if (Build_Mode != "Tray Lid" && Create_A_Lid == true) {
    translate([0, (scaled_tray_width + Scale_Units), 0]) {
        make_lid();
    }
}
