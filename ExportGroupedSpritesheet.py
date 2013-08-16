#!/usr/bin/env python

import os

# This tells Python to load the Gimp module 
from gimpfu import *

# create an output function that redirects to gimp's Error Console
def gprint( text ):
  pdb.gimp_message(text)
  return 

def scan_layer( layer ):
  if not pdb.gimp_item_is_group( layer ):
    return [ layer ]
  children_info = pdb.gimp_item_get_children( layer )
  children_count = children_info[0]
  children = children_info[1]
  layers = []
  for id in children:
    l = gimp.Item.from_id( id )
    layers.extend( scan_layer( l ) )
  return layers

def export_grouped_spritesheet_layers( layers, max_width ) :
  
  #layers.reverse()
  sprites = []
  #gather all sprites
  for layer in layers:
    sprites.extend( scan_layer( layer ) )
  
  #compute image extents
  sprite_width = sprites[ 0 ].width
  sprite_height = sprites[ 0 ].height
  cols = min( math.floor( max_width / sprite_width ), len( sprites ) )
  rows = math.ceil( len( sprites ) / cols )
  image_width = sprite_width * cols
  image_height = sprite_height * rows
  #gprint( "cols %s rows %s img %s x %s " % ( cols, rows, image_width, image_height ) )
  
  #add all sprites
  image = pdb.gimp_image_new( image_width, image_height, 0 )
  offset_x = 0
  offset_y = 0
  for sprite_src in sprites:
    sprite = pdb.gimp_layer_new_from_drawable(sprite_src, image)
    pdb.gimp_image_insert_layer( image, sprite, None, 0 )
    pdb.gimp_layer_set_offsets( sprite, offset_x, offset_y )
    pdb.gimp_item_set_visible( sprite, TRUE )
    offset_x += sprite_width
    if offset_x >= sprite_width * cols:
      offset_x = 0
      offset_y += sprite_height
  
  return image
  
  
# This is the function that will perform actual actions
def export_grouped_spritesheet(image, drawable, export_all, export_layer, max_width, save, dir, filename ) :
  #gprint( "params %s %s %s %s %s " % ( export_all, export_layer, max_width, dir, filename ) )
  
  layers = image.layers
  if not export_all:
    layers = [ export_layer ]
  
  image_out = export_grouped_spritesheet_layers( layers, max_width )
  
  #flatten image into a single layer
  merged = pdb.gimp_image_merge_visible_layers(image_out, 1)
  
  pdb.gimp_display_new(image_out)
  
  filename = "%s\\%s" % ( dir, filename )
  pdb.gimp_image_set_filename(image_out, filename)
  
  if save
    pdb.file_png_save_defaults( image_out, merged, filename, filename )
  
  gprint( "Saved to %s " % ( filename ) )
  
  return

# This is the plugin registration function
# I have written each of its parameters on a different line 
register(
    "export_grouped_spritesheet",    
    "Export Grouped Spritesheet",   
    "Export spritesheet, including recursive layer groups",
    "Jaroslav Meloun", 
    "Jarnik www.jarnik.com", 
    "August 2013",
    "<Image>/MyScripts/Export Grouped Spritesheet", 
    "*", 
    [
      (PF_BOOL, 'export_all', 'Export All Layers', TRUE ),
      (PF_LAYER, 'export_layer', 'Or selected layer:', None ),
      (PF_FLOAT, 'max_width', 'Maximum spritesheet width', 1024 ),
      (PF_BOOL, 'save', 'Save to file', TRUE ),
      (PF_DIRNAME, 'dir', 'Output directory', os.getcwd() ),
      (PF_STRING, 'filename', 'Output filename', 'spritesheet.png' )
    ], 
    [],
    export_grouped_spritesheet,
    )

main()
