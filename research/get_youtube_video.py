import pafy
import cv2

url = "https://www.youtube.com/watch?v=V71lWsCKtYI"
video = pafy.new(url)
best = video.getbest(preftype="mp4")

capture = cv2.VideoCapture(best.url)
while True:
    grabbed, frame = capture.read()
    if not grabbed:
        break
    cv2.imshow(__file__, frame)
    cv2.waitKey(1)