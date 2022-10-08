import React from "react";

class Player extends React.Component {
  constructor(props) {
    super(props);
    console.log("player constructor called");

    this.serverUrl = "http://localhost:8989";
    this.mediaServerUrl = "http://localhost:8080";

    this.connectStream(this.props.streamUrl).then((streamUrl) => {
      this.playStream(streamUrl);
    });
  }

  async connectStream(sourceStreamUrl) {
    console.log("Stream Connect.");

    const res = await fetch(`${this.serverUrl}/stream/start`, {
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

  playStream(streamUrl) {
    setupEyevinnPlayer("player-wrapper", streamUrl).then(function (player) {
      let muteOnStart = true;
      player.play(muteOnStart);
    });
  }

  render() {
    return (
      <div className="Player">
        <div id="player-wrapper"></div>
      </div>
    );
  }
}

export default Player;
