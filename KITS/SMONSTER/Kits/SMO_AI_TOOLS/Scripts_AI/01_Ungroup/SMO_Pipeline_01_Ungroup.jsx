﻿ // DISCLAIMER:
//				--> Original Script by Sergey Osokin <--
//	
// 	I've changed the UI Layout as well as the Output file to Modo compatible AI 8.0
//	This script is not intend to grab all the glory from Sergey Osokin work.
//	He made a great work to do those scripts.
// 
//	SMO AI Kit couldn't be done without is awesome work.
//	I encourage my followers to take a look at his GitHub page and donate to him.
//													https://github.com/creold
//	-------------------------------------------------------------------------------
// 
// ########################################################################################################
// Original DISCLAIMER:
// 		ExtUngroup.jsx for Adobe Illustrator
// 		Description: This script with UI is сan be easily custom ungrouping to all group items, releasing clipping masks in the Document.
// 		Requirements: Adobe Illustrator CS/CC
// 		Author: Sergey Osokin (hi@sergosokin.ru), 2018
// 		Based on 'ungroupV1.js' script by Jiwoong Song (netbluew@nate.com), 2009 & modification by John Wundes (wundes.com), 2012
// 		============================================================================
// 		Installation:
// 		1. Place script in:
// 		Win (32 bit): C:\Program Files (x86)\Adobe\Adobe Illustrator [vers.]\Presets\en_GB\Scripts\
// 		Win (64 bit): C:\Program Files\Adobe\Adobe Illustrator [vers.] (64 Bit)\Presets\en_GB\Scripts\
// 		Mac OS: <hard drive>/Applications/Adobe Illustrator [vers.]/Presets.localized/en_GB/Scripts
// 		2. Restart Illustrator
// 		3. Choose File > Scripts > ExtUngroup
// 		============================================================================
// 		Donate (optional): If you find this script helpful and want to support me 
// 		by shouting me a cup of coffee, you can by via PayPal http://www.paypal.me/osokin/usd
// 		============================================================================
// 		Versions:
// 		1.0 Initial version
// 		1.1 Added option to delete / save mask objects. Fixed a performance issue.
// 		 1.2 Fixed ungrouping of the selected group inside another.
// 		==========================================================================================
// 		THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
// 		INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
// 		AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// 		DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// 		OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// 		==========================================================================================
// 		Released under the MIT license.
// 		http://opensource.org/licenses/mit-license.php
// ########################################################################################################


//@target illustrator
app.preferences.setBooleanPreference('ShowExternalJSXWarning', false); // Fix drag and drop a .jsx file

// Global variables
var scriptName = 'SMO Ungroup',
    scriptVersion = '0.90',
    scriptAuthor = '\u00A9 Franck Elisabeth, 2020';
var Doc = app.activeDocument;


