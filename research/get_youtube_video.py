import pafy
import cv2
import sys


pafy.set_api_key('AIzaSyC0i7Y_ss-OVPklVi4y7DcQssjDOnkBxHg')

# url = "https://www.youtube.com/watch?v=V71lWsCKtYI"
# url = "https://www.youtube.com/watch?v=jD9XgQEWCcY"
url = "https://www.youtube.com/watch?v=jD9XgQEWCcY"

video = pafy.new(url)
best = video.getbest(preftype="mp4")

print(video.duration)
if video.duration == '00:00:00':
    print('live')
else:
    print('video')
    sys.exit(0)

capture = cv2.VideoCapture(best.url)
fps = int(capture.get(cv2.CAP_PROP_FPS))
while True:
    grabbed, frame = capture.read()
    if not grabbed:
        break
    cv2.imshow(__file__, frame)
    cv2.waitKey(fps)
    
    
# imshow 말고 hls 등 이용해서 인터넷에 뿌리기
# youtube api 받아서 fps 등 조절