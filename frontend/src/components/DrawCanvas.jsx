import React, { useRef, useState, useEffect } from "react";
import { Button, Slider } from "antd";
import { TwitterPicker } from "react-color";
import "antd/dist/antd.css";
import "../css/DrawCanvas.css"

const LEDS_X = 64;
const LEDS_Y = 32;
const WIDTH = 512;
const HEIGHT = 256;
const SPACING = HEIGHT / LEDS_Y;
const RADIUS = SPACING * 0.25;

const drawMatrix = ctx => {
  ctx.fillStyle = 'rgb(55,55,55)';
  ctx.fillRect(0, 0, WIDTH, HEIGHT);
  ctx.fillStyle = 'rgb(105,105,105)';
  for (let y = 0; y < LEDS_Y; y++) {
    for (let x = 0; x < LEDS_X; x++) {
      drawLED(ctx, x, y);
    }
  }
};

const drawLED = (ctx, x, y) => {
  ctx.beginPath();
  ctx.arc(idxToPos(x), idxToPos(y), RADIUS, 0, Math.PI * 2, false);
  ctx.fill()
};

const colorsEqual = (c1, c2) => (c1[0] === c2[0] && c1[1] === c2[1] && c1[2] === c2[2]);

const idxToPos = i => (i + 0.5) * SPACING;
const posToIdx = p => Math.floor(p / SPACING - 0.5);

function DrawCanvas(props) {

  const [ctx, setCtx] = useState();
  const [isDrawing, setIsDrawing] = useState(false);
  const [drawRadius, setDrawRadius] = useState(2);
  const [drawColor, setDrawColor] = useState([65, 230, 124]);
  const canvasRef = useRef();

  const [leds, setLeds] = useState([]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const _ctx = canvas.getContext('2d');
    drawMatrix(_ctx);
    fillLeds([0, 0, 0]);
    setCtx(_ctx);
  }, []);

  const onMouseMove = event => {
    if (!isDrawing) return;
    const {offsetX, offsetY} = event.nativeEvent;
    draw(offsetX, offsetY);
  };

  const onMouseClick = event => {
    const {offsetX, offsetY} = event.nativeEvent;
    draw(offsetX, offsetY);
  };

  const onTouchMove = event => {
    const rect = event.target.getBoundingClientRect();
    const x = event.targetTouches[0].pageX - rect.left;
    const y = event.targetTouches[0].pageY - rect.top;
    draw(x, y);
  };

  const startDrawing = () => setIsDrawing(true);

  const stopDrawing = () => setIsDrawing(false);

  const draw = (offsetX, offsetY) => {
    const [ix, iy] = [posToIdx(offsetX), posToIdx(offsetY)];
    const diff = drawRadius;
    ctx.fillStyle = `rgb(${drawColor[0]}, ${drawColor[1]}, ${drawColor[2]})`;
    const modified = [];
    for (let y = Math.max(0, iy - diff); y < Math.min(iy + diff, LEDS_Y); y++) {
      for (let x = Math.max(0, ix - diff); x < Math.min(ix + diff, LEDS_X); x++) {
        const ledIndex = y * LEDS_Y + x;
        if (Math.sqrt(Math.pow(offsetX - idxToPos(x)  , 2) +
          Math.pow(offsetY - idxToPos(y), 2)) <= drawRadius * 2 * RADIUS &&
          !colorsEqual(drawColor, leds[ledIndex])) {
          drawLED(ctx, x, y);
          modified.push({x, y, r: drawColor[0], g: drawColor[1], b: drawColor[2]});
        }
      }
    }
    const newLeds = [...leds];
    modified.forEach(p => newLeds[p.y * LEDS_Y + p.x] = [p.r, p.g, p.b]);
    setLeds(newLeds);
    if (modified.length > 0) {
      console.log(modified);
      props.socket.emit('draw', {pixels: modified});
    }
  };

  const clear = () => {
    fetch("/clear", {
      method: "GET"
    }).then(res => console.log(res));
    fillLeds([0, 0, 0]);
    drawMatrix(ctx);
  };

  const fillLeds = clr => {
    const newLeds = [];
    for (let i = 0; i < LEDS_X * LEDS_Y; i++) {
      newLeds[i] = clr;
    }
    setLeds(newLeds);
  };

  return (
    <div className="draw">
      <canvas className="canvas" ref={canvasRef} width={WIDTH} height={HEIGHT}
              onMouseDown={startDrawing}
              onMouseUp={stopDrawing}
              onMouseMove={onMouseMove}
              onTouchStart={startDrawing}
              onTouchEnd={stopDrawing}
              onTouchMove={onTouchMove}
              onClick={onMouseClick}
      />
      <TwitterPicker color={{r: drawColor[0], g: drawColor[1], b: drawColor[2]}}
                     onChange={clr => setDrawColor([clr.rgb.r, clr.rgb.g, clr.rgb.b])}/>
      <Slider value={drawRadius} onChange={setDrawRadius} min={1} max={10}/>
      <Button onClick={clear}>Clear</Button>
    </div>
  )

}

export default DrawCanvas;
