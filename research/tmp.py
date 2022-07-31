import m3u8
import requests
import cv2
# res = requests.get(
#     'https://openapi.its.go.kr:9443/cctvInfo?apiKey=044cd0c0407245a4bb5d2f6d1d8458bd&type=ex&cctvType=1&minX=127.100000&maxX=128.890000&minY=34.100000&maxY=39.100000&getType=json')
# print(res.json())

# this could also be an absolute filename
# playlist = m3u8.load(
#     'http://cctvsec.ktict.co.kr/6/dtEs+zn2rSEjTaS/tWBneIfmBdLGO8AAmKqgfQHvPyOy3PpqYBCgUXtIvjXwZqOg7DjJFuOd5CAvT2U11vlWaw==/playlist.m3u8')
# print(playlist.segments)
# print(playlist.target_duration)


url = "http://cctvsec.ktict.co.kr/6/dtEs+zn2rSEjTaS/tWBneIfmBdLGO8AAmKqgfQHvPyOy3PpqYBCgUXtIvjXwZqOg7DjJFuOd5CAvT2U11vlWaw==/playlist.m3u8"
cap = cv2.VideoCapture(url)
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(fps)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow(__file__, frame)
    delay = int(1/fps*1000)
    print(delay)
    cv2.waitKey(33)
