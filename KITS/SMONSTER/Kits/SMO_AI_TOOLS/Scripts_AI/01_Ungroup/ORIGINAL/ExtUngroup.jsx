﻿// ExtUngroup.jsx for Adobe Illustrator
// Description: This script with UI is сan be easily custom ungrouping to all group items, releasing clipping masks in the document.
// Requirements: Adobe Illustrator CS/CC
// Author: Sergey Osokin (hi@sergosokin.ru), 2018
// Based on 'ungroupV1.js' script by Jiwoong Song (netbluew@nate.com), 2009 & modification by John Wundes (wundes.com), 2012
// ============================================================================
// Installation:
// 1. Place script in:
//  Win (32 bit): C:\Program Files (x86)\Adobe\Adobe Illustrator [vers.]\Presets\en_GB\Scripts\
//  Win (64 bit): C:\Program Files\Adobe\Adobe Illustrator [vers.] (64 Bit)\Presets\en_GB\Scripts\
//  Mac OS: <hard drive>/Applications/Adobe Illustrator [vers.]/Presets.localized/en_GB/Scripts
// 2. Restart Illustrator
// 3. Choose File > Scripts > ExtUngroup
// ============================================================================
// Donate (optional): If you find this script helpful and want to support me 
// by shouting me a cup of coffee, you can by via PayPal http://www.paypal.me/osokin/usd
// ============================================================================
// THIS SOFTWARE IS PROVIDED ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, 
// INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
// AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
// THE FOUNDATION OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
// PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; 
// OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
// IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED 
// OF THE POSSIBILITY OF SUCH DAMAGE.
// ============================================================================
// Versions:
//  1.0 Initial version
//  1.1 Added option to delete / save mask objects. Fixed a performance issue.
//  1.2 Fixed ungrouping of the selected group inside another.
// ============================================================================
// Released under the MIT license.
// http://opensource.org/licenses/mit-license.php
// ============================================================================
// Check other author's scripts: https://github.com/creold

#target illustrator

// Global variables
var scriptName = 'ExtUngroup',
    scriptVersion = '1.2',
    scriptAuthor = '\u00A9 Sergey Osokin, 2019',
    scriptDonate = 'Donate via PayPal';
var doc = app.activeDocument;

if (app.documents.length > 0) {
  try {
    var currLayer = doc.activeLayer,
        boardNum = doc.artboards.getActiveArtboardIndex() + 1,
        clearArr = [], // Array of Clipping Masks obj
        margins = [10, 20, 10, 20];

    // Create Main Window
    var win = new Window('dialog', scriptName + ' ver.' + scriptVersion, undefined);
    win.orientation = 'column';
    win.alignChildren = ['fill', 'fill'];

    // Target radiobutton
    var slctTarget = win.add('panel', undefined, 'Target');
    slctTarget.alignChildren = 'left';
    slctTarget.margins = margins;
    if (getSelection(doc).length > 0) {
      var currSelRadio = slctTarget.add('radiobutton', undefined, 'Selected objects');
    }
    if (!currLayer.locked && currLayer.visible) {
      var currLayerRadio = slctTarget.add('radiobutton', undefined, 'Active Layer "' + currLayer.name + '"');
      currLayerRadio.value = true;
    }
    var currBoardRadio = slctTarget.add('radiobutton', undefined, 'Artboard No.' + boardNum);
    var currDocRadio = slctTarget.add('radiobutton', undefined, 'All Document');
    if (getSelection(doc).length > 0) {
      currSelRadio.value = true;
    } else if (typeof (currLayerRadio) == 'undefined') {
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
    var donate = copyright.add('button', undefined, scriptDonate);

    if (doc.groupItems.length > 0) {
      win.show();
    } else { 
      alert(scriptName + '\nDocument does not contain any groups.'); 
    }

    // Buttons click 
    donate.onClick = function () {
      var fname, shortcut;
      fname = '_aiscript_donate.url';
      shortcut = new File('' + Folder.temp + '/' + fname);
      shortcut.open('w');
      shortcut.writeln('[InternetShortcut]');
      shortcut.writeln('URL=http://www.paypal.me/osokin/usd');
      shortcut.writeln();
      shortcut.close();
      shortcut.execute();
      $.sleep(4000);
      return shortcut.remove();
    }

    cancel.onClick = function () {
      win.close();
    }

    function okClick() {
      // Ungroup selected objects
      if (typeof (currSelRadio) !== 'undefined' && currSelRadio.value) {
        var currSel = getSelection(doc);
        for (var i = 0; i < currSel.length; i++) {
          if (currSel[i].typename === 'GroupItem') ungroup(currSel[i]);
        }
      }
      // Ungroup in active Layer if it contains groups
      if (typeof (currLayerRadio) !== 'undefined' && currLayerRadio.value) {
        ungroup(currLayer);
      }
      // Ungroup in active Artboard only visible & unlocked objects
      if (currBoardRadio.value) {
        doc.selectObjectsOnActiveArtboard();
        ungroup(getSelection(doc));
        doc.selection = null;
      }
      // Ungroup all in the current Document
      if (currDocRadio.value) {
        for (var j = 0; j < doc.layers.length; j++) {
          var docLayer = doc.layers[j];
          // Run only for editable visible layers
          if (!docLayer.locked && docLayer.visible && docLayer.groupItems.length > 0) {
            ungroup(docLayer);
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
  alert(scriptName + '\nPlease open a document before running this script.');
}

function getSelection(doc) {
  return doc.selection;
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