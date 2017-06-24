import glob, sys, os, sched, time, random

# change every x second
period = 10

# command line to change wallpaper
command = "gsettings set org.gnome.desktop.background picture-uri '%s'"

# needed for gsettings to work
path_prefix = "file://"

# file extensions to search for
extensions = [
                "*.jpg",
                "*.JPG",
                "*.png",
                "*.PNG"
             ]

# path to search for
if len(sys.argv) >= 2:
    path = sys.argv[1]
else:
    path = os.environ['HOME'] + "/Pictures/"


# list of files
results = map(lambda extension: glob.glob(path + extension), extensions)

# flatten list
results = [item for sublist in results for item in sublist]

# remove duplicates
results = list(set(results))

s = sched.scheduler(time.time, time.sleep)
def change_wallpaper(sc): 

    # run wallpaper changing command
    os.system(command % (path_prefix + results[random.randint(0, len(results) - 1)]))

    s.enter(period, 1, change_wallpaper, (sc,))

s.enter(period, 1, change_wallpaper, (s,))
s.run()
