#!/usr/bin/python
#coding=utf-8
import os
import sys
import re
import random
import getopt
from PIL import Image,ImageDraw

def make_pola(input_filename,
              output_filename,
              content_rate_width=3.1,
              content_rate_height=3.1,
              pola_rate_width=3.5,
              pola_rate_height=4.2,
              page_rate_width=3.5,
              page_rate_height=5.0):
    print "input_filename:%s"%(input_filename,)
    image_input=Image.open(input_filename)
    content_width=image_input.size[0]
    content_height=image_input.size[1]
    if content_width!=content_height:
        print "Input image should be square size"
        exit(1)
    page_width=page_rate_width*content_width/content_rate_width
    page_height=page_rate_height*page_width/page_rate_width
    padding=(page_width-content_width)/2
    image_output=Image.new('RGBA',(int(page_width),int(page_height)),'white')
    image_output.paste(image_input,(int(padding),int(padding)))
    #crop line
    crop_y=pola_rate_height*page_width/pola_rate_width
    print "[%f,%f],[%f,%f],%f,%f"%(content_width,content_height,page_width,page_height,padding,crop_y)
    draw_image=ImageDraw.Draw(image_output)
    draw_image.line([(0,crop_y),(page_width,crop_y)],fill='gray')
    del draw_image
    image_output.save(output_filename,image_input.format,quality=95)
    print "save_to_file:%s"%(output_filename)

if __name__=="__main__":
    filename_input="/Users/reynoldqin/Pictures/IMG_0897.JPG"
    filename_output="/Users/reynoldqin/Pictures/IMG_0897_output.JPG"
    make_pola(filename_input,filename_output) 
