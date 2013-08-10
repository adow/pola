#!/usr/bin/python
#coding=utf-8
# pola.py
#
# Make polariod photos on common photo paper. 
# ln -s /$POLA_PATH/pola.py /usr/bin/pola
# Enter the folder that contains original photos:
#    $ cd PATH_OF_PHOTOS 
# Run it: 
#    $ pola
# You will find output photos in 'pola_output'

import os
import sys
import getopt
from PIL import Image,ImageDraw

def make_pola(input_filename,
              output_filename,
              content_rate=3.1,
              pola_rate_width=3.5,
              pola_rate_height=4.2,
              page_rate_width=3.5,
              page_rate_height=5.0):
    '''
    input_filename,output_filename,
    content_rate_width equals to content_rate_height means square , 
    pola_rate_width andpola_rate_height spceificed clipping area, 
    page_rate_width and page_rate_height to generate page size. 
    '''
    image_pola=make_image_pola(input_filename,content_rate=content_rate,
                              pola_rate_width=pola_rate_width,
                              pola_rate_height=pola_rate_height)
    if not image_pola:
        return
    pola_width,pola_height=image_pola.size
    page_width=pola_width*page_rate_width/pola_rate_width 
    page_height=pola_height*page_rate_height/pola_rate_height
    print "%f,%f,%f,%f"%(pola_width,pola_height,page_width,page_height,)
    image_output=Image.new('RGBA',(int(page_width),int(page_height)),'white')
    image_output.paste(image_pola,(0,0,int(pola_width),int(pola_height)))
    #crop line
    crop_y=pola_height
    draw_image=ImageDraw.Draw(image_output)
    draw_image.line([(0,crop_y),(page_width,crop_y)],fill='#3f3f3f')
    del draw_image
    image_output.save(output_filename,image_pola.format,quality=95)
    print "save_to_file:%s"%(output_filename)

def make_pola_in_folder(folder,
                       content_rate=3.1,
                      pola_rate_width=3.5,
                      pola_rate_height=4.2,
                      page_rate_width=3.5,
                      page_rate_height=5.0):
    '''
    output images will be put in to sub dictionary(pola_output) of specificed folder. 
    '''
    all=os.listdir(folder)
    images=[os.path.join(folder,f) for f in all if os.path.splitext(f)[-1].upper() in ['.JPG','JPEG','.PNG']]
    #print images
    for one_image in images:
        dir,filename=os.path.split(one_image)
        dir_output=os.path.join(dir,'pola_output')
        output_filename=os.path.join(dir_output,filename)
        if not os.path.exists(dir_output):
            os.makedirs(dir_output) 
        make_pola(one_image,output_filename,
                 content_rate=content_rate,
                 pola_rate_width=pola_rate_width,
                 pola_rate_height=pola_rate_height,
                 page_rate_width=page_rate_width,
                 page_rate_height=page_rate_height)
    print 'make polas completed'

def make_double_pola(output_filename,
                     input_filename_left,input_filename_right,
                     content_rate=3.1,
                     pola_rate_width=3.5,
                     pola_rate_height=4.2,
                     page_rate_width=5.0,
                     page_rate_height=3.5,
                    split_line=True,
                    crop_line=True):
    image_left=make_image_pola(input_filename_left,content_rate=content_rate,
                               pola_rate_width=pola_rate_width,
                               pola_rate_height=pola_rate_height)
    image_right=make_image_pola(input_filename_right,content_rate=content_rate,
                                pola_rate_width=pola_rate_width,
                                pola_rate_height=pola_rate_height)
    pola_width=image_left.size[0]+image_right.size[0]
    pola_height=image_left.size[1]
    page_width=pola_width
    page_height=page_width*page_rate_height/page_rate_width
    print "%f,%f"%(pola_width,pola_height)
    image_output=Image.new('RGBA',(int(page_width),int(page_height)),'white')
    box_left=(0,0,int(image_left.size[0]),
              int(image_left.size[1]))
    print box_left
    image_output.paste(image_left,(0,0,int(image_left.size[0]),
                                   int(image_left.size[1])))
    box_right=(int(image_left.size[0]),0,
               pola_width,
               pola_height)
    print box_right
    image_output.paste(image_right,box_right)
    #crop line
    draw_image=ImageDraw.Draw(image_output)
    if crop_line:
        draw_image.line([(0,pola_height),(page_width,pola_height)],fill='#3f3f3f')
    if split_line:
        draw_image.line([(pola_width/2,0),(pola_width/2,page_height)],fill='#3f3f3f')
    del draw_image
    image_output.save(output_filename,image_left.format,quality=95)
    print "save to file:%s"%(output_filename)

def make_square(input_filename,output_filename,
                     content_rate=3.1,
                     pola_rate=3.5,
                     page_rate_width=3.5,
                     page_rate_height=5.0):
    image_square=make_image_square(input_filename,
                                   content_rate=content_rate,
                                   pola_rate=pola_rate)
    if not image_square:
        return
    page_width=int(image_square.size[0])
    page_height=int(page_width*page_rate_height/page_rate_width)
    image_output=Image.new('RGBA',(page_width,page_height),'white')
    image_output.paste(image_square,(0,0))
    #crop line
    draw_image=ImageDraw.Draw(image_output)
    draw_image.line([(0,page_width),(page_width,page_width)],fill='#3f3f3f')
    image_output.save(output_filename,image_square.format,quality=95)
    print "save_to_file:%s"%(output_filename)

