#python
#---------------------------------------
# Name:         SMO_SMONSTER_CheckKitLoad_Cmd.py
# Version:      1.0
#
# Purpose:      This script is designed to
#               Query UV Map count and name in all the scene and
#               query UV Map count and name in selected meshes.
#
#
# Author:       Franck ELISABETH (with the help of Tom Dymond for debug)
# Website:      http://www.smoluck.com
#
# Created:      29/07/2020
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

import lx, os, re

SMO_KitsList = ['SMONSTER', 'SMO_AI_TOOLS', 'SMO_BAKE', 'SMO_BATCH', 'SMO_CAD_TOOLS', 'SMO_CLEANUP', 'SMO_COLOR_BAR', 'SMO_GAME_CONTENT', 'SMO_MASTER', 'SMO_MARMOSET_LIVELINK', 'SMO_MATH_TOOLS', 'SMO_MESHOPS', 'SMO_MIFABOMA', 'SMO_PCLOUD_XYZ', 'SMO_PIXAFLUX_LIVELINK', 'SMO_QUICK_TAG', 'SMO_RIZOMUV_LIVELINK', 'SMO_UV', 'SMO_VENOM']

SMONSTER_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[0] + " ?")
SMO_AI_TOOLS_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[1] + " ?")
SMO_BAKE_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[2] + " ?")
SMO_BATCH_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[3] + " ?")
SMO_CAD_TOOLS_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[4] + " ?")
SMO_CLEANUP_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[5] + " ?")
SMO_COLOR_BAR_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[6] + " ?")
SMO_GAME_CONTENT_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[7] + " ?")
SMO_MASTER_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[8] + " ?")
SMO_MARMOSET_LIVELINK_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[9] + " ?")
SMO_MATH_TOOLS_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[10] + " ?")
SMO_MESHOPS_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[11] + " ?")
SMO_MIFABOMA_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[12] + " ?")
SMO_PCLOUD_XYZ_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[13] + " ?")
SMO_PIXAFLUX_LIVELINK_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[14] + " ?")
SMO_QUICK_TAG_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[15] + " ?")
SMO_RIZOMUV_LIVELINK_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[16] + " ?")
SMO_UV_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[17] + " ?")
SMO_VENOM_Status = lx.eval("kit.toggleEnable " + SMO_KitsList[18] + " ?")

lx.out("-------- SMO Kits List: LOADED --------")
lx.out("V-VV-VVV-----------------------VVV-VV-V")

if SMONSTER_Status == True :
    kit_folder_SMONSTER = lx.eval("query platformservice alias ? {kit_SMONSTER:}")
    index_file_SMONSTER = os.path.join(kit_folder_SMONSTER, "index.cfg")
    with open(index_file_SMONSTER, 'r') as index_file_data_SMONSTER:
        xml_as_string = index_file_data_SMONSTER.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_SMONSTER_version_installed = m.group(1)
    lx.out("SMONSTER - version: %s" % SMO_SMONSTER_version_installed)
    index_file_data_SMONSTER.close()
    
if SMO_AI_TOOLS_Status == True :
    kit_folder_SMO_AI_TOOLS = lx.eval("query platformservice alias ? {kit_SMO_AI_TOOLS:}")
    index_file_SMO_AI_TOOLS = os.path.join(kit_folder_SMO_AI_TOOLS, "index.cfg")
    with open(index_file_SMO_AI_TOOLS, 'r') as index_file_data_SMO_AI_TOOLS:
        xml_as_string = index_file_data_SMO_AI_TOOLS.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_AI_TOOLS_version_installed = m.group(1)
    lx.out("SMO AI TOOLS - version: %s" % SMO_AI_TOOLS_version_installed)
    index_file_data_SMO_AI_TOOLS.close()
    
if SMO_BAKE_Status == True :
    kit_folder_SMO_BAKE = lx.eval("query platformservice alias ? {kit_SMO_BAKE:}")
    index_file_SMO_BAKE = os.path.join(kit_folder_SMO_BAKE, "index.cfg")
    with open(index_file_SMO_BAKE, 'r') as index_file_data_SMO_BAKE:
        xml_as_string = index_file_data_SMO_BAKE.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_BAKE_version_installed = m.group(1)
    lx.out("SMO BAKE Kit - version: %s" % SMO_BAKE_version_installed)
    index_file_data_SMO_BAKE.close()

if SMO_BATCH_Status == True :
    kit_folder_SMO_BATCH = lx.eval("query platformservice alias ? {kit_SMO_BATCH:}")
    index_file_SMO_BATCH = os.path.join(kit_folder_SMO_BATCH, "index.cfg")
    with open(index_file_SMO_BATCH, 'r') as index_file_data_SMO_BATCH:
        xml_as_string = index_file_data_SMO_BATCH.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_BATCH_version_installed = m.group(1)
    lx.out("SMO BATCH - version: %s" % SMO_BATCH_version_installed)
    index_file_data_SMO_BATCH.close()
    
