// Color Modes To Text  
// ===================  
  
  
// Prints CMYK values, RGB values and HEX value of all selected swatches to a .txt file  
// The .txt file is saved with the same file name and inc the same folder as the .ai file  
// If the .ai file hasn't been saved, the .txt file is saved in the users home directory  
  
  
main();  
function main()  
{  
    var doc = app.activeDocument;  
    var selectedSwatches = doc.swatches.getSelected();  
  
  
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
  
  
            // CMYK Source  
            if (color.typename == "CMYKColor")  
            {  
                // CMYK Values  
                text += "C=" + Math.round(color.cyan) + " M=" + Math.round(color.magenta) + " Y=" + Math.round(color.yellow) + " K=" + Math.round(color.black) + "\n";  
  
  
                // RGB Values  
                var rgb = convertColor("CMYK", "RGB", [Math.round(color.cyan), Math.round(color.magenta), Math.round(color.yellow), Math.round(color.black)]);  
                text += "R=" + Math.floor(rgb[0]) + " G=" + Math.floor(rgb[1]) + " B=" + Math.floor(rgb[2]) + "\n";  
  
  
                // HEX Values  
                text += rgbToHex(Math.floor(rgb[0]), Math.floor(rgb[1]), Math.floor(rgb[2])) + "\n";  
                text += "\n";  
            }  
            // RGB Source  
            else if (color.typename == "RGBColor")  
            {  
                // CMYK Values  
                var cmyk = convertColor("RGB", "CMYK", [Math.round(color.red), Math.round(color.green), Math.round(color.blue)]);  
                text += "C=" + Math.round(cmyk[0]) + " M=" + Math.round(cmyk[1]) + " Y=" + Math.round(cmyk[2]) + " K=" + Math.round(cmyk[3]) + "\n";  
  
  
                // RGB Values  
                text += "R=" + Math.floor(color.red) + " G=" + Math.floor(color.green) + " B=" + Math.floor(color.blue) + "\n";  
  
  
                // HEX Values  
                text += rgbToHex(Math.floor(color.red), Math.floor(color.green), Math.floor(color.blue)) + "\n";  
                text += "\n";  
            }  
        }  
        saveTxt(text);  
    }  
    else {  
        alert("No Swatches Selected.");  
    }  
}  
  
  
function convertColor(src, dest, clrArr)  
{  
    return app.convertSampleColor(ImageColorSpace[src], clrArr, ImageColorSpace[dest], ColorConvertPurpose.defaultpurpose);  
}  
  
  
function componentToHex(c)  
{  
    var hex = c.toString(16);  
    return hex.length == 1 ? "0" + hex : hex;  
}  
  
  
function rgbToHex(r, g, b)  
{  
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);  
}  
  
  
function saveTxt(txt)  
{  
    var name = app.activeDocument.name.replace(/\.[^\.]+$/, '');  
    var path = (app.activeDocument.path != "") ? app.activeDocument.path : "~";  
  
  
    var saveFile = new File(path + "/" + name + ".txt");  
  
  
    if(saveFile.exists)  
        saveFile.remove();  
  
  
    saveFile.encoding = "UTF8";  
    saveFile.open("e", "TEXT");  
    saveFile.writeln(txt);  
    saveFile.close();  
  
  
    alert("Saved to File:\n" + saveFile.fullName)  
}  