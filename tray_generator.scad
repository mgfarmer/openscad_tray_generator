/* [Tray Dimensions and Mode] */
// Specifies the measurement system and scale you want to use for your trays.  All dimensions below will be in these units.  There are presets called "imperal defaults" and "metric defaults" that make good starting points. 
Scale_Units = 25.4; // [25.4:inch, 10.0:cm]

// When checked, the length, width, and height dimension are the external dimensions of the tray, when not checked they are the internal dimensions of the tray and the external dimensions will be adjusted accordingly.
Dimensions_Are_External = true;

// Specifies the tray length in the select unit scale.
Tray_Length = 8.00;  // [0.0:0.001:25.00]

// Specifies the tray width in the select unit scale. In "Storage Slot" mode this dimension represents the total internal dimension adjusted for divider wall thickenss. In other modes, just know that each divider wall reduces the available internal space.
Tray_Width = 4.00; // [0.0:0.001:25.00]

// Specifies the tray height in the select unit scale.  Stackable trays (Interlock Height > 0) will increase the actual height by the height of the interlocking extrusion.
Tray_Height = 1.00; // [0.0:0.001:25.00]

// Select a build mode then use the controls in the same named sections to specify generation parameters
Build_Mode = "Just_the_Tray"; // ["Just_the_Tray", "Square_Cups", "Length_Width_Cups", "Length_Width_Cup_Ratios", "Storage_Slots", "Custom_Divisions_per_Column_or_Row", "Custom_Ratio_Divisions", "Tray_Lid"]


/* [Build Mode: Square Cups] */
// If not 0, specifies the size of square cups to be created. Both tray_length and tray_width must be an integer multiple of this value.  If your tray is 8x4 and you use a cup size of 1 you will get 32 cups. 
Square_Cup_Size = 1; //[0.0:0.001:10]

/* [Build Mode: Length/Width Cups] */
// This create the specified number of equal length cups along the length of the tray.
Cups_Along_Length = 1; //[1.0:1.0:40]

// This create the specified number of equal width cups across the width of the tray.
Cups_Across_Width = 1; //[1.0:1.0:40]

/* [Build Mode: Length/Width Cup Ratios] */
// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal length divisions, and [1,1,2] makes 2 equal length small divisions and one division that is twice as long.
Lengthwise_Cup_Ratios = [1,1,2,1,1];

// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal width divisions, and [1,1,2] makes 2 equal width small divisions and one divisions that is twice as wide.
Widthwise_Cup_Ratios = [1,1,2,1,1];

/* [Build Mode: Storage Slots] */
Storage_Slot_Width = 0.08; // [0.02 : 0.001 : 1]
Minimum_Storage_Slot_Separation = 0.08; // [0.02 : 0.001 : 1]
Storage_Wall_Width = 0.25; // [0.02 : 0.001 : 1]
Number_Of_Columns = 1;

/* [Build Mode: Custom Divisions per Column or Row] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
Custom_Col_Row_Ratios = [1,5,2,2,2,1.5,2,0,3,0,3,0,3,0,2,0,5];

// M2-M3: ["|", 5, 2.5, 2, 3, 3, 3, "*", 3, "*", 3, "*", 3, "*", 2, "*", 5]
// M4:    ["|", 5, 2.5, 2, 3, 3, 3, "*", 4, "*", 4, "*", 3, "*", 2, "*", 5]

/* [Build Mode: Custom Ratio Divisions] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
Custom_Division_List = [ "-", 0.333, 0.0, 0.666, "-", 0.666, 0.333, 1.0, "|", 0.333, 0.333, 1.0, "|", 0.666, 0.0, 0.666 ];
//[[ "-", 0.66, [0.0, 0.66]],[ "|", 0.66, [0.66, 1.0]]];

/* [Outer Wall Parameters] */
// Specifies how thick the outer wall of the tray will be
Tray_Wall_Thickness = 0.07; // [0.05:0.001:0.50]

// Specifies how thick the floor will be.
Floor_Thickness = 0.07; // [0.05:0.001:0.50]

// Specifies the "roundess" of tray corners Set to 0 for square corners. Set to 1.0 for the most rounding.  This is a ratio of the wall thickness. This is overriden with making box tops with interlocking pins.
Corner_Roundness = 1.0; // [0.00:0.001:1.00]

/* [Divider Wall Parameters] */
// Specifies how thick each internal cup divider will be.
Divider_Wall_Thickness = 0.07; // [0.05:0.001:0.50]

// A fuzzy knob to scale the wall height down when all other knobs fails to accomplish what you want.
Divider_Wall_Height_Scale = 1.0;  // [0.05:0.001:1.50]


/* [Divider Wall Finger Slots] */

// Create finger slots in divider walls.
Make_Finger_Slots = false;

// Finger slots cut length-wise walls, or width-wise walls
Lengthwise_Finger_Slot = true;

// Width of the finger slots.
Finger_Slot_Width = 0.0; // [0.00:0.001:1.00]

// Normalized position for the finger slots.
Finger_Slot_Position = 0.5; // [0.00:0.001:1.00]

