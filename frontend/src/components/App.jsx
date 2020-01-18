import React, { useState } from 'react';
import {BrowserRouter as Router, Switch, Route, Link} from "react-router-dom";
import {Layout, Menu, Icon} from "antd";
import Panel from "./Panel.jsx";
import "antd/dist/antd.css";
import "../css/App.css";
import DrawCanvas from "./DrawCanvas";
import ImageUploader from "./ImageUploader";
import io from "socket.io-client";

const { Content, Sider } = Layout;

const socket = io();

function App() {

  const [sliderCollapsed, setSliderCollapsed] = useState(false);

  return (
    <Router>
      <Layout>
        <Sider collapsible collapsed={sliderCollapsed}
               onCollapse={setSliderCollapsed} className="sider">
          <div className="title">
            <h1>LED Flag</h1>
          </div>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1">
              <Link to="/draw">
              <Icon type="edit"/>
              <span>Draw</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="2">
              <Link to="/text">
              <Icon type="font-colors"/>
              <span>Text</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="3">
              <Link to="/pattern">
              <Icon type="border-outer"/>
              <span>Pattern</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="4">
              <Link to="/image">
              <Icon type="picture"/>
              <span>Image</span>
              </Link>
            </Menu.Item>
            <Menu.Item key="5">
              <Link to="/games">
              <Icon type="build"/>
              <span>Games</span>
              </Link>
            </Menu.Item>
          </Menu>
        </Sider>
        <Content className="content">
          <div className="panel-container">
            <Switch>
              <Route path="(/|/draw)">
                <DrawCanvas socket={socket}/>
              </Route>
              <Route path="/text">
                <Panel/>
              </Route>
              <Route path="/image">
                <ImageUploader/>
              </Route>
              <Route path="/(pattern|games)">
                <h1>Coming soon!™</h1>
              </Route>
              <Route>
                <h1>Page not found</h1>
              </Route>
            </Switch>
          </div>
        </Content>
      </Layout>
    </Router>
  )

}

export default App;