if SMO_CAD_TOOLS_Status == True :
    kit_folder_SMO_CAD_TOOLS = lx.eval("query platformservice alias ? {kit_SMO_CAD_TOOLS:}")
    index_file_SMO_CAD_TOOLS = os.path.join(kit_folder_SMO_CAD_TOOLS, "index.cfg")
    with open(index_file_SMO_CAD_TOOLS, 'r') as index_file_data_SMO_CAD_TOOLS:
        xml_as_string = index_file_data_SMO_CAD_TOOLS.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_CAD_TOOLS_version_installed = m.group(1)
    lx.out("SMO CAD TOOLS - version: %s" % SMO_CAD_TOOLS_version_installed)
    index_file_data_SMO_CAD_TOOLS.close()

if SMO_CLEANUP_Status == True :
    kit_folder_SMO_CLEANUP = lx.eval("query platformservice alias ? {kit_SMO_CLEANUP:}")
    index_file_SMO_CLEANUP = os.path.join(kit_folder_SMO_CLEANUP, "index.cfg")
    with open(index_file_SMO_CLEANUP, 'r') as index_file_data_SMO_CLEANUP:
        xml_as_string = index_file_data_SMO_CLEANUP.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_CLEANUP_version_installed = m.group(1)
    lx.out("SMO CLEANUP - version: %s" % SMO_CLEANUP_version_installed)
    index_file_data_SMO_CLEANUP.close()
    
if SMO_COLOR_BAR_Status == True :
    kit_folder_SMO_COLOR_BAR = lx.eval("query platformservice alias ? {kit_SMO_COLOR_BAR:}")
    index_file_SMO_COLOR_BAR = os.path.join(kit_folder_SMO_COLOR_BAR, "index.cfg")
    with open(index_file_SMO_COLOR_BAR, 'r') as index_file_data_SMO_COLOR_BAR:
        xml_as_string = index_file_data_SMO_COLOR_BAR.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_COLOR_BAR_version_installed = m.group(1)
    lx.out("SMO COLOR BAR - version: %s" % SMO_COLOR_BAR_version_installed)
    index_file_data_SMO_COLOR_BAR.close()
    
if SMO_GAME_CONTENT_Status == True :
    kit_folder_SMO_GAME_CONTENT = lx.eval("query platformservice alias ? {kit_SMO_GAME_CONTENT:}")
    index_file_SMO_GAME_CONTENT = os.path.join(kit_folder_SMO_GAME_CONTENT, "index.cfg")
    with open(index_file_SMO_GAME_CONTENT, 'r') as index_file_data_SMO_GAME_CONTENT:
        xml_as_string = index_file_data_SMO_GAME_CONTENT.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_GAME_CONTENT_version_installed = m.group(1)
    lx.out("SMO GAME CONTENT - version: %s" % SMO_GAME_CONTENT_version_installed)
    index_file_data_SMO_GAME_CONTENT.close()
    
if SMO_MASTER_Status == True :
    kit_folder_SMO_MASTER = lx.eval("query platformservice alias ? {kit_SMO_MASTER:}")
    index_file_SMO_MASTER = os.path.join(kit_folder_SMO_MASTER, "index.cfg")
    with open(index_file_SMO_MASTER, 'r') as index_file_data_SMO_MASTER:
        xml_as_string = index_file_data_SMO_MASTER.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_MASTER_version_installed = m.group(1)
    lx.out("SMO MASTER - version: %s" % SMO_MASTER_version_installed)
    index_file_data_SMO_MASTER.close()
    
if SMO_MATH_TOOLS_Status == True :
    kit_folder_SMO_MATH_TOOLS = lx.eval("query platformservice alias ? {kit_SMO_MATH_TOOLS:}")
    index_file_SMO_MATH_TOOLS = os.path.join(kit_folder_SMO_MATH_TOOLS, "index.cfg")
    with open(index_file_SMO_MATH_TOOLS, 'r') as index_file_data_SMO_MATH_TOOLS:
        xml_as_string = index_file_data_SMO_MATH_TOOLS.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_MATH_TOOLS_version_installed = m.group(1)
    lx.out("SMO MATH TOOLS - version: %s" % SMO_MATH_TOOLS_version_installed)
    index_file_data_SMO_MATH_TOOLS.close()
    