// Normalized radius where 1=divider wall height, and 0=zero
Finger_Slot_Radius = 1.0; // [0.00:0.001:10.00]

// Normalized lift of the slot above the floor
Finger_Slot_Lift = 0.2; // [0.00:0.001:1.00]

/* [Tray Insert Parameters] */

// Size this tray to fit into a bigger tray.  Tray Length and Width is the size of the tray it will fit into. This tray will be just small enough to rest inside the outer tray. The outer tray should have division walls for the insert tray to rest on, that are sized down appropriately, or add corner posts. See "Insert Tray Heighth". Using this will force the Interlock Height to 0
Make_Insert_Tray = false;

// Apply this to the main tray.  Use this to adapt a larger tray to accespt an smaller insert tray. Set this to be the same height as the height of the insert tray. 
Insert_Tray_Height = 0.0;  // [0.00:0.001:2.00]

// Apply this to the insert tray. Use this to specify how much free space is between the inner wall of the outer tray and the outer wall of the inner tray. Larger values will create a looser fit.
Insert_Tray_Gap = 0.03;  // [0.00:0.001:2.00]

// Corner posts give the insert something to rest on if you don't want any dividers walls in the main tray.
Add_Corner_Posts = false;

// Size of the corner post
Corner_Post_Size = 0.2; //[0.1:0.001:1.50]


/* [Lid Parameters] */
// Create a lid for your tray.  (See Lid and Interlock Parameters).
Create_A_Lid = false;


Lid_Handle_Style = "Finger_Holes"; // ["No_Handle", "Finger_Holes"]

// How thick should the lid be.  This is the height above the top edge of the tray.  If you want a fully recessed lid, specify 0 here.
Lid_Thickness = 0.07; // [0.00:0.001:0.50]

// Creates a raised edge so a tray can be stacked on top of the lid.  This is only used when Lid_Thickness > 0.
Interlocking_Lid = false;

// Normally the divider wall height is lowered to make room for the interlock extrusion.  If you want room for a recessed lid, check this.  Only used when Lid Thickness == 0.
Make_Room_For_Recessed_Lid_And_Stacked_Tray = false; 


// Only used when creating a tray too.  Creates a raised or recessed grid on top of the lid that matches the dividers, for labels, of course.
Label_Lid = false;

// Specify whether you want a raised label grid or a recessed label grid.
Label_Lid_Style = "Raised"; // ["Raised", "Recessed"]

// How many finger holes do you want.
Number_Of_Finger_Holes = 1; // [1, 2]

Finger_Hole_Style = "Round"; // ["Square", "Round", "Diamond"]

// Normalized length-wise position from the center of the tray to the finger hole(s). 0 will put the hole(s) in the center. 1.0 will center the hole on the outside of the edge.
Finger_Hole_Position = 1.0; // [0.0:0.001:1.50]

// Make them big enough for your fingers
Finger_Hole_Diameter = 0.75; // [0.5:0.001:5.00]

// Rotate the handle around the center point of the lid.
Rotate_Handle = 0.0; // [ 0.00 : 45.00 : 180.00]

/* [Box Top Parameters] */
// Create a lid for your tray.  (See Lid and Interlock Parameters).
Create_A_Box_Top = false;

// Internal or external height of the box top, see "Dimensions Are External"
Box_Top_Height = 0.75;

// Create matching dividers in the box top.  Can provide additional stiffness on large tops.
With_Dividers = false;

// Choose between overlappping shell edge nad no interlock.
Box_Top_Interlock_Type = "Shell"; // ["Shell", "None"]

Box_Top_Interlock_Height = 0.15; // [0.0:0.001:1.00]

// Create one or more finger detents to help open the box.  If you choose two they will be on opposite sides of the box. These are created in the main box, not the box top.
Finger_Detents = "One"; // ["None", "One", "Two"]

Detent_Orientation = "Length"; // ["Length", "Width"]

// A fuzzy knob to tune the height of the finger detent.
Detent_Height = 0.95; // [0.0: 0.001 : 1.00] 

// A fuzzy know to tune the width of the detent.
Detent_Width = 0.5; // [0.0: 0.001: 1.00]

/* [Interlocking Parameters] */
// Specifies the height of the interlock panel extruded below the tray (and also the distance that the top of the dividers are below the upper tray edge. Specify 0 for non-interlocking stackers. You can still stack them, they just won't interlock.).
Interlock_Height = 0.0; // [0.0:0.001:0.25]

// Only used when Interlock_Height==0, and intended for use with interlocking lids and trays, recessed lids, or to give a little more recess to insert trays.  When Interlock_Height > 0, it is used instead.
Interlock_Divider_Wall_Recess = 0.0; // [0.0:0.001:0.25]

// Specifies the gap between the interlock extrusion and the inner face of the outer wall of the tray. Largers values will give a looser fit.
Interlock_Gap = 0.003;  // [0.0:0.001:0.10]

// Make sure all variables for the customizer are declared above this line.  Other globals can be put below
// this line to ensure they don't show up in the customizer UI.
module __Customizer_Limit__ () {}


Perimeter_Interlock = false;
with_shell_interlock = Create_A_Box_Top && Box_Top_Interlock_Type == "Shell";
with_storage_slots = Build_Mode == "Storage_Slots";

