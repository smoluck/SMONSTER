// Color Modes To Text  
// ===================  
  
  
// Prints RGB values (0 to 1 range) of all selected swatches to a .lxc file  
// The .lxc file is saved with the same file name and in the same folder as the .ai file  
// If the .ai file hasn't been saved, the .lxc file is saved in the users home directory  
  
#target illustrator

converter();
function converter()
{  
    var doc = app.activeDocument;  
    var selectedSwatches = doc.swatches.getSelected();  
    var bit8 = 255
  
    if (selectedSwatches.length > 0)  
    {  
        var text = "";  
  
  
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
  
  
function convertColor(src, dest, clrArr)  
{  
    return app.convertSampleColor(ImageColorSpace[src], clrArr, ImageColorSpace[dest], ColorConvertPurpose.defaultpurpose);  
}  
  
  
function savelxc(lxc)  
{  
    var name = app.activeDocument.name.replace(/\.[^\.]+$/, '');  
    var path = (app.activeDocument.path != "") ? app.activeDocument.path : "~";  
  
  
    var saveFile = new File(path + "/" + name + ".lxc");  
  
  
    if(saveFile.exists)  
        saveFile.remove();  
  
  
    saveFile.encoding = "UTF8";  
    saveFile.open("e", "TEXT");  
    saveFile.writeln(lxc);  
    saveFile.close();  
  
  
    alert("Saved to File:\n" + saveFile.fullName)  
}  