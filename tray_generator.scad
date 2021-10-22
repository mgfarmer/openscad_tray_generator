// Specifies the base unit that you want to use for your trays
scale = 25.4; // [25.4:inch, 10.0:cm, 1.0:mm]

// Specifies the tray length in the select unit scale
tray_length = 8.0; // [1.0:1.0:10.0]

// Specifies the tray width in the select unit scale
tray_width = 2.0; // [1.0:1.0:10]

// Specifies the tray height in the select unit scale
tray_height = 1.0; // [0.5:0.5:5]

// Select a cup generating mode, then use the controls in the same named tabs to specify generation parameters
cup_mode = "Square Cups"; // ["Square Cups", "Length/Width Cups", "Length/Width Cup Ratios", "Custom Ratio Divisions"]

/* [Square Cups] */
// If not 0, specifies the size of square cups to be create, both tray_length and tray_width should be a multiple of this value.  If your tray is 8x4 and you use a cup size of 1 you will get 32 cups. 
square_cup_size = 1; //[1.0:1.0:10]

/* [Length/Width Cups] */
// This create the specified number of equal length cups along the length of the tray.
cups_along_length = 1; //[1.0:1.0:10]

// This create the specified number of equal width cups acrossthe width of the tray.
cups_across_width = 1; //[1.0:1.0:10]

/* [Length/Width Cup Ratios] */
// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal length divisions, and [1,1,2] makes 2 equal length small divisions and one division that is twice as long.
cup_ratios_length = [1,1,1,1,1];

// This creates cup dividers at the given ratios.  For instance [1,1] makes two equal width divisions, and [1,1,2] makes 2 equal width small divisions and one divisions that is twice as wide.
cup_ratios_width = [1,1,1,1,1];

/* [Custom Ratio Divisions] */
// It is strongly advised that you build this expression in a real text editor, then paste it here.
custom_divs = [[ "-", 0.5, [0.25, 0.75]], [ "|", 0.5, [0.25, 0.75]]];
//[[ "-", 0.66, [0.0, 0.66]],[ "|", 0.66, [0.66, 1.0]]];

/* [Wall Thickness Parameters] */
// Specifies how thick the outer wall of the tray will be
wall_thickness = 0.071;

// Specifies how thick the floor will be.
floor_thickness = 0.071;

// Specifies how thick each internal cup divider will be.
divider_thickness = 0.071;

// Specifies the ratio of the corner radius to the wall thickness. Set to 0 for square corners. Set to one for the most rounding.
corner_radius_ratio = 0.5;

/* [Interlocking Parameters] */
// Specifies the height of the interlock panel extruded below the tray (and also the distance that the top of the dividers are below the upper tray edge. Specify 0 for non-interlocking stackers. You can still stack them, they just won't interlock.).
interlock_height = 0.1;

// Specifies the gap between the interlock extrusion and the inner face of the outer wall of the tray. Largers values will give a looser fit.
interlock_gap = 0.003;




length = scale * tray_length;
width = scale * tray_width;
height = scale * tray_height;
thickness = scale * wall_thickness;
f_thick = scale * floor_thickness;
d_thick = scale * divider_thickness;
c_radius = scale * corner_radius_ratio * wall_thickness; 
igap = scale * interlock_gap;
iheight = scale * interlock_height;

function add(v, i = 0, r = 0) = i < len(v) ? add(v, i + 1, r + v[i]) : r;

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


module make_l_div(pos, from=0, to=1.0, hscale=1.0) {
    // pos is a normalized position, from 0.0 to 1.0
    wid = width-(d_thick);
    wpos = (wid*pos) - (wid/2);
    lstart = (length*from) - (length/2);
    lend = (length*to) - (length/2);
    llen = (to-from) * length; // + (d_thick/2);
    hdiv = (height-iheight) * hscale;
    translate([lstart+(llen/2),wpos,hdiv/2]) {
        union() {
            cube([llen,d_thick,hdiv], center=true);
            if (from > 0.0) {
                translate([lstart,0,0]) {
                    cylinder(hdiv, r=d_thick/2, center=true, $fn=20);
                }
            }

            if (to < 1.0) {
                translate([lend,0,0]) {
                    cylinder(hdiv, r=d_thick/2, center=true, $fn=20);
                }
            }
        }
    }
}

module make_w_div(pos, from=0, to=1.0, hscale=1.0) {
    // pos is a normalized position, from 0.0 to 1.0
    llen = length-d_thick;
    lpos = (llen*pos) - (llen/2);
    wstart = (width*from) - (width/2);
    wend = (width*to) - (width/2);
    wlen = (to-from) * width;
    hdiv = (height-iheight) * hscale;
    translate([lpos,wstart+(wlen/2),hdiv/2]) {
        union() {
            cube([d_thick,wlen, hdiv], center=true);
            cylinder(hdiv, r=d_thick/2, center=true, $fn=20);
            if (from > 0.0) {
                translate([0,wstart,0]) {
                    cylinder(hdiv, r=d_thick/2, center=true, $fn=20);
                }
            }

            if (to < 1.0) {
                translate([0,wend,0]) {
                    cylinder(hdiv, r=d_thick/2, center=true, $fn=20);
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

module make_tray() {
    translate([0,0,height/2]) {
        difference() {
            // Main outer shell
            mkshell(length, width, height, thickness, c_radius); 
            translate([0,0,f_thick]) {
                // Subtract inner space..
                mkshell(length, width, height, 
                    thickness, c_radius, thickness*2);
            }
        };
    };
    if (iheight > 0) {
        translate([0,0, -iheight/2+0.001]) {
            mkshell(length, width, iheight, 
            thickness, c_radius, thickness*2, igap);
        }
    }
}

module make_dividers(divs, orient="length") {
    // divs is a normalized array of 
    // positions for each divider to create.
    for ( i = divs ){
        make_div(orient, i);
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
        //make_equal_cups(2, "length");
        make_cups([1, 1, 2]);
        make_cups([1, 1, 2],"width");
        //make_equal_cups(4, "width");
        //make_dividers([0.25, 0.5, 0.75], "length");
    }
}

module make_cups(ratios, orient="length") {
    total = add(ratios);
    mult = 1.0/total;
    divs = [ for(i=ratios) (i*mult) ];
    divs2 = [ for(i=[len(divs)-1:-1:1]) add(divs, i, 0)];
    make_dividers(divs2, orient);
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

if (cup_mode == "Custom Ratio Divisions") {
    union() {
        make_tray();
        for ( div = custom_divs ) {
            if (len(div) == 3) {
                pos = div[1];
                from = div[2][0];
                to = div[2][1];
                dir = div[0];
                make_div(dir, pos, from, to);
            }
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

