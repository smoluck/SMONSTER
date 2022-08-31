//				--> Original Script by Sergey Osokin <--
//	
//	 Script based on:
//                      SMO_AI_TOOLS/Scripts_AI/01_Ungroup/ORIGINAL/ExtUngroup.jsx
//                      SMO_AI_TOOLS/Scripts_AI/03_Export_AI_Paths_to_MODO/ORIGINAL/Export-selection-as-AI.jsx
//	
//	I've changed the UI Layout as well as the Output file to Modo compatible AI 8.0
//	This script is not intend to grab all the glory from Sergey Osokin work.
//	He made a great work to do those scripts.
//	
//	SMO AI Kit couldn't be done without is awesome work.
//	I encourage my followers to take a look at his GitHub page and donate to him.
//													https://github.com/creold
//	#---------------------------------------
//	# Name:			SMO_Pipeline_Complete.jsx
//	# Version:		1.0
//	#
//	# Purpose:  This script is designed to:
//	#           Ungroup all the path in the current document,
//	#           and export all the path to separate AI File (v8.0) compatible with MODO
//	#
//	# Author:		Franck ELISABETH
//	# Website:		http://www.smoluck.com
//	#
//	# Created:		13/01/2020
//	# Copyright:	(c) Franck ELISABETH 2020
//	#---------------------------------------

//@target illustrator
app.preferences.setBooleanPreference('ShowExternalJSXWarning', false); // Fix drag and drop a .jsx file

// Default variables for dialog box
var scriptName = 'SMO Pipeline --> AI to MODO',
    scriptVersion = '0.90',
    scriptAuthor = ' \u00A9 Franck Elisabeth, 2020';

var ActiveDoc = app.activeDocument,
    sel = ActiveDoc.selection;

var fileName = 'Mesh',
    fileAI_Ext = '.ai',
    separator = '_',
    outFolder = Folder.desktop;


// -------------------------
// Function                 Get Document Selection
// -------------------------
function getSelection(ActiveDoc) {
    return ActiveDoc.selection;
}


