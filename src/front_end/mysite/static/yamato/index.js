    (() => {
        window.onload = () => {
            initCanvas();
        };
    })();

    function initCanvas() {
        const canvas = document.getElementById("map-canvas");
        const context = canvas.getContext("2d");

        generateCoordinate(context);
    }

    function generateCoordinate(context) {
        class coordinate {
            constructor(x,y) {
                this.x = x;
                this.y = y;
            }
        }

        const coordinates = [
            new coordinate(200,300),
            new coordinate(100,200),
            new coordinate(400,100),
            new coordinate(150,400),
        ]

        generateMap(coordinates);

        function generateMap(coordinates) {
            const xs = coordinates.map(function(c){return c.x})
            const ys = coordinates.map(function(c){return c.x})

            const x_max = Math.max.apply(null, xs)
            const x_min = Math.min.apply(null, ys)
            const y_max = Math.max.apply(null, xs)
            const y_min = Math.min.apply(null, ys)

            $.each(coordinates, function(i, val) {
                addPin(val);
            })
            
            function addPoint(val) {
                context.save();
                context.beginPath();
                context.arc(val.x, val.y, 5, 0, Math.PI * 2, false);
                context.fill();
                context.moveTo(val.x, val.y);
                context.restore();
            }

            function addPin(val) {
                const chara = new Image();
                chara.src = "mapPin.png";
                chara.onload = () => {
                    context.drawImage(chara, 200, 200)
                }
            }

        }

	}