if SMO_MESHOPS_Status == True :
    kit_folder_SMO_MESHOPS = lx.eval("query platformservice alias ? {kit_SMO_MESHOPS:}")
    index_file_SMO_MESHOPS = os.path.join(kit_folder_SMO_MESHOPS, "index.cfg")
    with open(index_file_SMO_MESHOPS, 'r') as index_file_data_SMO_MESHOPS:
        xml_as_string = index_file_data_SMO_MESHOPS.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_MESHOPS_version_installed = m.group(1)
    lx.out("SMO MESHOPS - version: %s" % SMO_MESHOPS_version_installed)
    index_file_data_SMO_MESHOPS.close()
    
if SMO_MIFABOMA_Status == True :
    kit_folder_SMO_MIFABOMA = lx.eval("query platformservice alias ? {kit_SMO_MIFABOMA:}")
    index_file_SMO_MIFABOMA = os.path.join(kit_folder_SMO_MIFABOMA, "index.cfg")
    with open(index_file_SMO_MIFABOMA, 'r') as index_file_data_SMO_MIFABOMA:
        xml_as_string = index_file_data_SMO_MIFABOMA.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_MIFABOMA_version_installed = m.group(1)
    lx.out("SMO MIFABOMA - version: %s" % SMO_MIFABOMA_version_installed)
    index_file_data_SMO_MIFABOMA.close()
    
if SMO_PCLOUD_XYZ_Status == True :
    kit_folder_SMO_PCLOUD_XYZ = lx.eval("query platformservice alias ? {kit_SMO_PCLOUD_XYZ:}")
    index_file_SMO_PCLOUD_XYZ = os.path.join(kit_folder_SMO_PCLOUD_XYZ, "index.cfg")
    with open(index_file_SMO_PCLOUD_XYZ, 'r') as index_file_data_SMO_PCLOUD_XYZ:
        xml_as_string = index_file_data_SMO_PCLOUD_XYZ.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_PCLOUD_XYZ_version_installed = m.group(1)
    lx.out("SMO PCLOUD XYZ - version: %s" % SMO_PCLOUD_XYZ_version_installed)
    index_file_data_SMO_PCLOUD_XYZ.close()
    
if SMO_QUICK_TAG_Status == True :
    kit_folder_SMO_QUICK_TAG = lx.eval("query platformservice alias ? {kit_SMO_QUICK_TAG:}")
    index_file_SMO_QUICK_TAG = os.path.join(kit_folder_SMO_QUICK_TAG, "index.cfg")
    with open(index_file_SMO_QUICK_TAG, 'r') as index_file_data_SMO_QUICK_TAG:
        xml_as_string = index_file_data_SMO_QUICK_TAG.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_QUICK_TAG_version_installed = m.group(1)
    lx.out("SMO QUICK TAG - version: %s" % SMO_QUICK_TAG_version_installed)
    index_file_data_SMO_QUICK_TAG.close()
    
if SMO_UV_Status == True :
    kit_folder_SMO_UV = lx.eval("query platformservice alias ? {kit_SMO_UV:}")
    index_file_SMO_UV = os.path.join(kit_folder_SMO_UV, "index.cfg")
    with open(index_file_SMO_UV, 'r') as index_file_data_SMO_UV:
        xml_as_string = index_file_data_SMO_UV.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_UV_version_installed = m.group(1)
    lx.out("SMO UV - version: %s" % SMO_UV_version_installed)
    index_file_data_SMO_UV.close()
    
if SMO_VENOM_Status == True :
    kit_folder_SMO_VENOM = lx.eval("query platformservice alias ? {kit_SMO_VENOM:}")
    index_file_SMO_VENOM = os.path.join(kit_folder_SMO_VENOM, "index.cfg")
    with open(index_file_SMO_VENOM, 'r') as index_file_data_SMO_VENOM:
        xml_as_string = index_file_data_SMO_VENOM.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_VENOM_version_installed = m.group(1)
    lx.out("SMO VENOM - version: %s" % SMO_VENOM_version_installed)
    index_file_data_SMO_VENOM.close()
lx.out("A-AA-AAA-----------------------AAA-AA-A")


lx.out("-------- Kits list: LIVELINK LOADED --------")
lx.out("V-VV-VVV---------------------------VVV-VV-V")

if SMO_MARMOSET_LIVELINK_Status == True:
    kit_folder_SMO_MARMOSET_LIVELINK = lx.eval("query platformservice alias ? {kit_SMO_MARMOSET_LIVELINK:}")
    index_file_SMO_MARMOSET_LIVELINK = os.path.join(kit_folder_SMO_MARMOSET_LIVELINK, "index.cfg")
    with open(index_file_SMO_MARMOSET_LIVELINK, 'r') as index_file_data_SMO_MARMOSET_LIVELINK:
        xml_as_string = index_file_data_SMO_MARMOSET_LIVELINK.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_MARMOSET_LIVELINK_version_installed = m.group(1)
    lx.out("SMO MARMOSET LIVELINK - version: %s" % SMO_MARMOSET_LIVELINK_version_installed)
    index_file_data_SMO_MARMOSET_LIVELINK.close()

