/**
 * An HTML <canvas> element where the agents are drawn onto.
 *
 * @param height of the canvas
 * @param width of the canvas
 * @param context of the canvas
 */
let ContinuousVisualization = function(height, width, context) {
    this.draw = function (agents) {
        // Draw every agent in the appropriate shape
        agents.forEach(agent => {
            const a = agent; // a is just a short alias for agent so draw calls fit on one line

            if (agent.shape === "rect")
               this.drawRectangle(a.x, a.y, a.w, a.h, a.color, a.filled);
            if (agent.shape === "circle")
               this.drawCircle(a.x, a.y, a.r, a.color, a.filled);
            if (agent.shape === "triangle")
               this.drawTriangle(a.x, a.y, a.w, a.h, a.heading, a.color, a.filled);

            // Draw a circle around the agent to show the visual range it has
            if (agent.showVisionRange) {
                this.drawCircle(a.x, a.y, a.vision, false);
            }

            // Draw a line from the center of the agent to where it is heading
            if (agent.showHeadingVector) {
                this.drawHeadingArrow(a.x, a.y, a.headingX, a.headingY);
            }

            // Add agent ID above agents
            this.addText(agent.id, agent.x, agent.y);
        });
    };

    this.addText = function(text, x, y) {
        if (text !== undefined) {
            context.textAlign = "center";
            context.fillStyle = "red";
            context.fillText(text, x * width, y * height - 15);
        }
    };

    this.drawCircle = function(x, y, radius, color, fill) {
        const centerX = x * width;
        const centerY = y * height;
        const r = radius;

        context.beginPath();
        context.arc(centerX, centerY, r, 0, Math.PI * 2, false);
        context.closePath();

        context.strokeStyle = color;
        context.stroke();

        if (fill) {
            context.fillStyle = color;
            context.fill();
        }
    };

    this.drawRectangle = function(x, y, w, h, color, fill) {
        context.beginPath();
        let dx = w * width;
        let dy = h * height;

        // Keep the drawing centered:
        let x0 = (x * width) - 0.5 * dx;
        let y0 = (y * height) - 0.5 * dy;

        context.strokeStyle = color;
        context.fillStyle = color;

        if (fill)
            context.fillRect(x0, y0, dx, dy);
        else
            context.strokeRect(x0, y0, dx, dy);
    };

    this.drawTriangle = function(x, y, w, h, heading, color, fill) {
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
        context.lineTo(dx + (w*1.5),    dy - h);    // 150, 0
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

    this.drawHeadingArrow = function(x, y, headingX, headingY) {
        const centerX = x * width;
        const centerY = y * height;

        //
        const arrowLength = 30;

        context.moveTo(centerX, centerY);
        context.lineTo(centerX + (headingX * arrowLength), centerY + (headingY * arrowLength));
        context.stroke();
    };

    this.resetCanvas = function () {
        context.clearRect(0, 0, height, width);
        context.beginPath();
    };
};

let Simple_Continuous_Module = function(canvas_width, canvas_height) {
    // Create the element
    // ------------------

    // Create the tag:
    let canvas_tag = "<canvas width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "style='grid-row: 1 / span 2;border:1px dotted'></canvas>";

    // Append it to body:
    let canvas = $(canvas_tag)[0];
    $("#elements").append(canvas);

    // Create the context and the drawing controller:
    let context = canvas.getContext("2d");
    let canvasDraw = new ContinuousVisualization(canvas_width, canvas_height, context);

    this.render = function (data) {
        canvasDraw.resetCanvas();
        canvasDraw.draw(data);
    };

    this.reset = function () {
        canvasDraw.resetCanvas();
    };
};