// -------------------------
// Function                 Create the Dialog Window
// -------------------------
function MainUI() {
    try {
      var CurLayer = ActiveDoc.activeLayer,
          BoardIndex = ActiveDoc.artboards.getActiveArtboardIndex() + 1,
          clearArr = [], // Array of Clipping Masks obj
          margins = [10, 20, 10, 20];
      
      
      
      //###################################################
      //-BLOCK--------------- WINDOW TITLE
      //###################################################
      var win = new Window('dialog', scriptName + 'beta' + scriptVersion + ' ' + scriptAuthor, undefined);
      win.orientation = 'column';
      win.alignChildren = ['fill', 'fill'];
      
      
      
      //###################################################
      //-BLOCK--------------- Ungroup Options
      //###################################################
      // Ungroup Target via Radio Button (only one possible selection)
      var slctTarget = win.add('panel', undefined, 'Target');
      slctTarget.alignChildren = 'left';
      slctTarget.margins = margins;
      if (getSelection(ActiveDoc).length > 0) {
        var currSelRadio = slctTarget.add('radiobutton', undefined, 'Selected objects');                        // RADIO BUTTON - Selected objects
      }
      if (!CurLayer.locked && CurLayer.visible) {
        var CurLayerRadio = slctTarget.add('radiobutton', undefined, 'Active Layer "' + CurLayer.name + '"');   // RADIO BUTTON - Active Layer
        CurLayerRadio.value = true;
      }
      var currBoardRadio = slctTarget.add('radiobutton', undefined, 'Artboard No.' + BoardIndex);               // RADIO BUTTON - Artboard No.
      var currDocRadio = slctTarget.add('radiobutton', undefined, 'All Document');                              // RADIO BUTTON - All Document
          currDocRadio.value = true;
      if (getSelection(ActiveDoc).length > 0) {
          currSelRadio.value = true;
      } else if (typeof (CurLayerRadio) == 'undefined') {
          currBoardRadio.value = true;
      }
      
      
      // Checkbox
      var UngroupOptions = win.add('panel', undefined, 'Options');                                              // PANEL - Ungroup Options
          UngroupOptions.alignChildren = 'left';
          UngroupOptions.margins = margins;
      var CHECKBOXUnroup = UngroupOptions.add('checkbox', undefined, 'Ungroup All');                            // CHECKBOX - Ungroup All
          // Default State
          CHECKBOXUnroup.value = true;
      var CHECKBOXClipping = UngroupOptions.add('checkbox', undefined, 'Release Clipping Masks');               // CHECKBOX - Release Clipping Masks
          CHECKBOXClipping.value = true;
      var CHECKBOXRemoveClipping = UngroupOptions.add('checkbox', undefined, 'Remove Masks Shapes');            // CHECKBOX - Remove Masks Shapes
          CHECKBOXRemoveClipping.enabled = false;
      
      
      // Show/hide checkbox 'Remove Masks Shapes'
      CHECKBOXClipping.onClick = function () {
        CHECKBOXRemoveClipping.enabled = !CHECKBOXRemoveClipping.enabled;
      }
      
      
      
      //###################################################
      //-BLOCK--------------- Export to separate AI Options
      //###################################################
      //---------Destination Folder (Output)
      var OutputOptionsFolders = win.add('panel', undefined, 'Output folder');                                  // PANEL - Output folder
          OutputOptionsFolders.orientation = 'row';
      var SCBtnsOutFolder = OutputOptionsFolders.add('button', undefined, 'Select');                            // BUTTON - Select
      var LABELOutFolder = OutputOptionsFolders.add('edittext', undefined);
          LABELOutFolder.text = decodeURI(outFolder);
          LABELOutFolder.characters = 30;
          
      //---Group-------------------- FileName (Output)
      //----------------------------- FileName
      var OutputFileNameGrp = win.add('group');                                                                 // GROUP - Output FileName
      var FileNamePANEL = OutputFileNameGrp.add('panel', undefined, 'File name prefix');                        // PANEL - File Name Prefix
          FileNamePANEL.orientation = 'row';
      var FileNamePrefix = FileNamePANEL.add('edittext', undefined, fileName);
          FileNamePrefix.characters = 30;
      //----------------------------- Separator
      var SeparatorPANEL = OutputFileNameGrp.add('panel', undefined, 'Separator');                              // SEPARATOR
      var symbol = SeparatorPANEL.add('edittext', undefined, separator);
          symbol.characters = 4;
          symbol.enabled = false;
      
      //---Group-------------------- Options
      var OutputOptionsGrp = win.add('group');                                                                  // GROUP - Output Options
      var OutputOptionsPanel = OutputOptionsGrp.add('panel', undefined, 'Options');                             // PANEL - Export Options
          OutputOptionsPanel.orientation = 'column';
          OutputOptionsPanel.alignChildren = 'left';
      //----------------------------- Save to Separate Files
      var separateCHECKBOX = OutputOptionsPanel.add('checkbox', undefined, 'Save to separate files');           // CHECKBOX - Save to separate files
      //----------------------------- Crop To Curve
      var fitBoardCHECKBOX = OutputOptionsPanel.add('checkbox', undefined, 'Crop to Curve');                    // CHECKBOX - Crop to Curve
          // Default State
          separateCHECKBOX.value = true;
          fitBoardCHECKBOX.value = false;
      
      
      //#################################################
      //-BLOCK--------------- Script Choice Buttons Group
      //#################################################
      var SCBtnsGroup = win.add('group');                                                                       // GROUP - Script Choice
          SCBtnsGroup.alignChildren = ['fill', 'fill'];
          SCBtnsGroup.margins = [0, 10, 0, 0];
      var SCBtnsCancel = SCBtnsGroup.add('button', undefined, 'Cancel', { name: 'cancel' });                    // BUTTON - Cancel
          SCBtnsCancel.helpTip = 'Press Esc to Close';
      var SCBtnsExport = SCBtnsGroup.add('button', undefined, 'Export', { name: 'export' });                                // BUTTON - Ok
          SCBtnsExport.helpTip = 'Press Enter to Run';
          SCBtnsExport.onClick = okClick;
      
      
      //----------------------- Progress Bar
      win.prgPANEL = win.add('panel', undefined, 'Progress');                                                   // PANEL PROGRESS
      win.prgPANEL.progBar = win.prgPANEL.add('progressbar', [20, 15, 276, 40], 0, 100);                        // PROGRESS BAR
      
      
      //###############################
      //-BLOCK--------------- Copyright
      //###############################
      var copyright = win.add('panel');                                                                         // PANEL - Copyright
          copyright.orientation = 'column';
          copyright.alignChild = ['center', 'center'];
          copyright.alignment = 'fill';
          copyright.margins = margins / 4;
      var LABELCopyright = copyright.add('statictext');
          LABELCopyright.text = scriptAuthor;
      
      
      //#############################
      //-BLOCK--------------- OnClick
      //#############################
      separateCHECKBOX.onClick = function () {
      symbol.enabled = !symbol.enabled;
      }
      
      SCBtnsOutFolder.onClick = function () {
      var userFolder = Folder.selectDialog('Select a folder to export');
      if (userFolder != null) {
        LABELOutFolder.text = decodeURI(userFolder);
        outFolder = userFolder;
        }
      }
      
      
      SCBtnsExport.onClick = function () {
      var colorSpace = ActiveDoc.documentColorSpace;
      
      if (!isEmpty(FileNamePrefix.text)) {
        fileName = FileNamePrefix.text.trim();
      } else {
        alert('Please enter file name prefix');
        return;
      }
      
      if (separateCHECKBOX.value) {
      if (symbol.text != '') {
        separator = symbol.text;
        }
        fileName = fileName + separator;
      
        for (var i = 0; i < sel.length; i++) {
          win.prgPANEL.progBar.value = i*(100.0/(sel.length-1)); // Change progress bar
          var element = sel[i];
          var myFile = File(outFolder + '/' + fileName + i + fileAI_Ext);
          saveSelection(element, myFile, colorSpace, fitBoardCHECKBOX.value, separateCHECKBOX.value);
        }
      } else {
        var myFile = File(outFolder + '/' + fileName + fileAI_Ext);
        saveSelection(sel, myFile, colorSpace, fitBoardCHECKBOX.value, separateCHECKBOX.value);
      }
      win.close();
      }
      
      win.center();
      win.show();
      
      
      
      if (ActiveDoc.groupItems.length > 0) {
          win.show();
      } else { 
          alert(scriptName + '\nDocument does not contain any groups.'); 
      }
      
      SCBtnsCancel.onClick = function () {
        win.close();
      }
    } catch (e) {
      // showError(e);
    }
};



