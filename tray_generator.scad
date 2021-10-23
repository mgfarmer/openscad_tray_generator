// Specifies the measurement system and scale you want to use for your trays.  All dimensions below will be in these units.  There are presets called "imperal defaults" and "metric defaults" that make good starting points. 
scale = 25.4; // [25.4:inch, 10.0:cm]

// Specifies the tray length in the select unit scale
tray_length = 4.0; // [1.0:1.0:10.0]

// Specifies the tray width in the select unit scale
tray_width = 2.0; // [1.0:1.0:10]

// Specifies the tray height in the select unit scale
tray_height = 1.0; // [0.0:0.25:8]

// Select a cup generating mode, then use the controls in the same named tabs to specify generation parameters
cup_mode = "Square Cups"; // ["Square Cups", "Length/Width Cups", "Length/Width Cup Ratios", "Custom Divisions per Column or Row", "Custom Ratio Divisions", "Tray Lid"]

/* [Square Cups] */
// If not 0, specifies the size of square cups to be create, both tray_length and tray_width should be a multiple of this value.  If your tray is 8x4 and you use a cup size of 1 you will get 32 cups. 
square_cup_size = 1; //[1.0:0.5:10]

/* [Length/Width Cups] */
// This create the specified number of equal length cups along the length of the tray.
cups_along_length = 1; //[1.0:1.0:10]

// This create the specified number of equal width cups across the width of the tray.
cups_across_width = 1; //[1.0:1.0:10]

/* [Length/Width Cup Ratios] */
// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal length divisions, and [1,1,2] makes 2 equal length small divisions and one division that is twice as long.
cup_ratios_length = [1,1,1,1,1];

// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal width divisions, and [1,1,2] makes 2 equal width small divisions and one divisions that is twice as wide.
cup_ratios_width = [1,1,1,1,1];

/* [Custom Divisions per Column or Row] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
custom_colrow_divs = [ "|", 3, 1, 2, 1, "-", 3, 1, 1, 1, "-", 2, 1, 2, "-", 1];

// ["|", 5, "*", 3, "*", 3, "*", 3, "*", 2, "*", 5 ]

/* [Custom Ratio Divisions] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
custom_divs = [ [ "-", 0.5, [0.25, 0.75] ], [ "|", 0.5, [0.25, 0.75] ] ];
//[[ "-", 0.66, [0.0, 0.66]],[ "|", 0.66, [0.66, 1.0]]];

/* [Wall Thickness Parameters] */
// Specifies how thick the outer wall of the tray will be
wall_thickness = 0.07; // [0.05:0.01:0.50]

// Specifies how thick the floor will be.
floor_thickness = 0.07; // [0.05:0.01:0.50]

// Specifies how thick each internal cup divider will be.
divider_thickness = 0.07; // [0.05:0.01:0.50]

// Specifies the ratio of the corner radius to the wall thickness. Set to 0 for square corners. Set to one for the most rounding.
scaled_corner_radius_ratio = 0.5;

/* [Interlocking Parameters] */
// Specifies the height of the interlock panel extruded below the tray (and also the distance that the top of the dividers are below the upper tray edge. Specify 0 for non-interlocking stackers. You can still stack them, they just won't interlock.).
interlock_height = 0.1; // [0.0:0.01:0.25]

// Specifies the gap between the interlock extrusion and the inner face of the outer wall of the tray. Largers values will give a looser fit.
interlock_gap = 0.003;  // [0.0:0.001:0.020]

