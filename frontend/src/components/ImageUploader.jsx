import React from "react";

function ImageUploader(props) {

  const imageHandler = event => {
    console.log("ImageUploader Handler invoked");
    const width = 64;
    const height = 32;
    const ctx = document.createElement("canvas").getContext('2d');
    const url = URL.createObjectURL(event.target.files[0]);
    const img = new Image();
    img.onload = function() {
      ctx.drawImage(img, 0, 0, width, height);
      console.log("Draw complete");
      const data = ctx.getImageData(0, 0, width, height).data;
      callApi(data).then(success => console.log(success));
    };
    img.src = url;
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
    <input type="file" accept="image/*" onChange={imageHandler}/>
  </div>

}

export default ImageUploader
