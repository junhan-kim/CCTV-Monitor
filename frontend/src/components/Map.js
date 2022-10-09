/* global kakao */
import React from "react";

class Map extends React.Component {
  mapRef = React.createRef();
  defaultLatitude = 33.450701;
  defaultLongitude = 126.570667;

  componentDidMount() {
    this.getLocation();
  }

  getLocation = () => {
    if (navigator.geolocation) {
      // GPS를 지원하면
      navigator.geolocation.getCurrentPosition(
        (position) => {
          // position 객체 내부에 timestamp(현재 시간)와 coords 객체
          const time = new Date(position.timestamp);
          console.log(position);
          console.log(`현재시간 : ${time}`);
          console.log(`latitude 위도 : ${position.coords.latitude}`);
          console.log(`longitude 경도 : ${position.coords.longitude}`);
          console.log(`altitude 고도 : ${position.coords.altitude}`);

          this.setMap(position.coords.latitude, position.coords.longitude);
        },
        (error) => {
          console.error(error);
          this.setMap(this.defaultLatitude, this.defaultLongitude);
        },
        {
          enableHighAccuracy: false,
          maximumAge: 0,
          timeout: Infinity,
        }
      );
    } else {
      alert("GPS를 지원하지 않습니다");
      this.setMap(this.defaultLatitude, this.defaultLongitude);
    }
  };

  setMap(latitude, longitude) {
    console.log(`Lat, Lng: ${latitude}, ${longitude}`);
    let container = this.mapRef.current; //지도를 담을 영역의 DOM 레퍼런스
    let options = {
      //지도를 생성할 때 필요한 기본 옵션
      center: new kakao.maps.LatLng(latitude, longitude), //지도의 중심좌표.
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
