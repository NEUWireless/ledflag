import React, {useRef, useState} from "react";
import { Form, Select } from 'antd';

const { Option } = Select;

function ImageUploader(props) {

  const WIDTH = 64;
  const HEIGHT = 32;

  const canvasRef = useRef();
  const [mode, setMode] = useState("stretch");
  const [sourceImage, setSourceImage] = useState(null);

  const onImageChange = event => {
    const img = new Image();
    img.onload = () => drawAndSend(img, canvasRef.current.getContext("2d"), mode);
    img.src = URL.createObjectURL(event.target.files[0]);
    setSourceImage(img);
  };

  const onModeChange = value => {
    setMode(value);
    if (sourceImage) {
      drawAndSend(sourceImage, canvasRef.current.getContext('2d'), value);
    }
  };

  const drawAndSend = (img, ctx, mode) => {
    draw(img, ctx, mode);
    const data = ctx.getImageData(0, 0, WIDTH, HEIGHT).data;
    callApi(data).then(success => console.log(success));
  };

  const draw = (img, ctx, mode) => {
    switch (mode) {
      case "fit":
        drawFit(img, ctx);
        break;
      default:
        drawStretch(img, ctx);
    }
  };

  const drawFit = (img, ctx) => {

    ctx.fillStyle = "rgb(0,0,0)";
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    const screenAspect = WIDTH / HEIGHT;
    const imgAspect = img.width / img.height;

    const scale = screenAspect > imgAspect ?
      HEIGHT / img.height : WIDTH / img.width;

    const dWidth = img.width * scale;
    const dHeight = img.height * scale;

    const dx = (WIDTH - dWidth) / 2;
    const dy = (HEIGHT - dHeight) / 2;

    ctx.drawImage(img, 0, 0, img.width, img.height, dx, dy, dWidth, dHeight);
  };

  const drawStretch = (img, ctx) => {
    ctx.drawImage(img, 0, 0, WIDTH, HEIGHT);
  };

  const callApi = async imageData => {
    const response = await fetch("/image", {
      method: "POST",
      body: JSON.stringify({
        data: Array.from(imageData)
      }),
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.ok;
  };

  return <div>
    <Form>
      <Form.Item>
        <input type="file" accept="image/*" onChange={onImageChange}/>
        <Select value={mode} onChange={onModeChange}>
          <Option value="stretch">Stretch</Option>
          <Option value="fit">Fit</Option>
        </Select>
      </Form.Item>
      <Form.Item>
        <canvas width={WIDTH} height={HEIGHT} ref={canvasRef}/>
      </Form.Item>
    </Form>
  </div>

}

export default ImageUploader