make_room_for_recessed_lid = Make_Room_For_Recessed_Lid_And_Stacked_Tray && Lid_Thickness == 0;
Label_Lid_Height = 0.3; // mm

// Create scaled versions of all user paramters
scaled_wall_thickness = Scale_Units * Tray_Wall_Thickness;
scaled_floor_thickness = Scale_Units * Floor_Thickness;
scaled_divider_thickness = Scale_Units * Divider_Wall_Thickness;
scaled_Insert_Tray_Gap = Scale_Units * Insert_Tray_Gap;

_external_tray_length = Dimensions_Are_External?Tray_Length:(Tray_Length+2*Tray_Wall_Thickness);

xtrw = with_storage_slots?((Number_Of_Columns-1)*Divider_Wall_Thickness):0;
//echo(xtrw=xtrw);
_external_tray_width = Dimensions_Are_External?Tray_Width:((Tray_Width+2*Tray_Wall_Thickness)+xtrw); 
    //+ (with_storage_slots?(Number_Of_Columns-1*Divider_Wall_Thickness):0));
_external_tray_heigth = Dimensions_Are_External?Tray_Height:(Tray_Height+Floor_Thickness);
_external_box_height = Dimensions_Are_External?Box_Top_Height:(Box_Top_Height+Floor_Thickness);

_internal_tray_length = !Dimensions_Are_External?Tray_Length:(Tray_Length-2*Tray_Wall_Thickness);
_internal_tray_width = !Dimensions_Are_External?Tray_Width+xtrw:((Tray_Width-2*Tray_Wall_Thickness));
_internal_tray_heigth = !Dimensions_Are_External?Tray_Height:(Tray_Height-Floor_Thickness);
_internal_box_height = !Dimensions_Are_External?Box_Top_Height:(Box_Top_Height+Floor_Thickness);

echo(_internal_tray_length=_internal_tray_length, _external_tray_length=_external_tray_length);
echo(_internal_tray_width=_internal_tray_width, _external_tray_width=_external_tray_width);
echo(_internal_tray_heigth=_internal_tray_heigth, _external_tray_heigth=_external_tray_heigth);


scaled_tray_length = (Scale_Units * _external_tray_length) - 
    (2*((Make_Insert_Tray==true)?scaled_wall_thickness+scaled_Insert_Tray_Gap:0));
scaled_tray_width = (Scale_Units * _external_tray_width) - 
    (2*((Make_Insert_Tray==true)?scaled_wall_thickness+scaled_Insert_Tray_Gap:0));
scaled_tray_height = Scale_Units * _external_tray_heigth;

x_bt_ht = with_storage_slots?Box_Top_Interlock_Height:0;

scaled_box_top_height = Scale_Units * (_external_box_height + x_bt_ht);

scaled_corner_radius = Scale_Units * Corner_Roundness * Tray_Wall_Thickness; 
scaled_interlock_gap = Scale_Units * Interlock_Gap;
scaled_interlock_height = (Make_Insert_Tray==true)?0:(Scale_Units * Interlock_Height);
scaled_Interlock_Divider_Wall_Recess = Scale_Units * ((scaled_interlock_height==0)?Interlock_Divider_Wall_Recess:Interlock_Height);
scaled_lid_thickness = Scale_Units * Lid_Thickness;
scaled_finger_hole_diameter = Scale_Units * Finger_Hole_Diameter;
scaled_insert_tray_height = Scale_Units * Insert_Tray_Height;
scaled_divider_height = scaled_tray_height -
    ((make_room_for_recessed_lid?2:1)*scaled_Interlock_Divider_Wall_Recess) - 
    ((make_room_for_recessed_lid && Label_Lid && Label_Lid_Style == "Raised")?(Label_Lid_Height+0.01):0) -
    scaled_insert_tray_height;

scaled_corner_post_size = Scale_Units * Corner_Post_Size;


scaled_box_top_interlock_height = Scale_Units * Box_Top_Interlock_Height;

// A function to add up the elements of an vector.
function add_vect(v, i = 0, r = 0) = i < len(v) ? add_vect(v, i + 1, r + v[i]) : r;

// Extract all elements starting at 'start' into a new vector
function sub_vect(vect, start) = [for( i = [start : 1 : len(vect)-1]) vect[i] ];

// Reverse the elements in a vector, returning a new vector, of course
function rev_vect(vect) = [for( i = [len(vect)-1 : -1 : 0]) vect[i] ];

// Convert a list of ratios into a list of normalized division.
function make_normalized_divs(ratios) = (
    let (total = add_vect(ratios))
    let (mult = 1.0/total)
    let (divs = [ for(i=ratios) (i*mult) ])
    [ for(i=[len(divs)-1:-1:1]) add_vect(divs, i, 0)]
);

module mkshell(length, width, height, wall, c_radius, offset=0, offset2=0) {
    // length => length of the shell
    // width => width of the shell
    // height => height of the shell
    // radius => corner radius (corresponds to wall thickness)
    
    // offset => shrinks the resulting shell by this amount in
    // both length and width (but not height).  This param is used 
    // to build the inner-cavity that is subtracted from the outer
    // shell in order to create the tray.
    
