//Copyright (c) 2018 by Jack Rugile (https://codepen.io/jackrugile/pen/JLOXWZ)
//
//Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

var stats = new Stats();

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

var Calc = function () {
  function Calc() {
    _classCallCheck(this, Calc);
  }

  _createClass(Calc, null, [{
    key: 'rand',


    /*
    ------------------------------------------
    | rand:float - returns random float
    |
    | min:number - minimum value
    | max:number - maximum value
    | ease:function - easing function to apply to the random value
    |
    | Get a random float between two values,
    | with the option of easing bias.
    ------------------------------------------ */
    value: function rand(min, max, ease) {
      if (max === undefined) {
        max = min;
        min = 0;
      }
      var random = Math.random();
      if (ease) {
        random = ease(Math.random(), 0, 1, 1);
      }
      return random * (max - min) + min;
    }

    /*
    ------------------------------------------
    | randInt:integer - returns random integer
    |
    | min:number - minimum value
    | max:number - maximum value
    | ease:function - easing function to apply to the random value
    |
    | Get a random integer between two values,
    | with the option of easing bias.
    ------------------------------------------ */

  }, {
    key: 'randInt',
    value: function randInt(min, max, ease) {
      if (max === undefined) {
        max = min;
        min = 0;
      }
      var random = Math.random();
      if (ease) {
        random = ease(Math.random(), 0, 1, 1);
      }
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    /*
    ------------------------------------------
    | randArr:item - returns random iem from array
    |
    | arr:array - the array to randomly pull from
    |
    | Get a random item from an array.
    ------------------------------------------ */

  }, {
    key: 'randArr',
    value: function randArr(arr) {
      return arr[Math.floor(Math.random() * arr.length)];
    }

    /*
    ------------------------------------------
    | map:number - returns a mapped value
    |
    | val:number - input value
    | inputMin:number - minimum of input range
    | inputMax:number - maximum of input range
    | outputMin:number - minimum of output range
    | outputMax:number - maximum of output range
    |
    | Get a mapped value from and input min/max
    | to an output min/max.
    ------------------------------------------ */

  }, {
    key: 'map',
    value: function map(val, inputMin, inputMax, outputMin, outputMax) {
      return (outputMax - outputMin) * ((val - inputMin) / (inputMax - inputMin)) + outputMin;
    }

    /*
    ------------------------------------------
    | clamp:number - returns clamped value
    |
    | val:number - value to be clamped
    | min:number - minimum of clamped range
    | max:number - maximum of clamped range
    |
    | Clamp a value to a min/max range.
    ------------------------------------------ */

  }, {
    key: 'clamp',
    value: function clamp(val, min, max) {
      return Math.max(Math.min(val, max), min);
    }

    /*
    ------------------------------------------
    | roundToUpperInterval:number - returns rounded up value
    |
    | value:number - value to be rounded
    | interval:number - interval
    |
    | Round up a value to the next highest interval.
    ------------------------------------------ */

  }, {
    key: 'roundToUpperInterval',
    value: function roundToUpperInterval(value, interval) {
      if (value % interval === 0) {
        value += 0.0001;
      }
      return Math.ceil(value / interval) * interval;
    }

    /*
    ------------------------------------------
    | roundDownToInterval:number - returns rounded down value
    |
    | value:number - value to be rounded
    | interval:number - interval
    |
    | Round down a value to the next lowest interval.
    ------------------------------------------ */

  }, {
    key: 'roundToLowerInterval',
    value: function roundToLowerInterval(value, interval) {
      if (value % interval === 0) {
        value -= 0.0001;
      }
      return Math.floor(value / interval) * interval;
    }

    /*
    ------------------------------------------
    | roundToNearestInterval:number - returns rounded value
    |
    | value:number - value to be rounded
    | interval:number - interval
    |
    | Round a value to the nearest interval.
    ------------------------------------------ */

  }, {
    key: 'roundToNearestInterval',
    value: function roundToNearestInterval(value, interval) {
      return Math.round(value / interval) * interval;
    }

    /*
    ------------------------------------------
    | intersectSphere:boolean - returns if intersecting or not
    |
    | a:object - sphere 1 with radius, x, y, and z
    | b:object - sphere 2 with radius, x, y, and z
    |
    | Check if two sphere are intersecting
    | in 3D space.
    ------------------------------------------ */

  }, {
    key: 'intersectSphere',
    value: function intersectSphere(a, b) {
      var distance = Math.sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) + (a.z - b.z) * (a.z - b.z));
      return distance < a.radius + b.radius;
    }

    /*
    ------------------------------------------
    | getIndexFromCoords:number - returns index
    |
    | x:number - x value (column)
    | y:number - y value (row)
    | w:number - width of grid
    |
    | Convert from grid coords to index.
    ------------------------------------------ */

  }, {
    key: 'getIndexFromCoords',
    value: function getIndexFromCoords(x, y, w) {
      return x + y * w;
    }

    /*
    ------------------------------------------
    | getCoordsFromIndex:object - returns coords
    |
    | i:number - index
    | w:number - width of grid
    |
    | Convert from index to grid coords.
    ------------------------------------------ */

  }, {
    key: 'getCoordsFromIndex',
    value: function getCoordsFromIndex(i, w) {
      return {
        x: i % w,
        y: Math.floor(i / w)
      };
    }
  }]);

  return Calc;
}();

