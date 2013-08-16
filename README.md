Installation
==================
See:
- http://www.gimp.org/docs/python/
- http://www.gimpusers.com/tutorials/install-python-for-gimp-2-6-windows
- http://www.exp-media.com/content/extending-gimp-python-python-fu-plugins-part-1

Export Fancy Annotated Spritesheet
==================================
Python plugin script to create a fancy spritesheet preview.

Will work as expected under following circumstances:
- sprites have uniform size, each sprite in a separate layer
- there are multiple group layers (GIMP 2.8+) at the root
- each group layer contains multiple sprites
Will open a new image containing the spritesheet.
The annotations are taken directly from the group / layer names.

Screenshots
===========
- "layer_structure.png" - an example layer structure
- "export_grouped_spritesheet.png" - plugin window
- "fancy_annotated_spritesheet.png" - expected result

It's a single-purpose script, tweak at your own will for other purposes
