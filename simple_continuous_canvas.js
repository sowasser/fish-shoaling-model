var ContinuousVisualization = function(height, width, context) {
    var height = height;
    var width = width;
    var context = context;

    this.draw = function (objects) {
        for (var i in objects) {
            var p = objects[i];
            if (p.Shape == "rect")
                this.drawRectangle(p.x, p.y, p.w, p.h, p.Color, p.Filled);
            if (p.Shape == "circle")
                this.drawCircle(p.x, p.y, p.r, p.Color, p.Filled);
            if (p.Shape == "triangle")
                this.drawTriangle(p.x, p.y, p.w, p.h, p.heading, p.Color, p.Filled);
        }
    };

    this.drawCircle = function (x, y, radius, color, fill) {
        var cx = x * width;
        var cy = y * height;
        var r = radius;

        context.beginPath();
        context.arc(cx, cy, r, 0, Math.PI * 2, false);
        context.closePath();

        context.strokeStyle = color;
        context.stroke();

        if (fill) {
            context.fillStyle = color;
            context.fill();
        }

    };

    this.drawRectangle = function (x, y, w, h, color, fill) {
        context.beginPath();
        var dx = w * width;
        var dy = h * height;

        // Keep the drawing centered:
        var x0 = (x * width) - 0.5 * dx;
        var y0 = (y * height) - 0.5 * dy;

        context.strokeStyle = color;
        context.fillStyle = color;

        if (fill)
            context.fillRect(x0, y0, dx, dy);
        else
            context.strokeRect(x0, y0, dx, dy);
    };

    this.drawTriangle = function (x, y, w, h, heading, color, fill) {
        // Increase the width by a bit so it's relatively consistent in size
        // of a circle of radians of 3. The value 3 here below is just arbitrary
        w = w * 3;
        h = h * 3;

        let dx = x * width;
        let dy = y * height;

        // Todo: keep the drawing centered, like in drawRectangle()
        // Todo: provide a heading with radians, rotate

        context.save();
        context.translate(dx, dy);
        context.rotate(heading);

        context.beginPath();
        context.moveTo(dx + w,          dy + h);    // 100, 100
        context.lineTo(dx + (w*1.5),    dy - h);        // 150, 0
        context.lineTo(dx + (w*2),      dy + h);    // 200, 100
        context.closePath();

        context.fillStyle = color;
        context.strokeStyle = color;

        if (fill) {
            context.fill();
        } else {
            context.stroke();
        }

        context.restore();

        //console.log(`triangle, x: ${x}, y: ${y}, dx: ${dx}, dy: ${dy}`); // Debug
    };

    this.resetCanvas = function () {
        context.clearRect(0, 0, height, width);
        context.beginPath();
    };
};

var Simple_Continuous_Module = function (canvas_width, canvas_height) {
    // Create the element
    // ------------------

    // Create the tag:
    var canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "style='border:1px dotted'></canvas>";

    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("body").append(canvas);

    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");
    var canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

    this.render = function (data) {
        canvasDraw.resetCanvas();
        canvasDraw.draw(data);
    };

    this.reset = function () {
        canvasDraw.resetCanvas();
    };
};