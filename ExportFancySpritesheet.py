#!/usr/bin/env python

# This tells Python to load the Gimp module 
from gimpfu import *

# create an output function that redirects to gimp's Error Console
def gprint( text ):
  pdb.gimp_message(text)
  return 

# This is the function that will perform actual actions
def fancy_spritesheet(image, drawable) :
  
  max_layer_width = 0
  image_height = 0
  
  LAYER_HEIGHT = 300
  TITLE_HEIGHT = 40
  IMAGE_PADDING = 10
  SPRITE_MARGIN = 10
  SPRITE_SCALE = 2
  SPRITE_CAPTION_HEIGHT = 30
  SHADOW_OFFSET = 4
  SHADOW_OPACITY = 30
  
  # scan layers for image size
  for layer in image.layers:
    if pdb.gimp_item_is_group( layer ):
      children_info = pdb.gimp_item_get_children( layer )
      children_count = children_info[0]
      children = children_info[1]
      sprite_width = gimp.Item.from_id( children[0] ).width * SPRITE_SCALE
      sprite_height = gimp.Item.from_id( children[0] ).height * SPRITE_SCALE
      #gprint ( "sprites %s : %s x %s " % ( children_count, sprite_width, sprite_height ) )
      layer_width = IMAGE_PADDING * 2 + ( sprite_width + SPRITE_MARGIN ) * children_count
      #gprint ( "group %s width %s " % ( layer.name, layer_width ) )
      max_layer_width = max( max_layer_width, layer_width )
      image_height += LAYER_HEIGHT
    else: 
      pass
  
  #create new image
  image_width = max_layer_width
  gprint ( "creating new image %s x %s " % ( image_width, image_height ) )
  out_image = pdb.gimp_image_new( image_width, image_height, 0 )
  pdb.gimp_display_new(out_image)
  
  #create bgr layer
  layer = pdb.gimp_layer_new(out_image, image_width, image_height, 1, "bgr", 100, 0)
  pdb.gimp_image_insert_layer( out_image, layer, None, 0 )
  pdb.gimp_context_set_foreground( (115,64,40) )
  pdb.gimp_drawable_fill(layer, 0)
  
  #draw layers
  offset_y = 0
  for layer in image.layers:
    if pdb.gimp_item_is_group( layer ):
      #analyze
      children_info = pdb.gimp_item_get_children( layer )
      children_count = children_info[0]
      children = children_info[1]
      sprite_width = gimp.Item.from_id( children[0] ).width * SPRITE_SCALE
      sprite_height = gimp.Item.from_id( children[0] ).height * SPRITE_SCALE
      #create container
      container = pdb.gimp_layer_group_new( out_image )
      container.name = layer.name
      pdb.gimp_image_insert_layer( out_image, container, None, 0 )
      
      #create inner container for shaded layers
      shadedLayers = []
      shaded = pdb.gimp_layer_group_new( out_image )
      shaded.name = layer.name + "_shaded"
      pdb.gimp_image_insert_layer( out_image, shaded, container, 0 )
      
      #create group title
      title_layer = pdb.gimp_text_layer_new( out_image, layer.name, "Nokia Cellphone FC", 32, 0 )
      pdb.gimp_image_insert_layer( out_image, title_layer, shaded, 0 )
      pdb.gimp_text_layer_set_color(title_layer, (255,255,255) )
      pdb.gimp_layer_set_offsets(title_layer, 10, 10 + offset_y )
      
      offset_x = SPRITE_MARGIN
      #loop across individual sprites
      for sprite_id in children:
        sprite_src = gimp.Item.from_id( sprite_id )
        sprite = pdb.gimp_layer_new_from_drawable(sprite_src, out_image)
        
        #copy sprite
        sprite.name = sprite_src.name
        pdb.gimp_image_insert_layer( out_image, sprite, shaded, 0 )
        pdb.gimp_context_set_interpolation( 0 )
        pdb.gimp_layer_scale(sprite, sprite_width, sprite_height, TRUE )
        pdb.gimp_layer_set_offsets( sprite, offset_x, offset_y + TITLE_HEIGHT )
        pdb.gimp_item_set_visible( sprite, TRUE )
        shadedLayers.append( sprite )
        
        #create caption
        caption_layer = pdb.gimp_text_layer_new( out_image, sprite_src.name, "Nokia Cellphone FC", 8, 0 )
        pdb.gimp_image_insert_layer( out_image, caption_layer, container, 0 )
        pdb.gimp_text_layer_set_color(caption_layer, (255,255,255) )
        pdb.gimp_text_layer_set_justification(caption_layer, 2)
        pdb.gimp_layer_set_offsets(caption_layer, offset_x, offset_y + TITLE_HEIGHT + sprite_height + 10 )
        pdb.gimp_text_layer_resize(caption_layer, sprite_width, SPRITE_CAPTION_HEIGHT )
        
        offset_x += sprite_width + SPRITE_MARGIN
      
      #merge shaded layers
      for l in shadedLayers:
        merged_layer = pdb.gimp_image_merge_down(out_image, l, 0 )
      
      #create shadow layer
      shadow = pdb.gimp_layer_copy(merged_layer, TRUE )
      pdb.gimp_image_insert_layer( out_image, shadow, shaded, 1 )
      pdb.gimp_layer_set_offsets( shadow, 10 + SHADOW_OFFSET, 10 + offset_y + SHADOW_OFFSET )
      pdb.gimp_layer_set_lock_alpha(shadow, TRUE)
      pdb.gimp_context_set_foreground( (0,0,0) )
      pdb.gimp_edit_fill(shadow, 0 )
      pdb.gimp_layer_set_opacity( shadow, SHADOW_OPACITY )
      
      offset_y += LAYER_HEIGHT
    else: 
      pass
  
  #flatten image into a single layer
  pdb.gimp_image_flatten(out_image)
  
  return

# This is the plugin registration function
# I have written each of its parameters on a different line 
register(
    "fancy_spritesheet",    
    "Export Fancy Spritesheet",   
    "Export a fancy annotated layers",
    "Jaroslav Meloun", 
    "Jarnik www.jarnik.com", 
    "August 2013",
    "<Image>/MyScripts/Export Fancy Spritesheet", 
    "*", 
    [], 
    [],
    fancy_spritesheet,
    )

main()
