// Color Modes To Text  
// ===================  
  
  
// Prints CMYK values, RGB values and HEX value of all selected swatches to a .lxc file  
// The .lxc file is saved with the same file name and inc the same folder as the .ai file  
// If the .ai file hasn't been saved, the .lxc file is saved in the users home directory  
  
//@target illustrator
app.preferences.setBooleanPreference('ShowExternalJSXWarning', false); // Fix drag and drop a .jsx file
  
var scriptName = 'Export current Color Swatch Group to LXC (Modo) file',
	copyright = ' \u00A9 Smoluck';

// Default variables for dialog box
var fileName = 'SwatchColor',
	fileExt = '.lxc',
	separator = '_',
	outFolder = Folder.desktop;

// Main function
main();
function main(){
	function PopUpWindow() {
		

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
			separateChk.value = true;

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
				var LXCFile = File(outFolder + '/' + fileName + i + fileExt);
				saveSelection(element, LXCFile, colorSpace, separateChk.value);
			}
		} else {
			var LXCFile = File(outFolder + '/' + fileName + fileExt);
			saveSelection(sel, LXCFile, colorSpace, separateChk.value);
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



	converter();
	function converter()
	{  
		var doc = app.activeDocument;  
		var selectedSwatches = doc.swatches.getSelected();  
		var bit8 = 256
	  
		if (selectedSwatches.length > 0)  
		{  
			var text[i] = "";  
	  
	  
			for (var i = 0; i < selectedSwatches.length; i++)  
			{  
				var swatch = selectedSwatches[i]  
				var color = swatch.color;  
	  
	  
				// Spot  
				if (color.typename == "SpotColor") {  
					text += color.spot.name + "\n";  
					color = color.spot.color;
				}  
	  
	  
				{  
					// LXC Tag  
					text += "#LXColor#" + "\n";  
				}  
				
				
				// CMYK Source  
				if (color.typename == "CMYKColor")  
				{  
					// RGB Values  
					var rgb = convertColor("CMYK", "RGB", [Math.round(color.cyan), Math.round(color.magenta), Math.round(color.yellow), Math.round(color.black)]);  
					text += "RGB" + " " + (Math.floor(rgb[0]) / bit8) + " " + (Math.floor(rgb[1]) / bit8) + " " + (Math.floor(rgb[2]) / bit8) + "\n";  
				}  
				
				
				// RGB Source  
				else if (color.typename == "RGBColor")  
				{  
					// RGB Values  
					text += "RGB" + " " + (Math.floor(color.red) / bit8) + " " + (Math.floor(color.green) / bit8) + " " + (Math.floor(color.blue) / bit8) + "\n";  
				}  
			}  
			savelxc(text);  
		}  
		else {  
			alert("No Swatches Selected.");  
		}  
	}  
	  


	function convertColor(src, dest, clrArr) {
		return app.convertSampleColor(ImageColorSpace[src], clrArr, ImageColorSpace[dest], ColorConvertPurpose.defaultpurpose);  
	}  



	function savelxc(text) {
		var element = sel[i];
		var LXCFile = new File(outFolder + '/' + fileName + i + fileExt);
	
		if(LXCFile.exists)  
			LXCFile.remove();  
	  
	  
		LXCFile.encoding = "UTF8";  
		LXCFile.open("e", "TEXT");  
		LXCFile.writeln(lxc);  
		LXCFile.close();  
	  
	  
		alert("Saved to File:\n" + LXCFile.fullName)  
	}
};	