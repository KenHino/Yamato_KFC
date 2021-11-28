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
                $("#pin-info").html(this.arrive);
                // $("#pin-info").html("x:" + this.originx + ", y:" + this.originy);
            }

            testHit(point) {
                return (this.rectx <= point.x && point.x <= this.rectx + this.w) &&
                    (this.recty <= point.y && point.y <= this.recty + this.h);
            }

            drawText() {
                context.font = "24px serif";
                context.fillText(this.arrive, this.x+10, this.y+10);
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

        const pins = []
        $(".coordinates").each(function (i, coordinate) {
            let xelem = $(coordinate).children()[0]
            let x = $(xelem).data("coordinate")
            let yelem = $(coordinate).children()[1]
            let y = $(yelem).data("coordinate")

            pins.push(new Pin((x+10)*20+100, (y+10)*20+100))
        })

        console.log(pins)

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

            
            const orders = []
            $(".orders").each(function (i, order) {
                let o = $(order).data("order")
                orders.push(o)
            })
            const time_lists = []
            $(".time_lists").each(function (i, time) {
                let t = $(time).data("time")
                time_lists.push(t)
            })

            let prev, next;
            $.each(orders, function(i, order) {
                if (i == 0) {
                    prev = order;
                    return true;
                }
                next = order;
                console.log(prev,next)
                new Line(pins[prev], pins[next]).draw("route");
                prev = next;
            })

            
            $.each(orders, function(i, order) {
                pins[order].arrive = time_lists[i]
                pins[order].drawText();
            })


            // new Line(pins[0], pins[1]).draw("route");

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
        }

	}