#python
#---------------------------------------
# Name:         SMO_3VariablesPrerequisite
# Version: 1.0
#
# Purpose: This script is designed to test if at Least 3 Polygons are selected
#
# Author:       Franck ELISABETH
# Website:      http://www.smoluck.com
#
# Created:      27/12/2018
# Copyright:    (c) Franck Elisabeth 2017-2022
#---------------------------------------

SMO_SafetyCheck_Only1MeshItemSelected = 0
lx.out('SafetyCheck1',SMO_SafetyCheck_Only1MeshItemSelected)

SMO_SafetyCheck_PolygonModeEnabled = 1
lx.out('SafetyCheck2',SMO_SafetyCheck_PolygonModeEnabled)

SMO_SafetyCheck_min3PolygonSelected = 1
lx.out('SafetyCheck3',SMO_SafetyCheck_min3PolygonSelected)

#Compare variables: Is SafetyCheck true ? 
mCompare1 = SMO_SafetyCheck_Only1MeshItemSelected == 1
mCompare2 = SMO_SafetyCheck_PolygonModeEnabled == 1
mCompare3 = SMO_SafetyCheck_min3PolygonSelected == 1

#Comparison Results
lx.out('SafetyCheck 1 status:', mCompare1)
lx.out('SafetyCheck 2 status:', mCompare2)
lx.out('SafetyCheck 3 status:', mCompare3)

TotalSafetyCheckTrueValue = 3
lx.out('Desired Value',TotalSafetyCheckTrueValue)
TotalSafetyCheck = (SMO_SafetyCheck_Only1MeshItemSelected + SMO_SafetyCheck_PolygonModeEnabled + SMO_SafetyCheck_min3PolygonSelected)
lx.out('Current Value',TotalSafetyCheck)


if TotalSafetyCheck == TotalSafetyCheckTrueValue:
	lx.out('good job')

elif TotalSafetyCheck != TotalSafetyCheckTrueValue:
	lx.out('script Stopped: your mesh does not match the requirement for that script.')
	sys.exit