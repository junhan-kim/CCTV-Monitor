import pafy
import cv2
import sys
import ffmpeg


server_url = "rtmp://localhost/show"


def start_streaming(width, height):
    process = (
        ffmpeg
        .input('pipe:', format='rawvideo', codec="rawvideo", pix_fmt='bgr24', s='{}x{}'.format(width, height))
        .output(
            server_url + '/stream',
            # codec = "copy", # use same codecs of the original video
            listen=1,  # enables HTTP server
            pix_fmt="yuv420p",
            preset="ultrafast",
            f='flv'
        )
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    return process


pafy.set_api_key('AIzaSyC0i7Y_ss-OVPklVi4y7DcQssjDOnkBxHg')

# url = "https://www.youtube.com/watch?v=V71lWsCKtYI"
url = "https://www.youtube.com/watch?v=jD9XgQEWCcY"
# url = "https://www.youtube.com/watch?v=RBchZuDSMgM"

video = pafy.new(url)
best = video.getbest(preftype="mp4")

print(video.duration)
if video.duration == '00:00:00':
    print('live')
else:
    print('video')
    sys.exit(0)

print(best.url)

cap = cv2.VideoCapture(best.url)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

streaming_process = start_streaming(width, height)


while True:
    grabbed, frame = cap.read()
    if not grabbed:
        break

    streaming_process.stdin.write(frame.tobytes())
    # cv2.imshow(__file__, frame)
    # cv2.waitKey(fps)


streaming_process.stdin.close()
streaming_process.wait()
cap.release()
