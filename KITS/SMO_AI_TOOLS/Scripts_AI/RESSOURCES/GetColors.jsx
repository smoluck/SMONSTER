with (app.activeDocument) {
    if (pathItems.length > 0)
    {
        alert(pathItems.length);
        for (var g = 0 ; g < pathItems.length; g++)
          {
               if (pathItems[g].filled == true)
               {
                   if (pathItems[g].fillColor.red > 200 == true && pathItems[g].fillColor.red < 210 == true && pathItems[g].fillColor.green > 200 == true && pathItems[g].fillColor.green < 210 == true && pathItems[g].fillColor.blue > 200 == true && pathItems[g].fillColor.blue < 210 == true)
                       {
                        alert('R' + pathItems[g].fillColor.red + ' G' + pathItems[g].fillColor.green + ' B' + pathItems[g].fillColor.blue);
                        }
               }
          }
      }
} 