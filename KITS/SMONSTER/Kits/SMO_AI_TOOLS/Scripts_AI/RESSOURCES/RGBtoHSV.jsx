function rgbToHsv(r, g, b)

{

    r = r/255;

    g = g/255;

    b = b/255;

       

    var max = Math.max(r, g, b);

    var min = Math.min(r, g, b);

    var h, v = max;

   

    var d = max - min;

    var s = (max == 0) ? 0 : d / max;

   

    if(max == min){

        h = 0;

    }else{

        switch(max){

            case r: h = (g - b) / d + ((g < b) ? 6 : 0); break;

            case g: h = (b - r) / d + 2; break;

            case b: h = (r - g) / d + 4; break;

        }

        h = h / 6;

    }

       

    h = Math.round (h*360 * 100) / 100;

    s = Math.round(s*100 * 100) / 100;

    v = Math.round(v*100 * 100) / 100;

       

    return (h + ' - ' + s  + ' - ' + v)

}

//  Here's are RGB values for testing

alert ( rgbToHsv(120, 50, 70) + '\n' +

          rgbToHsv(50, 60, 70) + '\n' +

//  shows difference between H1 and H2

       ( rgbToHsv(120, 50, 70) - rgbToHsv(50, 60, 70) ) );