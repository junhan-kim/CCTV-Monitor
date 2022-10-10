/* global kakao */
import React from "react";

class Map extends React.Component {
  constructor(props) {
    super(props);
    this.mapRef = React.createRef();
    this.defaultLatitude = 33.450701;
    this.defaultLongitude = 126.570667;
    this.defaultLevel = 3;
    this.openAPIurl = "https://openapi.its.go.kr:9443";
  }

  componentDidMount() {
    let map = this.setMap(this.defaultLatitude, this.defaultLongitude, this.defaultLevel);
    this.setCenterWithMyLocation(map);

    let openAPIurl = this.openAPIurl;
    let cctvMarkerImageUrl = "https://www.clipartmax.com/png/middle/58-586592_cctv-camera-icon-cctv-icon.png";

    // 지도 영역 변경시 이벤트 등록
    kakao.maps.event.addListener(map, "bounds_changed", function () {
      let bounds = map.getBounds();
      console.log(`bounds: ${bounds}`);
      let minLat = bounds.getSouthWest().getLat();
      let minLng = bounds.getSouthWest().getLng();
      let maxLat = bounds.getNorthEast().getLat();
      let maxLng = bounds.getNorthEast().getLng();

      // get cctv List in bounds
      console.log(`minLat: ${minLat}, maxLat: ${maxLat}, minLng: ${minLng}, maxLng: ${maxLng}`);
      let cctvInfoUrl = `${openAPIurl}/cctvInfo?apiKey=${process.env.REACT_APP_OPENAPI_ITS_KEY}&type=ex&cctvType=1&minX=${minLng}&maxX=${maxLng}&minY=${minLat}&maxY=${maxLat}&getType=json`;
      console.log(`cctvInfoUrl: ${cctvInfoUrl}`);

      fetch(cctvInfoUrl)
        .then((res) => res.json())
        .then((res) => {
          let cctvList = res.response.data;
          console.log(cctvList);
          if (typeof cctvList == "undefined") {
            return [];
          } else {
            return cctvList;
          }
        })
        .then((cctvList) => {
          for (let i = 0; i < cctvList.length; i++) {
            let lat = cctvList[i].coordy;
            let lng = cctvList[i].coordx;
            let latLng = new kakao.maps.LatLng(lat, lng);

            // draw markers
            let markerImage = new kakao.maps.MarkerImage(cctvMarkerImageUrl, new kakao.maps.Size(30, 30));
            let marker = new kakao.maps.Marker({
              position: latLng,
              image: markerImage,
            });

            marker.setMap(map);
          }
        });
    });
  }

  setCenterWithMyLocation = (map) => {
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

          map.setCenter(new kakao.maps.LatLng(position.coords.latitude, position.coords.longitude));
        },
        (error) => {
          console.error(error);
        },
        {
          enableHighAccuracy: false,
          maximumAge: 0,
          timeout: Infinity,
        }
      );
    } else {
      alert("GPS를 지원하지 않습니다");
    }
  };

  setMap(latitude, longitude, level) {
    console.log(`Lat, Lng: ${latitude}, ${longitude}`);
    let container = this.mapRef.current; //지도를 담을 영역의 DOM 레퍼런스
    let options = {
      //지도를 생성할 때 필요한 기본 옵션
      center: new kakao.maps.LatLng(latitude, longitude), //지도의 중심좌표.
      level: level, //지도의 레벨(확대, 축소 정도)
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
