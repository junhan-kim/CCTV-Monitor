/* global kakao */
import React from "react";

class Map extends React.Component {
  mapRef = React.createRef();

  componentDidMount() {
    this.setMap();
  }

  setMap() {
    let container = this.mapRef.current; //지도를 담을 영역의 DOM 레퍼런스
    let options = {
      //지도를 생성할 때 필요한 기본 옵션
      center: new kakao.maps.LatLng(33.450701, 126.570667), //지도의 중심좌표.
      level: 3, //지도의 레벨(확대, 축소 정도)
    };
    let map = new kakao.maps.Map(container, options); //지도 생성 및 객체 리턴
    return map;
  }

  render() {
    return (
      <div>
        <div id="map" ref={this.mapRef} style={{ width: "500px", height: "400px" }}></div>
      </div>
    );
  }
}

export default Map;
