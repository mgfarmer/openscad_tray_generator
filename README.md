# A Generator for 3D Printable Organizer Trays

What if you could generate a vast library of organizing trays all designed to work together. Now you can!

## Description

You are a maker.  You have, or are building, a vast inventory of tools and small parts.  You would really like to 
keep all of this stuff sorted and organized. Maybe you have an existing storage cabinet with drawers, or maybe 
you are building one of those too.  What you need for those drawers are organizer trays tailor made for specific items.

This tool, which I call Tray Generator (because I cannot think of a better name right now) might be just what you 
need. Tray Generator can be used to build a large library of trays, trays that are all designed to work together.
They will fill grids nicely.  They will stack nicely.  You can even print lids.  

The general intent is that you can build a large library of compatible trays and then print what you need, when you 
need it.  By creating this library once, you'll ensure that your future tray needs are fully compatible with your 
existing trays.  (And, with careful planning, youi'll be able to add new custom, and compatible, trays in the 
future.)

## Getting Started

### Dependencies

* [OpenSCAD](https://openscad.org/) (source on [github](https://github.com/openscad/openscad)
* [Python 3.8+](https://www.python.org/)
* [Optional] A slicer with a CLI (I use PrusaSlicer)

Download and install the latest version of OpenSCAD.  It is recommend that you add the OpenSCAD folder to
your path.  If you don't, you'll need to tell Tray Generator where to find the executable using the --oscad 
command line parameter (or you could just edit the source and hard code the full path).

You probably already have python 3.8+.  If not, get it from [pyhton.org](python.org)

If you have a 3D printer, you probably have a slicer, and that slicer probably has a command line interface.
Tray Generator can, optionally, automatically slice the tray models that you create.  To make this work
you need to modify slice.bat/slice.sh to properly invoke your slicer of choice.  I use PrusaSlicer, so
these files are already setup to work with it, though you might need to specify the path or put your slicer 
on your path

### Installing

Simple! You only need to clone this repo to your system.
```
> git clone https://github.com/mgfarmer/openscad_tray_generator.git
```

## Help

You can get usage information via:
```
python tray_generator.py -h
```
## Getting Started

First cd to the folder where you cloned the repo.

Basic invocation starts with 
  
```
python .\make_trays.py
```
That will do nothing but print some information to help you get started.  So try:
```
python .\make_trays.py -o mytrays
```
This tells Tray Generator to place all generated objects in to a subfolder called "mytrays".
But nothing is generated yet because you haven't told Tray Generator what size trays you want to create.
So, next:

```
python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1
This is what is going to happen:
Number of objects declared:         2
Number of objects to be gen/sliced: 2, 0
Number of objects existing:         0

You can disable this prompt with "--doit"
Are you ready to do this? [Y/n]:
```
Finally, something good is going to happen.  You can see that two trays are going to be created.  
Each tray will be the dimensions you specified on the command line.  By the way, the default unit scale 
is inches, but Tray Generator works just as well with metric by specifying "-u/--units cm" on the command line.
All dimensions expressed in the command line parameters are expressed using the chosen unit scale.

So before Tray Generator does anything, it will ask you if you're ready to proceed.  This is done, by
default, because Tray Generator is capable of generating 1000's of trays in a single invocation, and 
that can take many hours to complete (of course you can always abort, but still...)

You can also specify "-d/--dryrun" on the command line and Tray Generator will just print out a list
operations that will execute to generate the trays.  This is a great way of seeing what is going to happen.

Go ahead and type "n" to cancel the process, then add the -d parameter:

```
python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -d
Generating: (1 of 2):
     Rendering: mytrays/4-in-L/4-in-W/1-in-H/tray_4x4x1.png mytrays/4-in-L/4-in-W/1-in-H/tray_4x4x1.3mf
Generating: (2 of 2):
     Rendering: mytrays/6-in-L/4-in-W/1-in-H/tray_6x4x1.png mytrays/6-in-L/4-in-W/1-in-H/tray_6x4x1.3mf

Summary:
Number of objects declared:         2
Number of objects to be gen/sliced: 2, 0
Number of objects existing:         0
```
Now you can see more details about the two trays that are going to be generated, including where the
files will be located.  By default, Tray Generator will organize the trays into subfolders organized first
by length, then by width, then by height.  If you are creating a large library of trays this will make
it much easier to find the tray you want to print in the future.  You can, however, use the "--flat"
command line option to have all generate files placed in the top level of the output folder.  Try it:

```
python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -d
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
python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 --flat --doit
Generating: (1 of 2):
     Rendering: mytrays/tray_4x4x1.png mytrays/tray_4x4x1.3mf
Generating: (2 of 2):
     Rendering: mytrays/tray_6x4x1.png mytrays/tray_6x4x1.3mf

Summary:
Number of objects declared:         2
Number of objects to be gen/sliced: 0, 0
Number of objects existing:         2
```
That's it.  Take a look at what you just created:
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
You can see that we have one png file and one 3mf file for each tray we just generated.
Since tray generation can be quite slow (OpenSCAD is not fast) you can also specify 
"-p/--preview_only" on the command line and only generate the png preview files.  This is 
fairly fast and is a great way to see what your library will  look like before committing 
to the full model generation.  You your favorite file browser/image viewer to check out
the png file previews.

Tray Generator generates 3mf model files by default.  You can specify STL, but be aware that
at this time OpenSCAD generates STL files with many errors that some slicers don't even
notice.  (When I started this I was using STL files because that's what I always used. I 
loaded the STL into my slicer and it looked fine, but when I printed it, some walls were
just plain missing.  I was baffled.  Finally, after looking at the layers view I saw that
the wall was missing in there, but not in the preview.  Googling revealed the known issues 
exporting STLs from OpenSCAD, and more googling revealed that 3mf was superior format.  
I tried it. It worked. The model still has errors, but PrusaSlicer detects and repairs 
them automatically.

Anyway, if you want STL files (or any other format that OpenSCAD exports to), use the 
"-e/-export_model_as" command line parameter;

```
python .\make_trays.py -o mytrays --dimensions 4x4x1 6x4x1 -e STL
```

## Printing Your Trays

This is mostly up to you.  You know your printer and how to make it print well. But I very
highly recommend printing with supports if you are printing stackable trays.  Stackable
trays have a recessed edge at the bottom with a 90 degree corner.  If you don't print
with supports, your edged will sag and the trays will not stack nicely.
## Authors & Contributors

Contributors names and contact info

* just me, so far...

## Version History

* no official releases, yet.

## License

This project is licensed under GPL v2 License - see the LICENSE.md file for details

