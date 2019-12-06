function ApiClient() {

  const request = (url, method, params={}) => {
    const init = { method };
    if (method === "POST") {
      init.headers = {"Content-Type": "application/json"};
      init.body = JSON.stringify(params);
    }
    else if (method === "GET") {
      url += '?' + Object.keys(params).filter(k => params[k]).map(
        k => {
          const value = params[k];
          return encodeURIComponent(k) + "=" + encodeURIComponent(value);
        }
      ).join('&');
    }
    return fetch(url, init);
  };

  const displayText = (text, scrolling=true) => {
    request(scrolling ? "/scrolltext" : "/displaytext", "GET", {text})
      .then(res => console.log(res));
  };

  return { displayText };

}

export default ApiClient;
