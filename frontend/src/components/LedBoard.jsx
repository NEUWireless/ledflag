import React, { useRef, useState, useEffect } from "react";
import "../css/DrawCanvas.css";

export const LEDS_X = 64;
export const LEDS_Y = 32;

export const leds = [];

const drawMatrix = (ctx, scale) => {
  ctx.fillStyle = 'rgb(40,40,40)';
  ctx.fillRect(0, 0, scale.width, scale.height);
  ctx.fillStyle = 'rgb(0,0,0)';
  for (let y = 0; y < LEDS_Y; y++) {
    for (let x = 0; x < LEDS_X; x++) {
      drawLED(ctx, x, y, scale);
    }
  }
};

const drawLED = (ctx, x, y, scale) => {
  ctx.beginPath();
  ctx.arc(idxToPos(x, scale), idxToPos(y, scale), scale.radius, 0, Math.PI * 2, false);
  ctx.fill();
};

const idxToPos = (i, scale) => (i + 0.5) * scale.spacing;
const posToIdx = (p, scale) => Math.floor(p / scale.spacing - 0.5);
export const colorsEqual = (c1, c2) => (c1[0] === c2[0] && c1[1] === c2[1] && c1[2] === c2[2]);

const fillLeds = clr => {
  for (let i = 0; i < LEDS_X * LEDS_Y; i++) {
    leds[i] = clr;
  }
};

fillLeds([0, 0, 0]);

function LedBoard(props) {

  const canvasRef = useRef();
  const [isDrawing, setIsDrawing] = useState(false);

  useEffect(() => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    drawMatrix(ctx, props.scale);
    for (let y = 0; y < LEDS_Y; y++) {
      for (let x = 0; x < LEDS_X; x++) {
        const p = leds[y * LEDS_X + x];
        ctx.fillStyle = `rgb(${p[0]}, ${p[1]}, ${p[2]})`;
        drawLED(ctx, x, y, props.scale);
      }
    }
  }, [props.scale]);

  useEffect(() => {
    fetch('/draw/get', {
      method: 'GET',
      headers: {
        "Accept": "application/json"
      }
    }).then(res => {
      if (!res.ok) {
        throw new Error("Unable to fetch led current state");
      }
      return res.json();
    }).then(({ pixels }) => {
      const ctx = canvasRef.current.getContext('2d');
      for (let i = 0; i < LEDS_X * LEDS_Y; i++) {
        const p = pixels[i];
        leds[i] = p;
        const x = i % LEDS_X;
        const y = Math.floor(i / LEDS_X);
        ctx.fillStyle = ctx.fillStyle = `rgb(${p.r}, ${p.g}, ${p.b})`;
        drawLED(ctx, x, y, props.scale);
      }
    }).catch(err => {
      console.log(err);
    });
  }, []);

  useEffect(() => {
    const ctx = canvasRef.current.getContext('2d');
    props.socket.on('draw_update', ({ pixels }) => {
      pixels.forEach(p => {
        ctx.fillStyle = `rgb(${p.r}, ${p.g}, ${p.b})`;
        drawLED(ctx, p.x, p.y, props.scale);
        leds[p.y * LEDS_X + p.x] = [p.r, p.g, p.b];
      });
    });
    props.socket.on('draw_clear', () => {
      fillLeds([0, 0, 0]);
      drawMatrix(ctx, props.scale);
    });
  }, [props.socket, props.scale]);

  const drawPoint = (ctx, offsetX, offsetY) => {
    const [ix, iy] = [posToIdx(offsetX, props.scale), posToIdx(offsetY, props.scale)];
    const diff = props.drawRadius;
    const modified = [];
    for (let y = Math.max(0, iy - diff); y < Math.min(iy + diff, LEDS_Y); y++) {
      for (let x = Math.max(0, ix - diff); x < Math.min(ix + diff, LEDS_X); x++) {
        const ledIndex = y * LEDS_X + x;
        if (Math.sqrt(Math.pow(offsetX - idxToPos(x, props.scale)  , 2) +
          Math.pow(offsetY - idxToPos(y, props.scale), 2)) <= diff * 2 * props.scale.radius &&
          !colorsEqual(props.drawColor, leds[ledIndex])) {
          drawLED(ctx, x, y, props.scale);
          modified.push({x, y, r: props.drawColor[0], g: props.drawColor[1], b: props.drawColor[2]});
        }
      }
    }
    return modified;
  };

  const draw = (offsetX, offsetY) => {
    const ctx = canvasRef.current.getContext('2d');
    ctx.fillStyle = `rgb(${props.drawColor[0]}, ${props.drawColor[1]}, ${props.drawColor[2]})`;
    const modified = drawPoint(ctx, offsetX, offsetY, leds);
    modified.forEach(p => leds[p.y * LEDS_X + p.x] = [p.r, p.g, p.b]);
    if (modified.length !== 0) {
      props.socket.emit('draw', modified);
    }
  };

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
    const x = event.targetTouches[0].clientX - rect.left;
    const y = event.targetTouches[0].clientY - rect.top;
    draw(x, y);
  };

  const startDrawing = () => setIsDrawing(true);
  const stopDrawing = () => setIsDrawing(false);

  return <canvas ref={canvasRef} className="canvas"
                 width={props.scale.width}
                 height={props.scale.height}
                 onMouseDown={startDrawing}
                 onMouseUp={stopDrawing}
                 onMouseMove={onMouseMove}
                 onTouchStart={startDrawing}
                 onTouchEnd={stopDrawing}
                 onTouchMove={onTouchMove}
                 onClick={onMouseClick}>
  </canvas>

}

export default LedBoard;
