    var canvas, context;
    
    (() => {
        window.onload = () => {
            initCanvas();
        };
    })();

    function initCanvas() {
        canvas = document.getElementById("map-canvas");
        context = canvas.getContext("2d");

        context.save();
        context.fillStyle = "rgb(241,243,244)";
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.restore();

        generateCoordinate(context);
    }

    function generateCoordinate(context) {
        class Pin {
            constructor(x,y) {
                this.originx = x;
                this.originy = y;

                this.x = x;
                this.y = y;

                this.w = 24;
                this.h = 24;

                this.type = "undelivered";
            }

            calcFromMaxMin(max, min) {
                this.x = (this.originx - min) * 4 / 5 * canvas.width / max + canvas.width / 10;
                this.y = (this.originy - min) * 4 / 5 * canvas.height / max + canvas.height / 10;
                
                this.rectx = this.x - this.w / 2;
                this.recty = this.y - this.h;
            }

            draw(type) {
                context.save();
                const chara = new Image();

                chara.src = "/static/yamato/mapPin.png";
                
                if (type == "hover") {
                    chara.src = "/static/yamato/mapPinSelected.png";
                }
                chara.onload = () => {
                    context.drawImage(chara, this.rectx, this.recty, this.w, this.w)
                }
                context.restore();
            }

            hover() {
                this.draw("hover")
            }

            leave() {
                this.draw()

            }

            click() {
                const selectType = $('input[name=selectType]:checked').val();
                if (selectType == "currentPosition") {

                } else if (selectType == "delivered") {

                }
                $("#pin-info").html("x:" + this.originx + ", y:" + this.originy);
            }

            testHit(point) {
                return (this.rectx <= point.x && point.x <= this.rectx + this.w) &&
                    (this.recty <= point.y && point.y <= this.recty + this.h);
            }
        }

        class Line {
            constructor(pinA, pinB) {
                this.start = pinA;
                this.end = pinB;
            }

            draw(type) {
                context.strokeStyle = "rgb(217,219,223)";
                if (type=="route") context.strokeStyle = "rgb(29,106,212)"
                context.lineWidth = 8;
                context.lineCap = "round";

                context.beginPath();
                context.moveTo(this.start.x, this.start.y);
                context.lineTo(this.end.x, this.end.y);
                context.closePath();
                context.stroke();

                context.strokeStyle = "white";
                if (type=="route") context.strokeStyle = "rgb(102,157,246)"
                context.lineWidth = 6;
                context.lineCap = "round";

                context.beginPath();
                context.moveTo(this.start.x, this.start.y);
                context.lineTo(this.end.x, this.end.y);
                context.closePath();
                context.stroke();
            }
        }

        const pins = [
            new Pin(200,300),
            new Pin(100,200),
            new Pin(400,100),
            new Pin(150,400),
        ]

        generateMap(pins);

        canvas.addEventListener("mousemove", e => {
            const rect = canvas.getBoundingClientRect();
            const point = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            }

            pins.forEach(pin => {
                if (pin.testHit(point)) {
                    pin.hover(context);
                } else {
                    pin.leave(context);
                }
            })
        })

        canvas.addEventListener("click", e => {
            const rect = canvas.getBoundingClientRect();
            const point = {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
            }

            pins.forEach(pin => {
                if (pin.testHit(point)) {
                    pin.click(context);
                }
            })
        })

        function generateMap(pins) {
            // ピンを描画領域内に収まるように調整
            adjustCoordinate(pins);

            // 各ピンを描画
            $.each(pins, function(i, pin) {
                pin.draw();
            })

            new Line(pins[0], pins[1]).draw("route");

            function adjustCoordinate(pins) {
                const xs = pins.map(function(c){return c.x})
    
                const x_max = Math.max.apply(null, xs)
                const x_min = Math.min.apply(null, xs)
    
                $.each(pins, function(i, pin) {
                    pin.calcFromMaxMin(x_max, x_min);
                })
    
                const new_ys = pins.map(function(c){return c.y})
                const y_max = Math.max.apply(null, new_ys)
                const y_min = Math.min.apply(null, new_ys)
    
                if (y_min < canvas.height / 10 || canvas.height * 4 / 5 < y_max) {
                    $.each(pins, function(i, pin) {
                        pin.calcFromMaxMin(y_max, y_min);
                    })
                }
            }
            
            // function addPoint(val) {
            //     context.save();
            //     context.beginPath();
            //     context.arc(val.x, val.y, 5, 0, Math.PI * 2, false);
            //     context.fill();
            //     context.moveTo(val.x, val.y);
            //     context.restore();
            // }

        }

	}