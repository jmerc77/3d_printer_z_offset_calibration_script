# 3d_printer_z_offset_calibration_script
For calibrating Z offset of your 3d printer.

## Generating the test file

Open `Z offset box calibration.py` and adjust the settings at the top to match your:

- nozzle diameter
- default layer height
- max extra Z to test
- flow
- nozzle temp
- bed temp
- filament diameter
- linear advance value
- retract speed
- retract amount
- bed center position

Run then preview to ensure it fits bed. Extrusions may not render properly, but are fine.
Bigger nozzles make bigger test prints. However, you can open the `Z offset box.3mf` in PrusaSlicer and change the nozzle size.
Then, run `gcode prep.py` to create the new template. Be sure to note the print out during run (temp_w=[some number]).
Next, edit `Z offset box calibration.py` and in the template params, input:
- the `temp_w` value noted prior
- the new `temp_noz_d` value from the nozzle diameter setting in the slicer

## Using and reading the test

Start by having your Z ofset too close (ie. causing "elephants' foot").
Then, start the print. Once complete, look for where it starts to show loose strands or holes in the solid fill.
The side closest to home (either X=0 or X<0 if X=0 is center) should be solid and could be overly squished.
Measure the width of the fill and divide it into the distance of the solid looking area.
Mutiply by the extra Z and raise the Z offset by that much.
Re-test to be sure.
