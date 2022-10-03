import React from "react";
import Player from "../components/player/Player";
import { v1 as uuidv1 } from "uuid";

class Monitor extends React.Component {
  mediaServerUrl = "http://localhost:8080";
  state = {
    streamers: [],
  };

  addPlayer = (streamUrl) => {
    this.setState((state) => {
      return { streamers: [...state.streamers, { id: uuidv1(), streamUrl: streamUrl }] };
    });
  };

  render() {
    return (
      <div>
        <button onClick={this.addPlayer}>add</button>
        <div id="Monitor">
          {this.state.streamers.map(({ id, streamUrl }) => (
            <Player key={id} streamUrl={streamUrl} serverUrl={this.props.serverUrl} mediaServerUrl={this.mediaServerUrl}></Player>
          ))}
        </div>
      </div>
    );
  }
}

export default Monitor;
