import React from 'react';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";
import {Layout, Menu, Icon} from "antd";
import Panel from "./Panel.jsx";
import "antd/dist/antd.css";
import "../css/App.css";

const { Content, Sider } = Layout;

function App() {

  return (
    <Router>
      <Layout>
        <Sider trigger={null} collapsible className="sider">
          <div className="title">
            <h1>LED Flag Controller</h1>
          </div>
          <Menu theme="dark" mode="inline" defaultSelectedKeys={['1']}>
            <Menu.Item key="1">
              <Icon type="font-colors"/>
              <span>Text</span>
            </Menu.Item>
            <Menu.Item key="2">
              <Icon type="border-outer"/>
              <span>Pattern</span>
            </Menu.Item>
            <Menu.Item key="3">
              <Icon type="picture"/>
              <span>Image</span>
            </Menu.Item>
            <Menu.Item key="4">
              <Icon type="build" />
              <span>Games</span>
            </Menu.Item>
          </Menu>
        </Sider>
        <Content className="content">
          <Switch>
            <Route exact path="/">
              <div className="panel-container">
                <Panel/>
              </div>
            </Route>
          </Switch>
        </Content>
      </Layout>
    </Router>
  )

}

export default App;