    // offset2 => used when building the "bottom" tray that is 
    // subtracted from the top tray to create the stacking inter-
    // lock.  It expands the outer wall (to ensure overlap) and
    // shrinks the inner wall (to ensure a tight, but not too
    // tight, fit between the trays.
    
    l = length - offset;
    w = width - offset;
    h = height;
    cyl_h = h;
    cyl_h_xlat = 0;
    radius = c_radius;
    
    difference() {
        union() {
            cube([l-((radius+offset2/2)*2),w-offset2,h], center=true); 
            cube([l-offset2,w-((radius+offset2/2)*2),h], center=true); 
            if (radius > 0) {
                // Create the rounded corners
                diam = 2*radius;
                rad = diam/2;
                translate([l/2-radius-offset2/2, w/2-radius-offset2/2, cyl_h_xlat]) {
                    cylinder(cyl_h, r=radius, center=true, $fn=20);
                }
                translate([-l/2+radius+offset2/2, w/2-radius-offset2/2, cyl_h_xlat]) {
                    cylinder(cyl_h, r=radius, center=true, $fn=20);
                }
                translate([l/2-radius-offset2/2, -w/2+radius+offset2/2, cyl_h_xlat]) {
                    cylinder(cyl_h, r=radius, center=true, $fn=20);
                }
                translate([-l/2+radius+offset2/2, -w/2+radius+offset2/2, cyl_h_xlat]) {
                    cylinder(cyl_h, r=radius, center=true, $fn=20);
                }
            }
        }
    }
}

/*
    All division wall construction comes down to this and the next module.  Combinging
    these into a singel module, so far, has resulted in code that is really hard to
    understand, so, for now, they are two separate modules that are easier to grasp,
    but require a bit more maintenance.
 */
module make_l_div(pos, height, from=0, to=1.0, hscale=1.0, allow_half_walls=false, divt=scaled_divider_thickness) {
    tray_1_dim = _internal_tray_width * Scale_Units + (allow_half_walls?0:divt);
    tray_2_dim = scaled_tray_length;
    // pos is a normalized position, from 0.0 to 1.0
    // from is a normalized start point, default 0.0 is one wall
    // end is a normalized end point, default 1.0 is the other wall
    // hscale can be used to scale the height of the division wall
    dim = tray_1_dim;
    wpos = (tray_1_dim*pos) - (tray_1_dim/2);

    op_dim = tray_2_dim; 
    start = (op_dim*from) - (op_dim/2) + ((from==0)?scaled_wall_thickness:divt)/2;
    end = (op_dim*to) - (op_dim/2) - ((to==1)?scaled_wall_thickness:divt)/2;
    dlen = (end - start); 
    tmp_hdiv = (height-scaled_floor_thickness) * hscale * Divider_Wall_Height_Scale;
    hdiv = tmp_hdiv<0?height:tmp_hdiv;
    sft = tmp_hdiv<0?0:scaled_floor_thickness;

    xlat = hdiv/2+sft-0.001;
    union() {
        translate([start+(dlen/2),wpos,xlat]) {
            cube([dlen,divt,hdiv], center=true);
        }
        if (from > 0.0) {
            translate([start,wpos,xlat]) {
                cylinder(hdiv, r=divt/2, center=true, $fn=20);
            }
        }
        if (to < 1.0) {
            translate([end,wpos,xlat]) {
                cylinder(hdiv, r=divt/2, center=true, $fn=20);
            }
        }
    }
}

module make_w_div(pos, height, from=0, to=1.0, hscale=1.0, allow_half_walls=false, divt=scaled_divider_thickness) {
    // pos is a normalized position, from 0.0 to 1.0
    // from is a normalized start point, default 0.0 is one wall
    // end is a normalized end point, default 1.0 is the other wall
    // hscale can be used to scale the height of the division wall
    llen = _internal_tray_length * Scale_Units  + (allow_half_walls?0:divt);
    //echo(pos=pos, llen=llen, _internal_tray_length=_internal_tray_length);
    lpos = (llen*pos) - (llen/2);
    _length = scaled_tray_width ;
    wstart = (_length*from) - (_length/2) + ((from==0)?scaled_wall_thickness:divt)/2;
    wend = (_length*to) - (_length/2) - ((to==1)?scaled_wall_thickness:divt)/2;
    wlen = (wend-wstart);
    tmp_hdiv = (height-scaled_floor_thickness) * hscale * Divider_Wall_Height_Scale;
    hdiv = tmp_hdiv<0?height:tmp_hdiv;
    sft = tmp_hdiv<0?0:scaled_floor_thickness;
    xlat = hdiv/2+sft-0.001;
    union() {
        translate([lpos,wstart+(wlen/2),xlat]) {
            cube([divt,wlen, hdiv], center=true);
        }
        if (from > 0.0) {
            translate([lpos,wstart,xlat]) {
                cylinder(hdiv, r=divt/2, center=true, $fn=20);
            }
        }
        if (to < 1.0) {
            translate([lpos,wend,xlat]) {
                cylinder(hdiv, r=divt/2, center=true, $fn=20);
            }
        }
    }
}