def make_square_in_folder(folder):
    all=os.listdir(folder)
    images=[os.path.join(folder,f) for f in all if os.path.splitext(f)[-1].upper() in ['.JPG','JPEG','.PNG']]
    #print images
    for one_image in images:
        dir,filename=os.path.split(one_image)
        dir_output=os.path.join(dir,'pola_output')
        output_filename=os.path.join(dir_output,filename)
        if not os.path.exists(dir_output):
            os.makedirs(dir_output) 
        make_square(one_image,output_filename)
    print 'make polas completed'

def make_four_square(output_filename,
                        input_filename_1,
                     input_filename_2,
                     input_filename_3,
                     input_filename_4,
                     content_rate=3.1,
                     pola_rate=3.5,
                    page_rate_width=4,
                    page_rate_height=6,
                    split_line=True,
                    crop_line=True):
    image_1=make_image_square(input_filename_1,content_rate=content_rate,
                              pola_rate=pola_rate)
    image_2=make_image_square(input_filename_2,content_rate=content_rate,
                              pola_rate=pola_rate)
    image_3=make_image_square(input_filename_3,content_rate=content_rate,
                              pola_rate=pola_rate)
    image_4=make_image_square(input_filename_4,content_rate=content_rate,
                              pola_rate=pola_rate)
    pola_width=int(image_1.size[0])
    padding=int(pola_width*(pola_rate-content_rate)/2)
    page_width=image_1.size[0]*2-padding
    page_height=page_width*page_rate_height/page_rate_width
    print "%f,%f,%f,%f"%(pola_width,padding,page_width,page_height,)
    image_output=Image.new('RGBA',(int(page_width),int(page_height)),'white')
    box_1=(0,0,pola_width,pola_width)
    box_2=(pola_width-padding,0,pola_width*2-padding,pola_width)
    box_3=(0,pola_width-padding,pola_width,pola_width*2-padding)
    box_4=(pola_width-padding,pola_width-padding,pola_width*2-padding,pola_width*2-padding)
    print box_1,box_2,box_3,box_4
    image_output.paste(image_1,box_1)
    image_output.paste(image_2,box_2)
    image_output.paste(image_3,box_3)
    image_output.paste(image_4,box_4)
    #crop line
    draw_image=ImageDraw.Draw(image_output)
    if crop_line:
        draw_image.line([(0,page_width),(page_width,page_width)],
                        fill='#3f3f3f')
    image_output.save(output_filename,image_1.format,quality=95)
    print "save to file:%s"%(output_filename)

#make images
def make_image_pola(input_filename,
                    content_rate=3.1,
                    pola_rate_width=3.5,
                    pola_rate_height=4.2):
    image_input=Image.open(input_filename)
    content_width,content_height=image_input.size
    if content_width!=content_height:
        print "Input image should be square size:%f,%f"%(content_width,content_height,)
        return None
    pola_width=content_width*pola_rate_width/content_rate 
    pola_height=pola_width*pola_rate_height/pola_rate_width
    padding=(pola_width-content_width)/2
    image_output=Image.new('RGBA',(int(pola_width),int(pola_height)),'white')
    image_output.paste(image_input,(int(padding),int(padding)))
    return image_output

def make_image_square(input_filename,
                      content_rate=3.1,
                      pola_rate=3.5):
    return make_image_pola(input_filename,content_rate=content_rate,
                           pola_rate_width=pola_rate,
                           pola_rate_height=pola_rate)
    
#test
def _test_make_double_pola():
    input_filename_left='/Users/reynoldqin/Pictures/pola/IMG_0948.JPG'
    input_filename_right='/Users/reynoldqin/Pictures/pola/IMG_0952.JPG'
    output_filename='/Users/reynoldqin/Pictures/pola/pola_double.JPG'
    make_double_pola(output_filename,input_filename_left,input_filename_right)

def _test_make_four_square():
    input_filename_1='/Users/reynoldqin/Pictures/pola/IMG_0948.JPG'
    input_filename_2='/Users/reynoldqin/Pictures/pola/IMG_0952.JPG'
    input_filename_3='/Users/reynoldqin/Pictures/pola/IMG_0950.JPG'
    input_filename_4='/Users/reynoldqin/Pictures/pola/IMG_0949.JPG'
    output_filename='/Users/reynoldqin/Pictures/pola/four_square.JPG'
    make_four_square(output_filename,
                     input_filename_1,input_filename_2,
                     input_filename_3,input_filename_4)


if __name__=="__main__":
    #filename_input="/Users/reynoldqin/Pictures/IMG_0897.JPG"
    #filename_output="/Users/reynoldqin/Pictures/IMG_0897_output.JPG"
    #image_pola=make_image_pola(filename_input)
    #image_pola=make_image_square(filename_input)
    #image_pola.save(filename_output)
    #make_pola(filename_input,filename_output)
    #make_pola_in_folder("/Users/reynoldqin/Pictures/pola")
    #_test_make_double_pola()
    #_test_make_four_square()

    folder='.'
    if len(sys.argv)>1:
        folder=sys.argv[1]
    print folder
    cmd='pola'
    if len(sys.argv)>2:
        cmd=sys.argv[2]
    if cmd=='square':
        make_square_in_folder(folder)
    elif cmd=='pola':
        make_pola_in_folder(folder)
