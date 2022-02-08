// DISCLAIMER:
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
//		Export-selection-as-AI.jsx for Adobe Illustrator
//		Description: Exports all selected objects to AI files
//		Date: February, 2019
//		Author: Sergey Osokin, email: hi@sergosokin.ru
//		Based on Layers to SVG 0.1 by Anton Ball
//		==========================================================================================
//		Installation:
//		1. Place script in:
//		    Win (32 bit): C:\Program Files (x86)\Adobe\Adobe Illustrator [vers.]\Presets\en_GB\Scripts\
//		    Win (64 bit): C:\Program Files\Adobe\Adobe Illustrator [vers.] (64 Bit)\Presets\en_GB\Scripts\
//		    Mac OS: <hard drive>/Applications/Adobe Illustrator [vers.]/Presets.localized/en_GB/Scripts
//		2. Restart Illustrator
//		3. Choose File > Scripts > Export-selection-as-AI
// 		============================================================================
// 		Donate (optional): If you find this script helpful and want to support me 
// 		by shouting me a cup of coffee, you can by via PayPal http://www.paypal.me/osokin/usd
// 		==========================================================================================
// 		NOTICE:
// 		Tested with Adobe Illustrator CC 2018 (Mac/Win), CC 2019 (Win).
// 		This script is provided "as is" without warranty of any kind.
// 		Free to use, not for sale.
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

#target illustrator

var scriptName = 'Export current Layers to individual AI 8 files',
    copyright = ' \u00A9 Smoluck & Sergey Osokin';

// Main function
function main() {
	// Default variables for dialog box
	var fileName = 'Mesh',
		fileExt = '.ai',
		separator = '_',
		outFolder = Folder.desktop;

	var sel = app.activeDocument.selection;

	if (sel.length < 1) {
		alert('Please select a path or group to export.');
		return;
	}

	// Create dialog box
	//----------------------- Dialog Title
	var win = new Window('dialog', scriptName + ' ' + copyright);
		win.alignChildren = 'center';
	//----------------------- Destination (Output) Folder
	var outPnl = win.add('panel', undefined, 'Output folder');
		outPnl.orientation = 'row';
	var btnOutFolder = outPnl.add('button', undefined, 'Select');
	var lblOutFolder = outPnl.add('edittext', undefined);
		lblOutFolder.text = decodeURI(outFolder);
		lblOutFolder.characters = 30;
	//---Group-------------------- FileName (Output)
	//----------------------------- FileName
	var fileNameGrp = win.add('group');
	var namePnl = fileNameGrp.add('panel', undefined, 'File name prefix');
		namePnl.orientation = 'row';
	var namePrefix = namePnl.add('edittext', undefined, fileName);
		namePrefix.characters = 30;
	//----------------------------- Separator
	var separatorPnl = fileNameGrp.add('panel', undefined, 'Separator');
	var symbol = separatorPnl.add('edittext', undefined, separator);
		symbol.characters = 4;
		symbol.enabled = false;
	//----------------------- Progress Bar
	win.prgPnl = win.add('panel', undefined, 'Progress');
	win.prgPnl.progBar = win.prgPnl.add('progressbar', [20, 15, 276, 40], 0, 100);
	//---Group-------------------- Options
	var optionGrp = win.add('group');
	var optionPnl = optionGrp.add('panel', undefined, 'Options');
		optionPnl.orientation = 'column';
		optionPnl.alignChildren = 'left';
	//----------------------------- Save to Separate Files
	var separateChk = optionPnl.add('checkbox', undefined, 'Save to separate files');
	//----------------------------- Crop To Curve
	var fitBoardChk = optionPnl.add('checkbox', undefined, 'Crop to Curve');
		separateChk.value = true;
		fitBoardChk.value = false;

	//----------------------- Script Choice
	var btnGroup = win.add('group');
	var btnCancel = btnGroup.add('button', undefined, 'Cancel', { name: 'btnCancel' });
	var btnExport = btnGroup.add('button', undefined, 'Export', { name: 'ok' });

	// Click functions
	separateChk.onClick = function () {
	symbol.enabled = !symbol.enabled;
	}

	btnOutFolder.onClick = function () {
	var userFolder = Folder.selectDialog('Select a folder to export');
	if (userFolder != null) {
		lblOutFolder.text = decodeURI(userFolder);
		outFolder = userFolder;
		}
	}

	btnCancel.onClick = function () {
	win.close();
	}

	btnExport.onClick = function () {
	var colorSpace = app.activeDocument.documentColorSpace;

	if (!isEmpty(namePrefix.text)) {
		fileName = namePrefix.text.trim();
	} else {
		alert('Please enter file name prefix');
		return;
	}

	if (separateChk.value) {
	if (symbol.text != '') {
		separator = symbol.text;
		}
		fileName = fileName + separator;

		for (var i = 0; i < sel.length; i++) {
			win.prgPnl.progBar.value = i*(100.0/(sel.length-1)); // Change progress bar
			var element = sel[i];
			var myFile = File(outFolder + '/' + fileName + i + fileExt);
			saveSelection(element, myFile, colorSpace, fitBoardChk.value, separateChk.value);
		}
	} else {
		var myFile = File(outFolder + '/' + fileName + fileExt);
		saveSelection(sel, myFile, colorSpace, fitBoardChk.value, separateChk.value);
	}
	win.close();
	}

	win.center();
	win.show();
};

// Check empty string
function isEmpty(str) {
	return str.replace(/\s/g, '').length == 0;
}

// Remove whitespaces from start and end of string
String.prototype.trim = function () {
	return this.replace(/^\s+|\s+$/g, '');
};


// Copy selection to a new document, and save it as an AI file
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

// Duplicate objects and add them to a document
function copyObjectsTo(objects, doc, separate) {
	if (separate) {
			objects.duplicate(doc.activeLayer, ElementPlacement.PLACEATBEGINNING);
		} else {
			for (var i = 0; i < objects.length; i++) {
				objects[i].duplicate(doc.activeLayer, ElementPlacement.PLACEATBEGINNING);
			}
		}
	}

try {
	if (app.documents.length > 0) {
		main();
	} else {
		alert('There are no documents open.');
	}
} catch (e) { }