module make_div(dir, pos, height, from=0, to=1.0, hscale=1.0, allow_half_walls=false, divt=scaled_divider_thickness) {
    if (dir == 0 || dir == "-" || dir == "length") {
        make_l_div(pos, height, from, to, hscale, allow_half_walls, divt);
    }
    if (dir == 1 || dir == "|" || dir == "width") {
        make_w_div(pos, height, from, to, hscale, allow_half_walls, divt);
    }
}

module make_lid() {
    label_div_offset = (Label_Lid == true)?Label_Lid_Height:0.0;
    interlock_height = (scaled_interlock_height==0)?scaled_Interlock_Divider_Wall_Recess:scaled_interlock_height;
    label_scale = 1.0; //scaled_lid_thickness > 0?1.0:0.95;
    rotate([0,0,0]) {
        difference() {
            union() {
                // Create the part of the lid above the tray edge.
                if (scaled_lid_thickness > 0) {
                    translate([0,0,scaled_lid_thickness/2]) {
                        mkshell(scaled_tray_length, scaled_tray_width, scaled_lid_thickness, scaled_wall_thickness, scaled_corner_radius); 
                    };
                }
                if (interlock_height > 0) {
                    // Create the part of the lid recessed below the tray edge.
                    translate([0,0, -interlock_height/2+0.001]) {
                        if (Perimeter_Interlock == false) {
                            mkshell(scaled_tray_length, scaled_tray_width, interlock_height, 
                            scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
                        }
                        else {
                            difference() {
                                mkshell(scaled_tray_length, scaled_tray_width, interlock_height, 
                                scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
                                mkshell(scaled_tray_length, scaled_tray_width, interlock_height+0.002, 
                                scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap+scaled_wall_thickness*2);
                            }
                        }
                    }
                }
                if (Interlocking_Lid == true && scaled_lid_thickness > 0) {
                    // Create a raised edge so a tray placed on top of this tray will stack interlocked.
                    translate([0,0,(scaled_lid_thickness+scaled_interlock_height/2)-0.001]) {
                        difference() {
                            mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height+label_div_offset+0.001, scaled_wall_thickness, scaled_corner_radius); 
                            mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height+label_div_offset+0.1, 
                            scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
                        }
                    }
                }
                if (Label_Lid == true && Label_Lid_Style == "Raised") {
                    difference() {
                        intersection() {
                            translate([0,0,scaled_lid_thickness-0.001]) {
                                //scale the dividers in XY so they dont extend past a recessed tray edge.
                                scale([label_scale,label_scale,1]) {
                                    make_tray_cups(label_div_offset);
                                }
                            }
                            if (scaled_lid_thickness > 0) {
                                translate([0,0,scaled_lid_thickness]) {
                                    mkshell(scaled_tray_length, scaled_tray_width, scaled_lid_thickness+2, scaled_wall_thickness, scaled_corner_radius); 
                                };
                            }
                            else {
                                translate([0,0,scaled_lid_thickness]) {
                                    mkshell(scaled_tray_length-scaled_wall_thickness*2-scaled_interlock_gap, 
                                        scaled_tray_width-scaled_wall_thickness*2-scaled_interlock_gap, scaled_lid_thickness+2, scaled_wall_thickness, scaled_corner_radius); 
                                };
                            }
                        }
                    }
                }
            }

             if (Label_Lid == true && Label_Lid_Style == "Recessed") {
                intersection() {
                    translate([0,0,scaled_lid_thickness-0.5]) {
                        scale([label_scale,label_scale,20]) {
                            make_tray_cups(label_div_offset);
                        }
                    }
                    translate([0,0, scaled_lid_thickness-0.5]) {
                        mkshell(scaled_tray_length, scaled_tray_width, interlock_height, 
                        scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
                    }
                }
             }

            // Create subtractive handles, if specified.
            if (Lid_Handle_Style == "Finger_Holes") {
                rotate([0,0,Rotate_Handle]) {
                    height = (scaled_lid_thickness+scaled_interlock_height)*8;
                    hole_offset = scaled_tray_length/2 * Finger_Hole_Position;
                    translate ([hole_offset, 0, 0]) {
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
                    if (Number_Of_Finger_Holes == 2) {
                        translate ([-hole_offset, 0, 0]) {
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
    }
}

module make_tray(height, wall_thickness, is_box_top=false) {
    union() {
        translate([0,0,height/2]) {
            difference() {
                // Main outer shell
                mkshell(scaled_tray_length, scaled_tray_width, height, wall_thickness, scaled_corner_radius); 
                translate([0,0,scaled_floor_thickness]) {
                    corner_radius = scaled_corner_radius;
                    // Subtract inner space..
                    mkshell(scaled_tray_length, scaled_tray_width, height, 
                        wall_thickness, corner_radius, wall_thickness*2);
                }
            };
        };
        // Make the bottom extrusion that allows this tray to interlock with a tray below for secure stacking.
        if (!is_box_top && scaled_interlock_height > 0) {
            translate([0,0, -scaled_interlock_height/2+0.001]) {
                mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height, 
                wall_thickness, scaled_corner_radius, wall_thickness*2, scaled_interlock_gap);
            }
        }
    }
}

module make_box_top_shell_interlock(height, wall_thickness, is_box_top=false) {
    if (with_shell_interlock) {
        translate([0,0,(height/2) + height - scaled_box_top_interlock_height]) { //2*height - scaled_box_top_interlock_height]) {
            ofs = wall_thickness + (is_box_top?-1:1)*scaled_interlock_gap/2;
            if (is_box_top) {
                mkshell(scaled_tray_length, scaled_tray_width, height+0.002, wall_thickness, scaled_corner_radius, ofs); 
            }
            else {
                difference() {
                    mkshell(scaled_tray_length, scaled_tray_width, height, wall_thickness, scaled_corner_radius, -ofs); 
                    mkshell(scaled_tray_length, scaled_tray_width, height+0.002, wall_thickness, scaled_corner_radius, ofs); 
                }
            }
        }
    }
}

module make_dividers(divs, height, orient="length", from=0, to=1.0, hscale=1.0) {
    // divs is a normalized array of 
    // positions for each divider to create.
    for ( i = divs ){
        make_div(orient, i, height, from, to, hscale);
    }
}

module make_equal_cups(num_divs, height, orient="length", from=0.0, to=1.0) {
    increment = 1.0/num_divs;
    for ( i = [increment : increment : (1.0-increment)] ){
        make_div(orient, i, height, from);
    }
}

module make_slot_walls(num_divs, height, orient="length", from=0.0, to=1.0, divt=scaled_divider_thickness) {
    increment = 1.0/num_divs;

    difference() {
        for ( i = [0 : increment : 1.0] ){
            make_div(orient, i, height, from=from, to=to, allow_half_walls = true, divt=divt);
        }
        
        itw = _internal_tray_width * Scale_Units + scaled_wall_thickness;
        sww = Storage_Wall_Width * Scale_Units;
        cw = itw/Number_Of_Columns;
        winc = 1.0/Number_Of_Columns;
        hwall = scaled_divider_thickness/2;
        for ( i = [0 : winc : 1.0-winc]) {
            start = itw * i + sww;
            end =  itw * (i+winc) - sww;
            center = start + (end - start) / 2 - itw/2;
            remove_width = end-start;
            dc = cw - start - remove_width/2;
            //echo(dc=dc);
            //echo(i=i, start=start, end=end, center=center, remove_width=remove_width);
            translate([0,center,scaled_tray_height/2+scaled_floor_thickness]) {
                cube([_internal_tray_length*Scale_Units,remove_width,scaled_tray_height], center=true);
            }
        }
    }
}

module make_cups(ratios, height, orient="length", from=0.0, to=1.0, hscale=1.0) {
    divs2 = make_normalized_divs(ratios);
    make_dividers(divs2, height, orient, from, to, hscale);
}

module make_walls(section, mode, walls, height, divisions) {
    //echo(section, mode, walls)
    if (section < len(divisions)-1) {
        from = divisions[section];
        to = divisions[section+1];
            if (len(walls) > 2 && walls[2] > 0) {
                ratios = rev_vect([ for( i = [1 : 1 : walls[1]]) walls[1+i] ]);
                make_cups(ratios, height, mode, from, to);
                wall_specs = sub_vect(walls, 2 + walls[1]); 
                make_walls(section+1, mode, wall_specs, height, divisions);
            }
            else {
                ratios = rev_vect([ for( i = [1 : 1 : walls[1]]) 1 ]);
                make_cups(ratios, height, mode, from, to);
                wall_specs = sub_vect(walls, 2); 
                make_walls(section+1, mode, wall_specs, height, divisions);
            }
    }
}

module make_custom_div(div_list, height) {
    if (len(div_list) > 3) {
        dir = div_list[0];
        pos = div_list[1];
        from = div_list[2];
        to = div_list[3];
        make_div(dir, pos, height, from, to);
        next_list = sub_vect(div_list, 4);
        make_custom_div(next_list, height);
    }
}

module make_equal_cup_dividers(height) {
    if (Square_Cup_Size != 0) {
        ldivs = Tray_Length/Square_Cup_Size;
        wdivs = Tray_Width/Square_Cup_Size;
        if (ldivs == floor(ldivs) && wdivs == floor(wdivs)) {
            make_equal_cups(Tray_Length/Square_Cup_Size, height, "width");
            make_equal_cups(Tray_Width/Square_Cup_Size, height, "length");
        }
        else {
            echo("Warning: Specified square cup size does not fit dimensions</b>");
        }
    }
}

module make_lw_cups(height) {
    make_equal_cups(Cups_Along_Length, height, "width");
    make_equal_cups(Cups_Across_Width, height, "length");
}

module make_lw_cup_ratios(height) {
    make_cups(Lengthwise_Cup_Ratios, height, "width");
    make_cups(Widthwise_Cup_Ratios, height, "length");
}

module make_custom_div_ratios(height) {
    mode = Custom_Col_Row_Ratios[0];
    other_mode = (mode == 1)?0:1;
    divs = Custom_Col_Row_Ratios[1];
    if (Custom_Col_Row_Ratios[2] > 0) {
        ratios = rev_vect([ for( i = [0 : 1 : divs-1]) Custom_Col_Row_Ratios[2+i] ]);
        make_cups(ratios, height, mode);
        divisions = concat( [0.0], make_normalized_divs(ratios), [1.0]);
        start = 2 + divs;
        wall_specs = sub_vect(Custom_Col_Row_Ratios, start);
        make_walls(0, other_mode, wall_specs, height, divisions);
    }
    else {
        make_equal_cups(divs, height, mode);
        divisions = concat( [0.0], make_normalized_divs([ for( i = [0 : 1 : divs-1]) 1 ]), [1.0]);
        wall_specs = sub_vect(Custom_Col_Row_Ratios, 2);
        make_walls(0, other_mode, wall_specs, height, divisions);
    }
}

module make_post(height, radius) {
    union() {
        cylinder(height, r=radius, $fn=20);
        translate([0,-radius,0]) {
            cube([scaled_corner_post_size/2, scaled_corner_post_size, height]);
        }
        translate([-radius,0,0]) {
            cube([scaled_corner_post_size, scaled_corner_post_size/2, height]);
        }
    }
}

module make_corner_posts(height) {
    //echo("make_corner_posts");
    internal_length_offset = (scaled_tray_length - (2*scaled_wall_thickness))/2 - scaled_corner_post_size/2;
    internal_width_offset = (scaled_tray_width - (2*scaled_wall_thickness))/2 - scaled_corner_post_size/2;
    radius = scaled_corner_post_size/2;
    //echo("height", height, "post_size", scaled_corner_post_size)
    translate([internal_length_offset,internal_width_offset,0]) {
        rotate([0,0,0]) {
            make_post(height,radius);
        }   
    }
    translate([internal_length_offset,-internal_width_offset,0]) {
        rotate([0,0,-90]) {
            make_post(height,radius);
        }   
    }
    translate([-internal_length_offset,-internal_width_offset,0]) {
        rotate([0,0,180]) {
            make_post(height,radius);
        }   
    }
    translate([-internal_length_offset,internal_width_offset,0]) {
        rotate([0,0,90]) {
            make_post(height,radius);
        }   
    }

}

module make_tray_cups(height, no_slots=false) {
    echo("Divider Wall Height:", (height*Divider_Wall_Height_Scale/Scale_Units));

    if (Build_Mode == "Square_Cups") {
        make_equal_cup_dividers(height);
    }

    if (Build_Mode == "Storage_Slots") {
        min_per_slot_width = Storage_Slot_Width + Minimum_Storage_Slot_Separation;
        num_slots_float = _internal_tray_length / min_per_slot_width;
        num_slots = floor(num_slots_float);
        tmp_total = min_per_slot_width * num_slots;
        tmp_extra = _internal_tray_length - tmp_total;
        //echo(tmp_total=tmp_total, tmp_extra=tmp_extra);
        extra_per_slot = tmp_extra/num_slots; //Minimum_Storage_Slot_Separation * extra / num_slots;
        //echo(min_per_slot_width=min_per_slot_width, num_slots_float=num_slots_float, num_slots=num_slots);
        slot_separation = Minimum_Storage_Slot_Separation + extra_per_slot;
        num_walls = num_slots;
        //echo(extra_per_slot=extra_per_slot, slot_separation=slot_separation);
        divt = Scale_Units * slot_separation;
        //echo(scaled_divider_thickness=scaled_divider_thickness);
        error = (num_slots) * (slot_separation+Storage_Slot_Width) - _internal_tray_length;
        //echo(error=error);
        echo("Total number of slots", num_slots*Number_Of_Columns);
        make_equal_cups(Number_Of_Columns, height, "length");
        if (no_slots == false) {
            make_slot_walls(num_walls, height, "width", divt=divt);
        }
    }

    if (Build_Mode == "Length_Width_Cups") {
        make_lw_cups(height);
    }

    if (Build_Mode == "Length_Width_Cup_Ratios") {
        make_lw_cup_ratios(height);
    }

    if (Build_Mode == "Custom_Divisions_per_Column_or_Row") {
        make_custom_div_ratios(height);
    }

    if (Build_Mode == "Custom_Ratio_Divisions") {
        make_custom_div(Custom_Division_List, height);
    }

    if (Add_Corner_Posts == true) {
        make_corner_posts(height);
    }
}

module make_finger_slots() {
    if (Make_Finger_Slots == true) {
        radius = scaled_divider_height * Divider_Wall_Height_Scale * Finger_Slot_Radius;
        lift = scaled_divider_height * Divider_Wall_Height_Scale * Finger_Slot_Lift;
        cy_faces = 40;
        union() {
            if (Lengthwise_Finger_Slot == false) {
                separation = Finger_Slot_Width * (((scaled_tray_length - scaled_wall_thickness*2))/2 - radius);
                cut_width = (2*(separation+radius));
                scl = (Finger_Slot_Position - 0.5)*2;
                position = scl * (scaled_tray_length - 2*scaled_wall_thickness - cut_width)/2;
                height = (scaled_tray_width)-(3*scaled_wall_thickness);
                translate ([position, 0, radius + scaled_floor_thickness + lift]) {
                    rotate([90,0,0]) {
                        translate([-separation, 0, 0]) {
                            cylinder(height, r=radius, center=true, $fn=cy_faces);
                            translate([0,scaled_divider_height/2,0]) {
                                cube([radius*2, scaled_divider_height, height], center=true);
                            }
                        }
                        if (separation > 0) {
                            translate([separation, 0, 0]) {
                                cylinder(height, r=radius, center=true, $fn=cy_faces);
                                translate([0,scaled_divider_height/2,0]) {
                                    cube([radius*2, scaled_divider_height, height], center=true);
                                }
                            }
                        }
                    }
                    cube([separation*2, height, radius*2], center=true);
                }
            }
            else {
                separation = Finger_Slot_Width * (((scaled_tray_width - scaled_wall_thickness*2))/2 - radius);
                cut_width = (2*(separation+radius));
                scl = (Finger_Slot_Position - 0.5)*2;
                position = scl * (scaled_tray_width - 2*scaled_wall_thickness - cut_width)/2;
                height = (scaled_tray_length)-(3*scaled_wall_thickness);
                translate ([0, position, radius + scaled_floor_thickness + lift]) {
                    rotate([0,0,90]) {
                        rotate([90,0,0]) {
                            translate([-separation, 0, 0]) {
                                cylinder(height, r=radius, center=true, $fn=cy_faces);
                                translate([0,scaled_divider_height/2,0]) {
                                    cube([radius*2, scaled_divider_height, height], center=true);
                                }
                            }
                            if (separation > 0) {
                                translate([separation, 0, 0]) {
                                    cylinder(height, r=radius, center=true, $fn=cy_faces);
                                    translate([0,scaled_divider_height/2,0]) {
                                        cube([radius*2, scaled_divider_height, height], center=true);
                                    }
                                }
                            }
                        }
                        cube([separation*2, height, radius*2], center=true);
                    }
                }
            }
        }
    }
}

module make_box_top() {
    union() {
        difference() {
            union() {
                make_tray(
                    scaled_box_top_height, 
                    scaled_wall_thickness,
                    is_box_top=true
                );
                if (With_Dividers) {
                    make_tray_cups(scaled_box_top_height, no_slots=true);
                }
            }
            if (with_shell_interlock) {
                make_top_interlock(
                    scaled_box_top_height, 
                    is_box_top=true
                );
            }
        }
    }
}

module make_top_interlock(height, is_box_top = false) {
    make_box_top_shell_interlock(
        height,
        scaled_wall_thickness,
        is_box_top
    );
    if (Create_A_Box_Top && Finger_Detents != "None" && !is_box_top) {
        base_r = 4;
        radius = Detent_Width * base_r * Scale_Units;
        // Using sqrt() makes the fuzzy knob a little more linear in response.
        factor = sqrt(Detent_Height) * radius;
        xlat = (Detent_Orientation == "Length")?(scaled_tray_length/2+radius
        -scaled_wall_thickness/2
        -scaled_interlock_gap/2):0;

        ylat = (Detent_Orientation == "Width")?(scaled_tray_width/2+radius
        -scaled_wall_thickness/2
        -scaled_interlock_gap/2):0;

        c_ht = with_shell_interlock?height-(Box_Top_Interlock_Height*Scale_Units):
            height;

        translate([xlat,ylat,0.001]) {
            //cylinder(h=height-(Box_Top_Interlock_Height*Scale_Units), 0, 3*Scale_Units, $fn=40);
            cylinder(c_ht, factor, radius, $fn=64);
        }
        if (Finger_Detents == "Two") {
            translate([-xlat,-ylat,0.001]) {
                //cylinder(h=height-(Box_Top_Interlock_Height*Scale_Units), 0, 3*Scale_Units, $fn=40);
                cylinder(c_ht, factor, radius, $fn=64);
            }
        }
    }
}

//echo(Build_Mode)
if (Build_Mode == "Just_the_Tray") {
    difference() {
        union() {
            make_tray(scaled_tray_height, scaled_wall_thickness);
            if (Add_Corner_Posts == true) {
                echo("scaled_divider_height",scaled_divider_height)
                make_corner_posts(scaled_divider_height);
            }
        }
        make_top_interlock(scaled_tray_height);
    }
}
else if (Build_Mode == "Tray_Lid") {
    make_lid();
}
else {
    difference() {
        union() {
            make_tray(scaled_tray_height, scaled_wall_thickness);
            make_tray_cups(scaled_divider_height);
        }
        make_finger_slots();
        make_top_interlock(scaled_tray_height);
    }
}

if (Build_Mode != "Tray_Lid" && Create_A_Lid == true) {
    // Move the lid so that it lay just separated from the main tray.
    translate([0, (scaled_tray_width + 8), 0]) {
        make_lid();
    }
}

if (Create_A_Box_Top == true) {
    // Move the box top so that it lay just separated from the main tray.
    echo("Internal Box Height:", _internal_tray_heigth + _internal_box_height);
    translate([0, -(scaled_tray_width + 8), 0]) {
        make_box_top();
    }
}



