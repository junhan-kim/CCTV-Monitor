import React from "react";

class Player extends React.Component {
  playStream(streamUrl) {
    setupEyevinnPlayer("player-wrapper", streamUrl).then(function (player) {
      let muteOnStart = true;
      player.play(muteOnStart);
    });
  }

  componentDidMount() {
    this.playStream(this.props.streamUrl);
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
