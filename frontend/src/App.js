import React from "react";
import Monitor from "./views/Monitor";

const serverUrl = "http://localhost:8989";

function App() {
  return (
    <div className="App">
      <Monitor serverUrl={serverUrl}></Monitor>
    </div>
  );
}

export default App;