if SMO_PIXAFLUX_LIVELINK_Status == True:
    kit_folder_SMO_PIXAFLUX_LIVELINK = lx.eval("query platformservice alias ? {kit_SMO_PIXAFLUX_LIVELINK:}")
    index_file_SMO_PIXAFLUX_LIVELINK = os.path.join(kit_folder_SMO_PIXAFLUX_LIVELINK, "index.cfg")
    with open(index_file_SMO_PIXAFLUX_LIVELINK, 'r') as index_file_data_SMO_PIXAFLUX_LIVELINK:
        xml_as_string = index_file_data_SMO_PIXAFLUX_LIVELINK.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_PIXAFLUX_LIVELINK_version_installed = m.group(1)
    lx.out("SMO PIXAFLUX LIVELINK - version: %s" % SMO_PIXAFLUX_LIVELINK_version_installed)
    index_file_data_SMO_PIXAFLUX_LIVELINK.close()

if SMO_RIZOMUV_LIVELINK_Status == True :
    kit_folder_SMO_RIZOMUV_LIVELINK = lx.eval("query platformservice alias ? {kit_SMO_RIZOMUV_LIVELINK:}")
    index_file_SMO_RIZOMUV_LIVELINK = os.path.join(kit_folder_SMO_RIZOMUV_LIVELINK, "index.cfg")
    with open(index_file_SMO_RIZOMUV_LIVELINK, 'r') as index_file_data_SMO_RIZOMUV_LIVELINK:
        xml_as_string = index_file_data_SMO_RIZOMUV_LIVELINK.read().replace('\n', '')
    r = r'<[ ]*configuration[^>]*version[ =]*[\"\']([^\"\']*)[\"\']'
    m = re.search(r, xml_as_string)
    SMO_RIZOMUV_LIVELINK_version_installed = m.group(1)
    lx.out("SMO RIZOMUV LIVELINK - version: %s" % SMO_RIZOMUV_LIVELINK_version_installed)
    index_file_data_SMO_RIZOMUV_LIVELINK.close()
lx.out("A-AA-AAA---------------------------AAA-AA-A")


lx.out("-------- Kits list: NOT LOADED --------")
lx.out("V-VV-VVV----------------------VVV-VV-V")
if SMONSTER_Status == False :
    lx.out("NOT LOADED : SMONSTER")
    
if SMO_AI_TOOLS_Status == False :
    lx.out("NOT LOADED : SMO AI TOOLS")
    
if SMO_BAKE_Status == False :
    lx.out("NOT LOADED : SMO BAKE")
    
if SMO_BATCH_Status == False :
    lx.out("NOT LOADED : SMO BATCH")
    
if SMO_CAD_TOOLS_Status == False :
    lx.out("NOT LOADED : SMO CAD TOOLS")
    
if SMO_CLEANUP_Status == False :
    lx.out("NOT LOADED : SMO CLEANUP")
    
if SMO_COLOR_BAR_Status == False :
    lx.out("NOT LOADED : SMO COLOR BAR")
    
if SMO_GAME_CONTENT_Status == False :
    lx.out("NOT LOADED : SMO GAME CONTENT")

if SMO_MASTER_Status == False:
    lx.out("NOT LOADED : SMO MASTER")

if SMO_MARMOSET_LIVELINK_Status == False:
    lx.out("NOT LOADED : SMO MARMOSET LIVELINK")
    
if SMO_MATH_TOOLS_Status == False :
    lx.out("NOT LOADED : SMO MATH TOOLS")
    
if SMO_MESHOPS_Status == False :
    lx.out("NOT LOADED : SMO MESHOPS")
    
if SMO_MIFABOMA_Status == False :
    lx.out("NOT LOADED : SMO MIFABOMA")
    
if SMO_PCLOUD_XYZ_Status == False :
    lx.out("NOT LOADED : SMO PCLOUD XYZ")
    
if SMO_PIXAFLUX_LIVELINK_Status == False :
    lx.out("NOT LOADED : SMO PIXAFLUX LIVELINK")
    
if SMO_QUICK_TAG_Status == False :
    lx.out("NOT LOADED : SMO QUICK TAG")
    
if SMO_RIZOMUV_LIVELINK_Status == False :
    lx.out("NOT LOADED : SMO RIZOMUV LIVELINK")
    
if SMO_UV_Status == False :
    lx.out("NOT LOADED : SMO UV")
    
if SMO_VENOM_Status == False :
    lx.out("NOT LOADED : SMO VENOM")

lx.out("A-AA-AAA----------------------AAA-AA-A")
    