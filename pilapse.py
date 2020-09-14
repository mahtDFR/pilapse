from picamera import PiCamera
import time, os

# interval in minutes
interval_mins = 1

interval = interval_mins * 60
camera = PiCamera()
camera.rotation = 180
outfile = "render.mkv"

def mkdirs():
    name = "pilapse_images"
    dir = os.getcwd() + "/" + name
    check_folder = os.path.isdir(dir)
    if not check_folder:
        os.mkdir(dir)
        print("folder created:", dir)
    return dir

def filecount():
    dir = mkdirs()
    path, dirs, files = next(os.walk(dir))
    file_count = len(files)
    return str(file_count)

def frame():
    dir = mkdirs()
    # camera.start_preview()
    # time.sleep(3)
    file_count = filecount()
    target = dir + "/frame_" + file_count.zfill(7) + ".jpg"
    camera.capture(target)
    # camera.stop_preview()
    print("image saved:", target)

def render():
    dir = mkdirs()
    input = str(dir)
    print("encoding video...")
    # ffmpegcmd = "ffmpeg -y -i " + input + "/frame_%07d.jpg -c:v libx264 -preset ultrafast -crf 0 render.mkv"
    # ffmpegcmd = "ffmpeg -hide_banner -loglevel panic -y -i " + input + "/frame_%07d.jpg -c:v libx264 -preset ultrafast -crf 0 " + outfile
    ffmpegcmd = "ffmpeg -hide_banner -loglevel panic -y -i " + input + "/frame_%07d.jpg -c:v libx264 -preset ultrafast -crf 0 -filter:v fps=fps=25 " + outfile
    os.system(ffmpegcmd)
    print("done.")


def play():
    render = os.getcwd() + "/" + outfile
    silent = " > /dev/null 2>&1"
    playercmd = "mplayer " + render + silent
    print("playing video so far...")
    os.system(playercmd)

while True:
    mkdirs()
    frame()
    render()
    play()
    print("waiting for next frame...")
    time.sleep(interval)
    # time.sleep(10)