// Create scaled versions of all user paramters
scaled_tray_length = scale * tray_length;
scaled_tray_width = scale * tray_width;
scaled_tray_height = scale * tray_height;
scaled_wall_thickness = scale * wall_thickness;
scaled_floor_thickness = scale * floor_thickness;
scaled_divider_thickness = scale * divider_thickness;
scaled_corner_radius = scale * scaled_corner_radius_ratio * wall_thickness; 
scaled_interlock_gap = scale * interlock_gap;
scaled_interlock_height = scale * interlock_height;

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
    echo(from, to);
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
    echo(from, to);
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
    union() {
        translate([0,0,scaled_floor_thickness/2]) {
            mkshell(scaled_tray_length, scaled_tray_width, scaled_floor_thickness, scaled_wall_thickness, scaled_corner_radius); 
        };
        if (scaled_interlock_height > 0) {
            translate([0,0, -scaled_interlock_height/2+0.001]) {
                mkshell(scaled_tray_length, scaled_tray_width, scaled_interlock_height, 
                scaled_wall_thickness, scaled_corner_radius, scaled_wall_thickness*2, scaled_interlock_gap);
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


if (cup_mode == "Square Cups") {
    lcups = tray_length/square_cup_size;
    wcups = tray_width/square_cup_size;
    union() {
        make_tray();
        make_equal_cups(lcups, "width");
        make_equal_cups(wcups, "length");
    }
}

if (cup_mode == "Length/Width Cups") {
    union() {
        make_tray();
        if (cups_along_length > 0) {
            make_equal_cups(cups_along_length, "width");
        }
        if (cups_across_width > 0) {
            make_equal_cups(cups_across_width, "length");
        }
    }
}

if (cup_mode == "Length/Width Cup Ratios") {
    union() {
        make_tray();
        if (cups_along_length > 0) {
            make_cups(cup_ratios_length, "width");
            //make_cups([1,2,1,2,1], "width");
        }
        if (cups_across_width > 0) {
            make_cups(cup_ratios_width, "length");
        }
    }
}

function sub_vect(vect, start) = [for( i = [start : 1 : len(vect)-1]) vect[i] ];

module make_walls(section, mode, walls, divisions) {
    if (section < len(divisions)-1) {
        from = divisions[section];
        to = divisions[section+1];
        //echo(section, from, to);
        //echo(walls);
        if (is_num(walls[2])) {
            ratios = [ for( i = [1 : 1 : walls[1]]) walls[1+i] ];
            //echo(ratios);
            make_cups(ratios, mode, from, to);
            // divisions = concat( [0.0], make_normalized_divs(ratios), [1.0]);
            // start = 2 + divs;
            wall_specs = sub_vect(walls, 2 + walls[1]); 
            //echo(wall_specs);
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

if (cup_mode == "Custom Divisions per Column or Row") {
    union() {
        make_tray();
        mode = custom_colrow_divs[0];
        other_mode = (mode == "|")?"-":"|";
        divs = custom_colrow_divs[1];
        if (is_num(custom_colrow_divs[2])) {
            ratios = [ for( i = [0 : 1 : divs-1]) custom_colrow_divs[2+i] ];
            make_cups(ratios, mode);
            divisions = concat( [0.0], make_normalized_divs(ratios), [1.0]);
            start = 2 + divs;
            wall_specs = sub_vect(custom_colrow_divs, start);
            make_walls(0, other_mode, wall_specs, divisions);
        }
        else {
            make_equal_cups(divs, mode);
            divisions = concat( [0.0], make_normalized_divs([ for( i = [0 : 1 : divs-1]) 1 ]), [1.0]);
            wall_specs = sub_vect(custom_colrow_divs, 2);
            make_walls(0, other_mode, wall_specs, divisions);
        }
    }
}

if (cup_mode == "Custom Ratio Divisions") {
    union() {
        make_tray();
        for ( div = custom_divs ) {
            // vectors with 3 elements use full height divisions.
            if (len(div) == 3) {
                pos = div[1];
                from = div[2][0];
                to = div[2][1];
                dir = div[0];
                make_div(dir, pos, from, to);
            }
            // vectors with 4 elements can scale the height of the division.
            if (len(div) == 4) {
                pos = div[1];
                from = div[3][0];
                to = div[3][1];
                dir = div[0];
                hscale = div[2];
                make_div(dir, pos, from, to, hscale);
            }
        }
    }
}

if (cup_mode == "Tray Lid") {
    make_lid();
}
