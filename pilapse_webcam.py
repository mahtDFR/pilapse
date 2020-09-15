import time, os

# interval in minutes
interval_mins = 15

interval = interval_mins * 60
outfile = "render.mkv"

def mkdirs():
    name = "webcam_frames"
    dir = os.getcwd() + "/" + name
    check_folder = os.path.isdir(dir)
    if not check_folder:
        os.mkdir(dir)
        print("folder created:", dir)
        time.sleep(0.5)
    return dir

def filecount():
    dir = mkdirs()
    path, dirs, files = next(os.walk(dir))
    file_count = len(files)
    # return str(file_count)
    return file_count

def frame():
    dir = mkdirs()
    file_count = str(filecount())
    target = dir + "/frame_" + file_count.zfill(7) + ".jpg"
    args = " -loglevel panic"
    capture_cmd = "ffmpeg -f video4linux2 -i /dev/video0 -vframes 1 " + target

    # comment this out to debug
    capture_cmd = capture_cmd + args

    time.sleep(3)
    os.system(capture_cmd)
    print("image saved:", target)
    time.sleep(0.5)
    return args

def render():
    dir = mkdirs()
    input = str(dir)
    print("encoding video...")

    ffmpegcmd = "ffmpeg -y -i " + input + "/frame_%07d.jpg -preset ultrafast -pix_fmt yuv420p -filter:v fps=fps=25 " + outfile
    args = frame()

    # comment this out to debug
    ffmpegcmd = ffmpegcmd + args

    os.system(ffmpegcmd)
    print("render complete.")

def play():
    render = os.getcwd() + "/" + outfile
    playercmd = "omxplayer > /dev/null 2>&1 " + render + " --aspect-mode stretch --loop &"
    os.system(playercmd)

def stop():
    kill_player = "sudo killall -s 9 omxplayer.bin"
    os.system(kill_player)

while True:
    mkdirs()
    frame()
    file_count = filecount()

    if file_count < 25:
        pass
    else:
        render()
        stop()
        print("starting latest video")
        time.sleep(0.5)
        play()

    print("waiting for next frame...")
    # time.sleep(interval)
    time.sleep(10)