import { useState, useEffect } from "react";
import logo from "./logo.svg";
import "./App.css";

const App = () => {
  const { token } = window.SERVER_DATA;
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${window.location.origin}/init`, {
      method: "POST",
      body: JSON.stringify({ token: token }),
      headers: { "Content-type": "application/json" },
    })
      .then((response) => {
        if (response.ok) return response.json();
        throw response;
      })
      .then((response) => {
        setData(response);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          {data ? (
            <span>
              Hello, <code>{data.user}</code>! <br />
            </span>
          ) : null}
          Edit <code>src/frontend/App.js</code> save to apply changes.
        </p>
      </header>
    </div>
  );
};

export default App;