// -------------------------
// Function                 Ungroup
// -------------------------
function Ungroup() {
  // If a Document is currently open
  if (app.Documents.length > 0) {
    function okClick() {
      // Ungroup selected objects
      if (typeof (currSelRadio) !== 'undefined' && currSelRadio.value) {
        var currSel = getSelection(ActiveDoc);
        for (var i = 0; i < currSel.length; i++) {
          if (currSel[i].typename === 'GroupItem') ungroup(currSel[i]);
        }
      }
      // Ungroup in active Layer if it contains groups
      if (typeof (CurLayerRadio) !== 'undefined' && CurLayerRadio.value) {
          ungroup(CurLayer);
      }
      // Ungroup in active Artboard only visible & unlocked objects
      if (currBoardRadio.value) {
          ActiveDoc.selectObjectsOnActiveArtboard();
          ungroup(getSelection(ActiveDoc));
          ActiveDoc.selection = null;
      }
      // Ungroup all in the current Document
      if (currDocRadio.value) {
        for (var j = 0; j < ActiveDoc.layers.length; j++) {
          var DocLayer = ActiveDoc.layers[j];
            // Run only for editable visible layers
              if (!DocLayer.locked && DocLayer.visible && DocLayer.groupItems.length > 0) {
                  ungroup(DocLayer);
              }
          }
      }
          // Remove empty clipping masks after ungroup
      if (CHECKBOXRemoveClipping.value) {
          removeMasks(clearArr);
      }
    win.close();
    }
  }
}