;
console.clear();

var SpatialHash = function () {
  function SpatialHash(cellSize) {
    _classCallCheck(this, SpatialHash);

    this.cellSize = cellSize;
    this.reset();
  }

  _createClass(SpatialHash, [{
    key: 'reset',
    value: function reset() {
      this.cells = {};
    }
  }, {
    key: 'key',
    value: function key(point) {
      var x = math.floor(point.x / this.cellSize);
      var y = math.floor(point.y / this.cellSize);
      return x + '-' + y;
    }
  }, {
    key: 'insert',
    value: function insert(point) {
      var key = this.key(point);
      var cell = this.cells[key];
      if (!cell) {
        cell = this.cells[key] = {};
        cell.x = math.floor(point.x / this.cellSize);
        cell.y = math.floor(point.y / this.cellSize);
        cell.alpha = 0;
        cell.alphaTarget = 0;
        cell.items = [];
      }
      cell.items.push(point);
    }
  }, {
    key: 'remove',
    value: function remove(point, last) {
      var cell = null;
      var key = null;
      if (last) {
        cell = this.cells[last];
      } else {
        key = this.key(point);
        cell = this.cells[key];
      }
      if (cell) {
        var index = fast.indexOf(cell.items, point);
        if (index !== -1) {
          cell.items.splice(index, 1);
        }
      }
    }
  }]);

  return SpatialHash;
}();

var Point = function () {
  function Point(demo, ctx) {
    _classCallCheck(this, Point);

    this.guid = demo.guid++;
    this.demo = demo;
    this.ctx = demo.ctx;
    this.x = Calc.rand(0, this.demo.width);
    this.y = Calc.rand(0, this.demo.height);
    this.vx = Calc.rand(-1, 1);
    this.vy = Calc.rand(-1, 1);
    this.radius = 1;
    this.demo.sh.insert(this);
    this.hash = this.demo.sh.key(this);
    this.lastHash = this.hash;
    this.thresh = math.pow(this.demo.sh.cellSize, 2);
    this.compareList = [];
    this.scale = 1;
    this.scaleTarget = 1;
  }

  _createClass(Point, [{
    key: 'compareOther',
    value: function compareOther(other) {
      if (fast.indexOf(this.compareList, other.guid) > -1 || fast.indexOf(other.compareList, this.guid) > -1) {
        return false;
      }
      var dx = other.x - this.x;
      var dy = other.y - this.y;
      var dist = dx * dx + dy * dy;
      if (dist < this.thresh) {
        var angle = math.atan2(dy, dx);
        var cos = math.cos(angle);
        var sin = math.sin(angle);
        var mag = (this.thresh - dist) * 0.0001;
        this.vx -= cos * mag;
        this.vy -= sin * mag;
        other.vx += cos * mag;
        other.vy += sin * mag;
      }
      this.compareList.push(other.guid);
      other.compareList.push(this.guid);
    }
  }, {
    key: 'compareMouse',
    value: function compareMouse() {
      var dx = this.demo.mouse.x - this.x;
      var dy = this.demo.mouse.y - this.y;
      var dist = dx * dx + dy * dy;
      var thresh = this.thresh * 3;
      this.scaleTarget = 1;
      if (dist < thresh) {
        var angle = math.atan2(dy, dx);
        var mag = (thresh - dist) * 0.0003;
        this.vx -= math.cos(angle) * mag;
        this.vy -= math.sin(angle) * mag;
        this.scaleTarget = 1 + (thresh - dist) * 0.009;
      }
    }
  }, {
    key: 'preupdate',
    value: function preupdate() {
      this.inRange = false;
      this.compareList.length = 0;
    }
  }, {
    key: 'update',
    value: function update(iMax) {
      this.hash = this.demo.sh.key(this);
      if (this.hash != this.lastHash) {
        this.demo.sh.remove(this, this.lastHash);
        this.demo.sh.insert(this);
      }

      this.vx += (this.demo.mouse.x - this.demo.width / 2) * 0.0009;
      this.vy += (this.demo.mouse.y - this.demo.height / 2) * 0.0009;

      this.compareMouse();

      if (this.vx > 0.5) {
        this.vx *= 0.95;
      }
      if (this.vx < -0.5) {
        this.vx *= 0.95;
      }
      if (this.vy > 0.5) {
        this.vy *= 0.95;
      }
      if (this.vy < -0.5) {
        this.vy *= 0.95;
      }

      this.x += this.vx * this.demo.dt;
      this.y += this.vy * this.demo.dt;

      if (this.x >= this.demo.width - this.radius) {
        this.x = this.demo.width - this.radius;
        this.vx -= 1;
      }
      if (this.x <= this.radius) {
        this.x = this.radius;
        this.vx += 1;
      }
      if (this.y >= this.demo.height - this.radius) {
        this.y = this.demo.height - this.radius;
        this.vy -= 1;
      }
      if (this.y <= this.radius) {
        this.y = this.radius;
        this.vy += 1;
      }

      this.lastHash = this.hash;

      this.scale += (this.scaleTarget - this.scale) * 0.1;
    }
  }, {
    key: 'render',
    value: function render() {
      this.demo.ctx.fillStyle = 'hsla(' + (this.demo.hue + this.y * 0.15 + this.x * 0.15) + ', 80%, 50%, 1)';
      this.demo.ctx.beginPath();
      this.demo.ctx.arc(this.x, this.y, this.radius * this.scale, 0, Math.PI * 2);
      this.demo.ctx.fill();
    }
  }]);

  return Point;
}();

