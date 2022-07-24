import pafy
import cv2
import sys
import subprocess


server_url = "rtmp://localhost/live/test"


def start_streaming(width, height):
    command = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', f'{width}x{height}',
               '-re',
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               '-preset', 'ultrafast',
               '-f', 'flv',
               f'{server_url}']

    proc = subprocess.Popen(command, stdin=subprocess.PIPE, shell=False)
    return proc


def init_video_stream():
    pafy.set_api_key('AIzaSyC0i7Y_ss-OVPklVi4y7DcQssjDOnkBxHg')


def connect_video_stream(source_url, ):
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
