import React from "react";

class Player extends React.Component {
  playStream(streamUrl) {
    setupEyevinnPlayer("player-wrapper", streamUrl).then(function (player) {
      let muteOnStart = true;
      player.play(muteOnStart);
    });
  }

  connectStream(sourceStreamUrl) {
    console.log("Stream Connect.");

    fetch(`${this.props.serverUrl}/stream/start`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        sourceUrl: sourceStreamUrl,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        console.debug(res);
        let streamUrl = `${this.props.mediaServerUrl}/hls/${res.channelName}/index.m3u8`;
        console.log(`Success to connect stream from ${streamUrl}`);
        this.playStream(streamUrl);
      })
      .catch((err) => {
        console.error("Error stream connection.");
        console.error(err.stack);
      });
  }

  render() {
    return (
      <div className="Player">
        <div id="player-wrapper"></div>
        {this.connectStream(this.props.streamUrl)}
      </div>
    );
  }
}

export default Player;
