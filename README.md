# A Generator for 3D Printable Organizer Trays

What if you could generate a vast library of organizing trays all designed to work together. Now you can!

## Description

You are a maker. You have, or are building, a vast inventory of tools and small parts. You would really like to keep all of this stuff sorted and organized. Maybe you have an existing storage cabinet with drawers, or maybe you are building one of those too. What you need for those drawers are organizer trays tailor made for specific items.

This tool, which I call Tray Generator (because I cannot think of a better name right now) might be just what you need. Tray Generator can be used to build a large library of trays, trays that are all designed to work together. They will fill grids nicely. They will stack nicely. You can even print lids. 

The general intent is that you can build a large library of compatible trays and then print what you need, when you need it. By creating this library once, you'll ensure that your future tray needs are fully compatible with your existing trays. (And, with careful planning, you will be able to add new custom, and compatible, trays in the future.)

There are two primary scripts:

  - tray_generator.scad
  - make_trays.py

The tray_generator.scad file is a stand-alone OpenSCAD program file. You can run the OpenSCAD GUI and load this script and use the Customizer to design individual trays. There is a lot of flexibility provided through the customizer (as you'll see later). And using OpenSCAD this way is a great way to design custom tray layouts to add to your library.

The make_trays.py script is a command line front-end to OpenSCAD and the tray_generator.scad script. Using make_trays.py lets you create and maintain libraries of trays defined in yaml configuration files. It also has a command line interface to quickly generate trays on demand.

It is best to get familiar with tray_generator.scad before using make_trays.py.

### Dependencies

* [OpenSCAD](https://openscad.org/) (source on [github](https://github.com/openscad/openscad)
* [Python 3.8+](https://www.python.org/)
* [Optional] A slicer with a CLI (I use PrusaSlicer)

Download and install the latest version of OpenSCAD. It is recommend that you add the OpenSCAD folder to
your path. If you don't, you'll need to tell Tray Generator where to find the executable using the --oscad 
command line parameter or in a yaml config file.

You probably already have python 3.8+. If not, get it from [python.org](python.org)
```
> python --version
Python 3.8.7  (or greater, or may lower, but I've only used 3.8, and now 3.9)
```

Tray Generator also depends on a few python libraries, and it is recommended that you setup a venv and install those libraries into the virtual environment (see requirements.txt). I'm still new to this whole python eco-system so it is probably best to seek guidance on this part elsewhere.

If you have a 3D printer, you probably have a slicer, and that slicer probably has a command line interface.
Tray Generator can, optionally, automatically slice the tray models that you create. To make this work
you need to modify slice.bat/slice.sh to properly invoke your slicer of choice. I use PrusaSlicer, so
these files are already setup to work with it, though you might need to specify the path or put your slicer 
on your path. Take a look at the slice.bat file and adapt it to your slicer of choice.

### Installing

Simple! Once you have the dependencies installed, you only need to clone this repo to your system.
```
> git clone https://github.com/mgfarmer/openscad_tray_generator.git
```
----
# Getting Started with tray_generator.scad

This section contains more detailed information about the construction parameters 
exposed in the scad script. OpenSCAD limits the amount of explanatory text that one
can provide in the UI, so this is where I can write as much as I want about each 
parameter.

Before I get started on all the parameters it might be helpful for you to start 
OpenSCAD and load the script so you can follow along and play with each parameter
as you are reading about them.

When you first load the script you will be presented with a generic boring 4 inch x 
8 inch x 1 inch high tray. If that is what you need, great!  You can render, export
and print it. 

If you are brand new to OpenSCAD then these are the steps to render and export your
tray:

  - Press F6 to render the tray (pressing F5 to preview doesn't count as rendering)
  - File -> Export -> Export as 3MF... 

I recommend 3MF as I've had some issues with STLs created by OpenSCAD. 3MF hasn't 
failed me ever (so far...)

The basic flow goes like this:

  - Select your scale units
  - Specify your tray dimensions
  - Specify a "Build Mode"
  - Customize you chosen "Build Mode"
  - Perform further customizations as needed

## Tray Dimensions and Mode

In this section of the customizer you specify the units, dimensions, and "divider wall"
construction mode. Let us go over each parameter:
### Parameter: Scale Units

tray_generator works just as well in "inch" mode or "cm" mode so you don't have to 
do any mental math. You can work in either system. In fact, you can add additional 
systems easily to the script if you want to use something else.

Once you select a unit, all other parameters that express some kind of dimension are
expressed using the chosen unit scale. If you want an 8x81 inch tray, select "inch"
than set the length, width, and height to 8, 4, and 1. If you want a 20x10x3 cm tray, 
select "cm", and specify 20, 10, and 3 for the length, width, and height. Easy.

### Parameter: Dimensions Are External

This checkbox specifies whether the overall tray dimensions represent the internal or 
external dimension of the final tray. If you are building a library of trays that
will all live together cooperatively in a storage system drawer you probably want to 
stick with "external" dimensions. 

Using "internal" dimensions is very useful when building trays to hold specific
objects, or classes of objects, when you want internal compartments to be a specific
size. (See the Storage Slots build mode for good examples.)

### Parameter: Tray Length

Pretty self-explanatory!  Specifies the internal or external dimension of the "length"
of the tray. The "length" and "width" are just names to give to the two primary 
dimensions. The "length" does not have to be equal to or greater than the "width". 
You can build a tray 2 units long by 10 units wide.

### Parameter: Tray Width

Specifies the internal or external dimension of the "length" of the tray. 

Important: This parameter, unlike, length, has some special considerations when using 
"internal" dimensions and using the "Storage Slots" build mode. This is explained
later in the "Storage Slot" section. The gist of it, though, it when you divide
a storage slot tray into multiple columns, the column divider width is compensated
for when computing the overall internal dimension. So, for example, if you need
3 2-inch wide columns in your storage slot tray, then you can specify the tray 
width as 6 inches. The constructed tray will then have 3 2-inch columns. You do
not need to adjust for the column divider wall thickness.

At this time, in all other build modes, you do need to manually compensate for
divider wall thickness if you need specific sized cells in the tray.

### Parameter: Tray Height

Specifies the internal or external dimension of the "height" of the tray. 

When building "interlocking" stacking trays, the tray will have an extrusion
below the "bottom" of the tray. This extrusion sits recessed into a similar
tray below it. It is, therefore, not considered part of the height of the 
tray. So the overall physical height of the tray will be the height specified
here plus the interlock extrusion height (covered later).

### Parameter: Build Mode

The Build Mode declares how you want to create divider walls in your tray. 
There are several! They are listed in order of increasing complexity (and flexability).

| Build Mode                         | Summary                                                                               |
| ---------------------------------- | ------------------------------------------------------------------------------------- |
| Just the Tray                      | Simple, build a tray with no dividers!                                                |
| Square Cups                        | Builds a tray with specified size square dividers that fit evenly in the tray         |
| Length Width Cups                  | Build with x equal dividers on the length and y equal dividers on the width           |
| Length Width Cup Ratios            | Build with x un-equal dividers on the length and y un-equal dividers on the width     |
| Storage Slots                      | Build a tray with storage slots (think photo slides, coin boxes, microscope slides)   |
| Custom Divisions per Column or Row | Build a tray with C rows/columns, with varied dividers in each row/column             |
| Custom Ratio Divisions             | Build a tray with completely custom placed divider walls, anywhere in the tray        |
| Tray Lid                           | Special mode to build just tray lids (if you already have a tray and just need a lid) |

Once you select a Build Mode, then you can use the next several parameter 
sections (each named after a specific Build Mode) to specify parameters that control 
the build. 

Note that for "Just the Tray" there is not a section to configure this mode as 
there are no options. You are are just getting a tray with no divider walls.

## Build Mode: Square Cups
This mode lets you build a tray with internal square cups. You can specify the size
of the cups, but the specified size must be equally divisible into both the length 
and width of the tray. For instance, with an 8x4 tray you can use 1, 2, or 4 sized
cups because all of those divide equally into both 4 and 8. You can also specify 
sizes less than 1, like 0.5, or 0.25 if you need really tiny cups. If you set a 
value that does not divide even the preview will not contain any dividers.

### Parameter: Square Cup Size
Specifies the size, in units, for the square cups.

## Build Mode: Length Width Cups
This mode lets you build equally spaced dividers in both length and width. You can 
specify different numbers of dividers for length and width. This allows for creating 
many equal sized rectangular storage cups. For instance, you can build a tray with 
2 dividers across the width (creating 3 rows), and 5 dividers (6 columns) down the length, 
resulting in 18 rectangular storage cups (for your rare gem collection!).

### Parameter: Cups Along Length
Specifies the number of equal sized storage divisions along the length of the tray.

### Parameter: Cups Across Width
Specifies the number of equal sized storage divisions across the width of the tray.

## Build Mode: Length Width Cup Ratios
The previous build modes are quite simple. Now we start getting into the more
complex modes that offer greater flexibility in how the dividers can by configured.

This mode is similar to the previous mode (and, in fact, can be configured to behave 
exactly the same, if you wanted to). But in this mode you can control the spacing
between the dividers in both directions, creating different sized storage cups. 

The method for specifying the spacing between dividers is done in a dimension independent
way. This way, if you change the dimension of the tray the relationship of the spacing 
between dividers is preserved and scaled accurately.  This is accomplished by using 
"ratios" to specify the relative size of each storage division across the length and width 
of the tray.  This "ratios" concept it used in other more complex configurations as well.

Ratios are expressed as a vector of ratio values (a list of numbers), like this:

```
[1, 1, 1, 1, 1]
```

That expression says "create 5 storage divisions, and make them all the same size".  
(This is equivalent to the previous build mode.)  The reason they are called ratios is that
the sum of all the numbers represents a unit-less total dimension (in this example, it is 5), 
while the count (i.e. length) of the vector represent the number of divisions. The relative 
size of each division is determine by (division size/total size) for each element in the 
vector.  In this case it is always 1/1 so all division will be equal sized.

Where-as this one...

```
[1, 1, 2, 1, 1]
```

...says "create 5 storage divisions, and make the middle one twice as large as the others 
(which will all be the same size). In this case the total size is 6.  Each of the "1" divisions
will be (1/6) of the total space, while the "2" division will be (2/6) or (1/3) of the 
total space.

And...

```
[2, 3, 2]
```

...creates 3 division, where the middle one is 1-1/2 (i.e. 3/2) times as wide as the 
two side ones.

You are not limited to integer values either.

### Parameter: Lengthwise Cup Ratios
Specify the vector of ratios use to create divisions along the length of the tray.

### Parameter: Widthwise Cup Ratios
Specify the vector of ratios use to create divisions across the width of the tray.

## Build Mode: Storage Slots

## Build Mode: Custom Divisions per Column or Row

## Build Mode: Custom Ratio Divisions

## Outer Wall Parameters
## Divider Wall Parameters
## Divider Wall Finger Slots
## Tray Insert Parameters
## Lid Parameters
## Box Top Parameters
## Interlocking Parameters

----
# Getting Started with make_trays.py

First cd to the folder where you cloned the repo.

Basic invocation starts with 
  
```
> python .\make_trays.py
You need to specify an output folder (-o <folder>) so I know where to put everything.
```
That will do nothing but print some information to help you get started. So try:
```
> python .\make_trays.py -o mytrays
You need to specify dimensions of the tray(s) you want to create using
--dimension/--heights, or --lengths, --widths, and --height.
For instance, try "--dimension 8x4x1"
Use "-h" to get more help
```
This tells Tray Generator to place all generated objects in to a subfolder called "mytrays".
But nothing is generated yet because you haven't told Tray Generator what size trays you want to create.
So, try this next:

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1
This is what is going to happen:
Number of objects declared:         2
Number of objects to be gen/sliced: 2, 0
Number of objects existing:         0

You can disable this prompt with "--doit"
Are you ready to do this? [Y/n]:
```
Finally, something good is going to happen. You can see that two trays are going to be created. Each tray will be the dimensions you specified on the command line. By the way, the default unit scale is inches, but Tray Generator works just as well with metric by specifying "-u/--units cm" on the command line (or in global_config.yaml). All dimensions expressed in the command line parameters are expressed using the chosen unit scale.

So before Tray Generator does anything, it will ask you if you're ready to proceed. This is done, by
default, because Tray Generator is capable of generating 1000's of trays in a single invocation, and 
that can take many hours to complete (of course you can always abort, but still...)

You can also specify "-d/--dryrun" on the command line and Tray Generator will just print out a list
operations that will execute to generate the trays. This is a great way of seeing what is going to happen.

Go ahead and type "n" to cancel the process, then add the -d parameter:

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -d
Generating: (1 of 2):
     Rendering: mytrays/4-in-long/4-in-wide/1-in-high/tray_4x4x1.3mf
Generating: (2 of 2):
     Rendering: mytrays/6-in-long/4-in-wide/1-in-high/tray_6x4x1.3mf

Summary:
Number of objects declared:         2
Number of objects to be gen/sliced: 2, 0
Number of objects existing:         0
```
Now you can see more details about the two trays that are going to be generated, including where the
files will be located. By default, Tray Generator will organize the trays into subfolders organized first
by length, then by width, then by height. If you are creating a large library of trays this will make
it much easier to find the tray you want to print in the future. You can, however, use the "--flat"
command line option to have all generate files placed in the top level of the output folder. Try it:

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -d
Generating: (1 of 2):
     Rendering: mytrays/tray_4x4x1.png mytrays/tray_4x4x1.3mf
Generating: (2 of 2):
     Rendering: mytrays/tray_6x4x1.png mytrays/tray_6x4x1.3mf

Summary:
Number of objects declared:         2
Number of objects to be gen/sliced: 2, 0
Number of objects existing:         0
```
See how the file location changed.

Finally, lets create these two trays:

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 --flat --doit
Generating: (1 of 2):
     Rendering: mytrays/tray_4x4x1.png mytrays/tray_4x4x1.3mf
Generating: (2 of 2):
     Rendering: mytrays/tray_6x4x1.png mytrays/tray_6x4x1.3mf

Summary:
Number of objects declared:         2
Number of objects to be gen/sliced: 0, 0
Number of objects existing:         2
```
That's it. Take a look at what you just created:
```
❯ ls mytrays

    Directory: C:\Users\kevin\git\tray_generator\mytrays

Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          10/28/2021  9:10 PM           4445 tray_4x4x1.3mf
-a---          10/28/2021  9:10 PM           7792 tray_4x4x1.png
-a---          10/28/2021  9:10 PM           4440 tray_6x4x1.3mf
-a---          10/28/2021  9:10 PM           7122 tray_6x4x1.png
```
You can see that we have one png file and one 3mf file for each tray we just generated. Since tray generation can be quite slow (OpenSCAD is not fast) you can also specify "-p/--preview_only" on the command line and only generate the png preview files (which is much faster than generating 3mf files). This is fairly fast and is a great way to see what your library will look like before committing to the full model generation. Use your favorite file browser/image viewer to check out the png file previews.

Tray Generator generates 3mf model files by default. You can specify STL, but be aware that at this time OpenSCAD generates STL files with many errors that some slicers don't even notice. (When I started this I was using STL files because that's what I always used. I loaded the STL into my slicer and it looked fine, but when I printed it, some walls were just plain missing. I was baffled. Finally, after looking at the layers view I saw that the wall was missing in there, but not in the preview. Googling revealed the known issues exporting STLs from OpenSCAD, and more googling revealed that 3mf was superior format. I tried it. It worked. The model still has errors, but PrusaSlicer detects and repairs them automatically.

Anyway, if you want STL files (or any other format that OpenSCAD exports to), use the "-e/-export_model_as" command line parameter;

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -e STL
```

Don't do that, it is just an example.

Now, try the same command we used earlier to generate the two trays:
```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 --flat --doit
All your work is already done!
Use --regen and/or --reslice if you need to.
Number of objects declared:         2
Number of objects to be gen/sliced: 0, 0
Number of objects existing:         2
```
Tray Generator will not generate models if they already exist in the output folder. This both saves time
and allows you to add to the library by adding new dimensions. Only the new trays will get generated. Try this:

```
> python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 2x4x1 --flat --doit
Generating: (1 of 1):
     Rendering: mytrays/tray_2x4x1.png mytrays/tray_2x4x1.3mf

Summary:
Number of objects declared:         3
Number of objects to be gen/sliced: 1, 0
Number of objects existing:         2
```
Only the one new tray was generated. Now, if you really want to regenerate all the trays, you can do that using
the "--regen" command line parameter (or completely delete the mytrays folder). Go ahead and try it (it is just 3 
tray...you have time).

Now try this:

```
python .\make_trays.py -o mytrays --dimensions 8x4
Accumulating work units...
When using 'dimensions' with LxW expressions, you must also provide heights using 'heights', or use LxWxH expressions
```

Notice that the --dimensions parameter only specified the length and width of the tray, and not the height. Then take note of the message printed. Using using just LxW dimensions like this allows you to create several trays of different heights by providing a list of heights instead of calling out the LxWxH specification for each tray. Add the --heights parameter:

```
python .\make_trays.py -o mytrays --dimensions 8x4 --heights 0.5 0.75 1 1.25 1.5 2

Accumulating work units...
This is what is going to happen:
Number of objects declared:         6
Number of objects existing:         0
Number of objects to be gen/sliced: 6, 0

You can disable this prompt with "--doit"
Are you ready to do this?
```
Now you are getting six trays of different heights. These trays are all stackable, using a small extrusion on the bottom of the tray that sits into the tray below it so they won't slide around.


There is so much more...

The --dimension parameter is primarily aimed at creating small batches of trays. If you want to create a larger library of trays, there are betters ways forward. Try this:

```
python .\make_trays.py -o tmp --lengths 2 4 6 8 --widths 2 4 6 8 --heights 0.5 0.75 1 1.25 1.5 2
Accumulating work units...
This is what is going to happen:
Number of objects declared:         60
Number of objects existing:         0
Number of objects to be gen/sliced: 60, 0

You can disable this prompt with "--doit"
Are you ready to do this? [Y/n]:
```

Whoa! That's going to create 60 trays. When using the --length, --widths, and --heights command line parameters you can create a lot of trays fast. The astute observer might notice that 4x4x6=96 trays, but only 60 are counted. Tray Generator is barely smart enough to know that a 2x4 and a 4x2 tray are identical. So duplicates like this are not created. That's why there are 60 and not 96.

But we're just getting started. Let's take it to the next level (level 2?). Try this:

```
python .\make_trays.py -o tmp --lengths 2 4 6 8 --widths 2 4 6 8 --heights 0.5 0.75 1 1.25 1.5 2 --make_square_cups
Accumulating work units...
This is what is going to happen:
Number of objects declared:         150
Number of objects existing:         0
Number of objects to be gen/sliced: 150, 0

You can disable this prompt with "--doit"
Are you ready to do this? [Y/n]:
```

Now we're cooking. 150 trays! Certainly you would not need this many options (oh, but you do, and more...). The "--make_square_cups" option will generate trays with square sized storage dividers in the trays. Trays are generated for each square size that will fit in a given tray dimension. For instance, if you have a 8x4 tray, you'll get storage cups with dimensions of 1, 2, and 4 units because those dimensions are all integer divisors of 8 and 4. On the other hand, if you make an 8x3 tray this way you will only get 1 unit cups because no other unit size divides evenly into 8 and 3.

Time to level up! Try this:

```
python .\make_trays.py -o tmp --lengths 2 4 6 8 --widths 2 4 6 8 --heights 0.5 0.75 1 1.25 1.5 2 --make_square_cups --make_divisions
Accumulating work units...
This is what is going to happen:
Number of objects declared:         1206
Number of objects existing:         0
Number of objects to be gen/sliced: 1206, 0

You can disable this prompt with "--doit"
Are you ready to do this? [Y/n]:
```

BAM!  1206 trays. That is a lot of trays... You know you may need them at some point. The "--make_divisions" options generates trays with integral divisions in length, width, and length+width combinations, for all heights. It is probably easier to visualize this then to explain it in text, so try (a smaller combination):

```
python .\make_trays.py -o tmp --lengths 4 --widths 2 4 --heights 1 --make_divisions --preview --doit
Accumulating work units...
Summary:
Number of objects declared:         12
Number of objects existing:         0
Number of objects to be gen/sliced: 12, 0
```
This will generate 4x2 and 4x4 trays, and yet, there are still 12 variants!

Then take a look at the generated preview images to get a clear picture of what is happening. You'll see that each tray size has variants with divisions that fit the tray down to 1" (or 3cm). 

You may never need all these trays, but you may need several of them, and with this tool, you'll have every variant available to choose from when the need arises. And, since you generated them all up front, using the same parameters, you know they will all be compatible, and fit nicely together in your storage solution.

But there is more. So much more!

To be continued.....

## Printing Your Trays

This is mostly up to you. You know your printer and how to make it print well (hopefully). But I very
highly recommend printing with supports if you are printing stackable trays. Stackable
trays have a recessed edge at the bottom with a 90 degree corner. If you don't print
with supports, your edged will sag and the trays will not stack nicely.
## Authors & Contributors

Contributors names and contact info

* just me, so far...

## Version History

No official releases, yet. Things are changing very quickly....

## License

This project is licensed under GPL v2 License - see the LICENSE.md file for details

