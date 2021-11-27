    (() => {
        window.onload = () => {
            // init2D();
            initCanvas();
        };
    })();

    function init2D() {
        const renderer = new THREE.WebGLRenderer();
        renderer.setSize(500, 500);
        renderer.setClearColor(0xff0000, 1);
        renderer.autoClear = false;
        document.body.appendChild( renderer.domElement );

        const aspect = 5/8;
        const camera = new THREE.PerspectiveCamera()
        camera.position.z = 500;

        // Sceneを用意
        var scene = new THREE.Scene();
        scene.add( camera );

        generateCoordinate(scene);

        // render
        renderer.render( scene, camera );
    }

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
                addPoint(val);
            })

            function addPoint2D(val) {
                var geometry = new THREE.SphereGeometry(5, 5);
                var material = new THREE.MeshBasicMaterial({color: 0xffffff})
                var mesh = new THREE.Mesh( geometry, material );
                mesh.position.set(val.x, val.y)
                scene.add( mesh );
            }
            
            function addPoint(val) {
                context.save();
                context.beginPath();
                context.arc(val.x, val.y, 5, 0, Math.PI * 2, false);
                context.fill();
                context.moveTo(val.x, val.y);
                context.restore();
            }

        }

	}