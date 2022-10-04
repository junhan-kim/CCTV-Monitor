import React from "react";
import Player from "../components/player/Player";
import { v1 as uuidv1 } from "uuid";

class Monitor extends React.Component {
  mediaServerUrl = "http://localhost:8080";
  state = {
    streamers: [],
  };
  streamUrlRef = React.createRef();

  async connectStream(sourceStreamUrl) {
    console.log("Stream Connect.");

    const res = await fetch(`${this.props.serverUrl}/stream/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sourceUrl: sourceStreamUrl,
      }),
    });
    const data = await res.json();
    let streamUrl = `${this.mediaServerUrl}/hls/${data.channelName}/index.m3u8`;
    console.log(`Success to connect stream from ${streamUrl}`);
    return streamUrl;
  }

  addPlayer = () => {
    let srcStreamUrl = this.streamUrlRef.current.value;
    console.log(`stream connecting => ${srcStreamUrl}`);
    let streamUrl = this.connectStream(srcStreamUrl);
    console.log(`stream is connected => ${streamUrl}`);
    this.setState((state) => {
      return { streamers: [...state.streamers, { id: uuidv1(), streamUrl: streamUrl }] };
    });
  };

  render() {
    return (
      <div>
        <input type="text" ref={this.streamUrlRef}></input>
        <button onClick={this.addPlayer}>add</button>
        <div id="Monitor">
          {this.state.streamers.map(({ id, streamUrl }) => (
            <Player key={id} streamUrl={streamUrl}></Player>
          ))}
        </div>
      </div>
    );
  }
}

export default Monitor;
