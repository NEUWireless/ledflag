import React, {useState, useEffect, useRef, useCallback} from "react";
import LedBoard, {LEDS_Y, colorsEqual} from "./LedBoard";
import "../css/DrawCanvas.css";
import {TwitterPicker} from "react-color";
import {Button, Slider} from "antd";

const calculateScale = width => {
  const height = Math.round(width / 2);
  const spacing = height / LEDS_Y;
  const radius = spacing * 0.25;
  return {width: Math.floor(width), height, spacing, radius};
};

function debounce(fn, ms) {
  let timer;
  return () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
      timer = null;
      fn.apply(this, arguments)
    }, ms)
  };
}

function DrawMode(props) {

  const [scale, setScale] = useState(calculateScale(512));
  const [drawRadius, setDrawRadius] = useState(2);
  const [drawColor, setDrawColor] = useState([65, 230, 124]);
  const containerRef = useRef();

  const handleResize = useCallback(() => {
    const width = containerRef.current.clientWidth * 0.97;
    setScale(calculateScale(width));
  }, [containerRef]);

  useEffect(() => {
    const debouncedResize = debounce(handleResize, 100);
    window.addEventListener("resize", debouncedResize);
    return () => window.removeEventListener("resize", debouncedResize);
  }, [handleResize]);

  const clear = () => {
    fetch('/clear', {
      method: "GET"
    }).then(res => console.log(res));
  };

  const erasing = colorsEqual(drawColor, [0, 0, 0]);

  return <div className="draw" ref={containerRef}>
    <LedBoard scale={scale}
              drawRadius={drawRadius} drawColor={drawColor}
              socket={props.socket}/>
    <div className="draw-settings">
      <div>
        <TwitterPicker color={{r: drawColor[0], g: drawColor[1], b: drawColor[2]}}
                       onChange={clr => setDrawColor([clr.rgb.r, clr.rgb.g, clr.rgb.b])}/>
      </div>
      <div className="settings-group">
        <p>Brush Size</p>
        <Slider value={drawRadius} onChange={setDrawRadius} min={1} max={10}/>
      </div>
      <div className="settings-group button-group">
        <Button type={erasing ? "dashed" : "default"} onClick={() => setDrawColor([0, 0, 0])}>Erase</Button>
        <Button onClick={clear}>Clear</Button>
      </div>
    </div>
  </div>

}

export default DrawMode;