var Demo = function () {
  function Demo() {
    var _this = this;

    _classCallCheck(this, Demo);

    this.guid = 0;
    this.currTime = Date.now();
    this.lastTime = this.currTime;
    this.dt = 1;
    this.setupCanvas();
    this.setupHash();

    this.points = [];
    this.combined = [];
    this.mouse = {
      x: 0,
      y: 0
    };
    this.hue = 160;

    this.capturer = new CCapture({
      verbose: true,
      framerate: 60,
      //motionBlurFrames: 12,
      quality: 100,
      format: 'webm',
      workersPath: 'js/'
    });
    this.capturing = false;

    this.reset();
    this.loop();

    window.addEventListener('resize', function () {
      return _this.onResize();
    });
    window.addEventListener('mousemove', function (e) {
      return _this.onMousemove(e);
    });
    window.addEventListener('keydown', function (e) {
      return _this.onKeydown(e);
    });
  }

  _createClass(Demo, [{
    key: 'setupCanvas',
    value: function setupCanvas() {
      this.canvas = document.querySelector('canvas');
      this.ctx = this.canvas.getContext('2d');
    }
  }, {
    key: 'setupHash',
    value: function setupHash() {
      this.sh = new SpatialHash(25);
    }
  }, {
    key: 'reset',
    value: function reset() {
      this.points = [];
      this.sh.reset();
      this.onResize();

      for (var i = 0; i < 300; i++) {
        var point = new Point(this);
        this.points.push(point);
      }
    }
  }, {
    key: 'onResize',
    value: function onResize() {
      this.width = 1920;
      this.height = 1280;
      this.dpr = window.devicePixelRatio;

      this.canvas.width = this.width * this.dpr;
      this.canvas.height = this.height * this.dpr;
      this.canvas.style.width = '100%';
      this.canvas.style.height = '100vh';
      this.ctx.scale(this.dpr, this.dpr);

      this.bcr = this.canvas.getBoundingClientRect();
      this.mouse.x = this.width / 2;
      this.mouse.y = this.height / 2;
    }
  }, {
    key: 'onMousemove',
    value: function onMousemove(e) {
      this.mouse.x = Calc.clamp(e.pageX - this.bcr.left, 0, this.width - 1);
      this.mouse.y = Calc.clamp(e.pageY - this.bcr.top, 0, this.height - 1);
    }
  }, {
    key: 'onKeydown',
    value: function onKeydown(e) {
      if (e.which === 82) {
        //this.toggleCapture();
      }
    }
  }, {
    key: 'toggleCapture',
    value: function toggleCapture() {
      if (this.capturing) {
        this.capturer.stop();
        this.capturer.save();
        this.capturing = false;
      } else {
        this.capturer.start();
        this.capturing = true;
      }
    }
  }, {
    key: 'preupdate',
    value: function preupdate() {
      var i = this.points.length;
      while (i--) {
        var point = this.points[i];
        point.preupdate(i);
      }
    }
  }, {
    key: 'update',
    value: function update() {
      this.hue += 0.5;

      for (var key in this.sh.cells) {
        var _combined, _combined2, _combined3, _combined4, _combined5, _combined6, _combined7, _combined8, _combined9;

        this.combined.length = 0;
        var cell = this.sh.cells[key];
        cell && (_combined = this.combined).push.apply(_combined, _toConsumableArray(cell.items));
        var cellNW = this.sh.cells[cell.x - 1 + '-' + (cell.y - 1)];
        cellNW && (_combined2 = this.combined).push.apply(_combined2, _toConsumableArray(cellNW.items));
        var cellN = this.sh.cells[cell.x + '-' + (cell.y - 1)];
        cellN && (_combined3 = this.combined).push.apply(_combined3, _toConsumableArray(cellN.items));
        var cellNE = this.sh.cells[cell.x + 1 + '-' + (cell.y - 1)];
        cellNE && (_combined4 = this.combined).push.apply(_combined4, _toConsumableArray(cellNE.items));
        var cellW = this.sh.cells[cell.x - 1 + '-' + cell.y];
        cellW && (_combined5 = this.combined).push.apply(_combined5, _toConsumableArray(cellW.items));
        var cellE = this.sh.cells[cell.x + 1 + '-' + cell.y];
        cellE && (_combined6 = this.combined).push.apply(_combined6, _toConsumableArray(cellE.items));
        var cellSW = this.sh.cells[cell.x - 1 + '-' + (cell.y + 1)];
        cellSW && (_combined7 = this.combined).push.apply(_combined7, _toConsumableArray(cellSW.items));
        var cellS = this.sh.cells[cell.x + '-' + (cell.y + 1)];
        cellS && (_combined8 = this.combined).push.apply(_combined8, _toConsumableArray(cellS.items));
        var cellSE = this.sh.cells[cell.x + 1 + '-' + (cell.y + 1)];
        cellSE && (_combined9 = this.combined).push.apply(_combined9, _toConsumableArray(cellSE.items));
        var j = this.combined.length;
        while (j--) {
          var item = this.combined[j];
          var k = j;
          while (k--) {
            var other = this.combined[k];
            item.compareOther(other);
          }
        }
      }

      var i = this.points.length;
      while (i--) {
        var point = this.points[i];
        point.update(i);
      }
    }
  }, {
    key: 'render',
    value: function render() {
      this.ctx.globalCompositeOperation = 'source-over';
      this.ctx.fillStyle = 'hsla(0, 0%, 5%, 1)';
      this.ctx.fillRect(0, 0, this.width, this.height);

      this.ctx.globalCompositeOperation = 'lighter';

      this.ctx.beginPath();
      for (var x = 0; x < this.width; x += this.sh.cellSize) {
        this.ctx.moveTo(x, 0);
        this.ctx.lineTo(x, this.height);
      }
      for (var y = 0; y < this.height; y += this.sh.cellSize) {
        this.ctx.moveTo(0, y);
        this.ctx.lineTo(this.width, y);
      }
      this.ctx.strokeStyle = 'hsla(0, 0%, 100%, 0.05)';
      this.ctx.stroke();

      var mxc = math.floor(this.mouse.x / this.sh.cellSize);
      var myc = math.floor(this.mouse.y / this.sh.cellSize);

      for (var key in this.sh.cells) {
        var cell = this.sh.cells[key];
        var length = cell.items.length;
        cell.alphaTarget = length * 0.04;
        var b = 50;
        var s = 70;
        if (cell.x === mxc && cell.y == myc) {
          b = 70;
          s = 100;
          cell.alphaTarget = 0.9;
          cell.alpha = 0.8;
        }
        cell.alpha += (cell.alphaTarget - cell.alpha) * 0.1;
        this.ctx.fillStyle = 'hsla(' + (this.hue + cell.y * this.sh.cellSize * 0.15 + cell.x * this.sh.cellSize * 0.15) + ', ' + s + '%, ' + b + '%, ' + cell.alpha + ')';
        this.ctx.fillRect(cell.x * this.sh.cellSize, cell.y * this.sh.cellSize, this.sh.cellSize, this.sh.cellSize);
      }

      // draw points
      var i = this.points.length;
      while (i--) {
        var point = this.points[i];
        point.render();
      }

      if (this.capturing) {
        this.capturer.capture(this.canvas);
      }
    }
  }, {
    key: 'loop',
    value: function loop() {
      var _this2 = this;

      this.currTime = Date.now();
      if (this.oldTime) {
        this.dt = (this.currTime - this.oldTime) / (1000 / 60);
      }
      this.oldTime = this.currTime;

      stats.begin();
      this.preupdate();
      this.update();
      this.render();
      stats.end();
      window.requestAnimationFrame(function () {
        return _this2.loop();
      });
    }
  }]);

  return Demo;
}();

var demo = new Demo();



