import React, {useState} from "react";
import {Form, Input, Button} from "antd";
import ApiClient from "../api/Api";
import "antd/dist/antd.css";
import "../css/Panel.css";

function Panel(props) {

  const [text, setText] = useState("");

  return (
    <div className="panel">
      <h1>Scrolling Text</h1>
      <Form onSubmit={e => {
        e.preventDefault();
        ApiClient().displayText(text);
        setText("");
      }}>
        <Form.Item>
        <Input placeholder="NU Wireless!" value={text} onChange={e => setText(e.target.value)}/>
        <Button block type="primary" htmlType="submit">Go!</Button>
        </Form.Item>
      </Form>
    </div>
  )
}

export default Panel;
