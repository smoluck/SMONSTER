#!/usr/bin/env python
# encoding: utf-8
# Made with Replay
# mechanicalcolor.com

#import the necessary Python libraries
import os
import lx

# get modo's temp dir
temp_dir = lx.eval('query platformservice path.path ? temp')
# name our temp file
temp_file = "REBEVEL_01.lxo"
# builds the complete path out of the temp dir and the temp file name
temp_path = os.path.join(temp_dir, "SMO_REBEVEL", temp_file)

# make sure the SMO_REBEVEL directory exists, if not create it
if not os.path.exists(os.path.dirname(temp_path)):
    # try to create the directory. 
    try:
        os.makedirs(os.path.dirname(temp_path))
    except:
        # if that fails for any reason print out the error
        print(traceback.format_exc())

# replay name:"Save Scene As"
# here we just call the save as command with our new custom
# path Python style instead of macro style.
lx.eval('!scene.saveAs filename:"{}" format:"$LXOB" export:false'.format(temp_path))