// -------------------------
// Function                 Get All Child
// -------------------------
function getChildAll(obj) {
    var AllChildsArray = [];
    if (Object.prototype.toString.call(obj) === '[object Array]') {
        AllChildsArray.push.apply(AllChildsArray, obj);
    } else {
        for (var i = 0; i < obj.pageItems.length; i++) {
            AllChildsArray.push(obj.pageItems[i]);
        }
    }
    if (obj.layers) {
        for (var l = 0; l < obj.layers.length; l++) {
            AllChildsArray.push(obj.layers[l]);
        }
    }
    return AllChildsArray;
}



// -------------------------
// Function                 Ungroup array of target objects
// -------------------------
function ungroup(obj) {
    if (!CHECKBOXClipping.value && obj.clipped) { 
        return; 
    }
    
    var ChildArray = getChildAll(obj);
    
    if (ChildArray.length < 1) {
        obj.remove();
        return;
    }
    
    for (var i = 0; i < ChildArray.length; i++) {
      var element = ChildArray[i];
      try {
        if (element.parent.typename !== 'Layer') {
          element.move(obj, ElementPlacement.PLACEBEFORE);
          // Push empty paths in array 
          if ((element.typename === 'PathItem' && !element.filled && !element.stroked) ||
              (element.typename === 'CompoundPathItem' && !element.pathItems[0].filled && !element.pathItems[0].stroked))
              clearArr.push(element);
        }
        if (element.typename === 'GroupItem' || element.typename === 'Layer') {
            ungroup(element);
        }
      } catch (e) { }
    }
}



// -------------------------
// Function                 Remove empty clipping masks after ungroup
// -------------------------
function removeMasks(arr) {
    for (var i = 0; i < arr.length; i++) {
        arr[i].remove();
    }
}



// -------------------------
// Function                 Show Error
// -------------------------
function showError(err) {
  if (confirm(scriptName + ': an unknown error has occurred.\n' + 'Would you like to see more information?', true, 'Unknown Error')) {
      alert(err + ': on line ' + err.line, 'Script Error', true);
  }
}


try {
  if (app.documents.length > 0) {
      getChildAll(obj);
  } else {
    alert('There are no documents open.');
  }
} catch (e) { }



// -------------------------
// Function                 Check empty string
// -------------------------
function isEmpty(str) {
    return str.replace(/\s/g, '').length == 0;
}



// -------------------------
// Function                 Remove whitespaces from start and end of string
// -------------------------
String.prototype.trim = function () {
    return this.replace(/^\s+|\s+$/g, '');
}



// -------------------------
// Function                 Copy selection to a new document, and save it as an AI file
// -------------------------
function saveSelection(objects, file, color, fitArtboard, separate) {
  var doc = app.documents.add(color);
  app.coordinateSystem = CoordinateSystem.ARTBOARDCOORDINATESYSTEM;
  
  copyObjectsTo(objects, doc, separate);
  
  // Resize the artboard to the object
  if (fitArtboard) {
    app.executeMenuCommand('selectall');
    doc.artboards[0].artboardRect = doc.visibleBounds;
  }
  
  // Save as AI in compatibility mode = v 8.0 to be loaded in Modo
  try {
    var saveOptions = new IllustratorSaveOptions();
    saveOptions.compatibility = Compatibility.ILLUSTRATOR8;
    doc.saveAs(file, saveOptions);
    doc.close();
  } catch (e) { }
}



// -------------------------
// Function                 Duplicate objects and add them to a document
// -------------------------
function copyObjectsTo(objects, doc, separate) {
  if (separate) {
    objects.duplicate(doc.activeLayer, ElementPlacement.PLACEATBEGINNING);
  } else {
    for (var i = 0; i < objects.length; i++) {
      objects[i].duplicate(doc.activeLayer, ElementPlacement.PLACEATBEGINNING);
    }
  }
}



// -------------------------
// Function                 Start Script
// -------------------------
try {
    if (app.documents.length > 0) {
      MainUI();
    } else {
      alert('There are no documents open.');
    }
} catch (e) { }