// If a Document is currently open
if (app.Documents.length > 0) {
  try {
    var CurLayer = Doc.activeLayer,
      BoardIndex = Doc.artboards.getActiveArtboardIndex() + 1,
      clearArr = [], // Array of Clipping Masks obj
      margins = [10, 20, 10, 20];


    // Create Main Window
    var win = new Window('dialog', scriptName + 'beta' + scriptVersion, undefined);
    win.orientation = 'column';
    win.alignChildren = ['fill', 'fill'];


    // Target radiobutton
    var slctTarget = win.add('panel', undefined, 'Target');
    slctTarget.alignChildren = 'left';
    slctTarget.margins = margins;
    if (getSelection(Doc).length > 0) {
      var currSelRadio = slctTarget.add('radiobutton', undefined, 'Selected objects');
    }
    if (!CurLayer.locked && CurLayer.visible) {
      var CurLayerRadio = slctTarget.add('radiobutton', undefined, 'Active Layer "' + CurLayer.name + '"');
      CurLayerRadio.value = true;
    }
    var currBoardRadio = slctTarget.add('radiobutton', undefined, 'Artboard No.' + BoardIndex);
    var currDocRadio = slctTarget.add('radiobutton', undefined, 'All Document');
    if (getSelection(Doc).length > 0) {
      currSelRadio.value = true;
    } else if (typeof (CurLayerRadio) == 'undefined') {
      currBoardRadio.value = true;
    }


    // Action checkbox
    var options = win.add('panel', undefined, 'Options');
    options.alignChildren = 'left';
    options.margins = margins;
    var chkUnroup = options.add('checkbox', undefined, 'Ungroup All');
    chkUnroup.value = true;
    var chkClipping = options.add('checkbox', undefined, 'Release Clipping Masks');
    var chkRmvClipping = options.add('checkbox', undefined, 'Remove Masks Shapes');
    chkRmvClipping.enabled = false;


    // Show/hide checkbox 'Remove Masks Shapes'
    chkClipping.onClick = function () {
      chkRmvClipping.enabled = !chkRmvClipping.enabled;
    }


    // Buttons
    var btns = win.add('group');
    btns.alignChildren = ['fill', 'fill'];
    btns.margins = [0, 10, 0, 0];
    var cancel = btns.add('button', undefined, 'Cancel', { name: 'cancel' });
    cancel.helpTip = 'Press Esc to Close';
    var ok = btns.add('button', undefined, 'OK', { name: 'ok' });
    ok.helpTip = 'Press Enter to Run';
    ok.onClick = okClick;


   // Copyright block
    var copyright = win.add('panel');
    copyright.orientation = 'column';
    copyright.alignChild = ['center', 'center'];
    copyright.alignment = 'fill';
    copyright.margins = margins / 4;
    var lblCopyright = copyright.add('statictext');
    lblCopyright.text = scriptAuthor;
	
    if (Doc.groupItems.length > 0) {
      win.show();
    } else { 
      alert(scriptName + '\nDocument does not contain any groups.'); 
    }
    
    cancel.onClick = function () {
      win.close();
    }


    function okClick() {
      // Ungroup selected objects
      if (typeof (currSelRadio) !== 'undefined' && currSelRadio.value) {
        var currSel = getSelection(Doc);
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
        Doc.selectObjectsOnActiveArtboard();
        ungroup(getSelection(Doc));
        Doc.selection = null;
      }
      // Ungroup all in the current Document
      if (currDocRadio.value) {
        for (var j = 0; j < Doc.layers.length; j++) {
          var DocLayer = Doc.layers[j];
          // Run only for editable visible layers
          if (!DocLayer.locked && DocLayer.visible && DocLayer.groupItems.length > 0) {
            ungroup(DocLayer);
          }
        }
      }
      // Remove empty clipping masks after ungroup
      if (chkRmvClipping.value) {
        removeMasks(clearArr);
      }
      win.close();
    }
  } catch (e) {
    // showError(e);
  }
} else {
  alert(scriptName + '\nPlease open a Document before running this script.');
}


function getSelection(Doc) {
  return Doc.selection;
}


function getChildAll(obj) {
  var childsArr = [];
  if (Object.prototype.toString.call(obj) === '[object Array]') {
    childsArr.push.apply(childsArr, obj);
  } else {
    for (var i = 0; i < obj.pageItems.length; i++) {
      childsArr.push(obj.pageItems[i]);
    }
  }
  if (obj.layers) {
    for (var l = 0; l < obj.layers.length; l++) {
      childsArr.push(obj.layers[l]);
    }
  }
  return childsArr;
}


// Ungroup array of target objects
function ungroup(obj) {
  if (!chkClipping.value && obj.clipped) { 
    return; 
  }

  var childArr = getChildAll(obj);

  if (childArr.length < 1) {
    obj.remove();
    return;
  }

  for (var i = 0; i < childArr.length; i++) {
    var element = childArr[i];
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


// Remove empty clipping masks after ungroup
function removeMasks(arr) {
  for (var i = 0; i < arr.length; i++) {
    arr[i].remove();
  }
}


function showError(err) {
  if (confirm(scriptName + ': an unknown error has occurred.\n' +
    'Would you like to see more information?', true, 'Unknown Error')) {
    alert(err + ': on line ' + err.line, 'Script Error', true);
  }
}