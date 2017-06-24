import glob, sys, os, sched, time, random

# change every x second
period = 10

# command line to change wallpaper
commands = [
               "gsettings set org.gnome.desktop.background picture-options 'fill'",     # wallpaper mode: fill, centered, ..
               "gsettings set org.gnome.desktop.background picture-uri '%s'"            # %s will be replaced with image path
           ]

# needed for gsettings to work
path_prefix = "file://"

# file extensions to search for
extensions = [
                "*.jpg",
                "*.JPG",
                "*.png",
                "*.PNG"
             ]

# path to search for give command line arguments
if len(sys.argv) >= 2:
    path = sys.argv[1]
else:
    path = os.environ['HOME'] + "/Pictures/"    # default path /home/amir/Pictures/


# list of files
results = map(lambda extension: glob.glob(path + extension), extensions)

# flatten list
results = [item for sublist in results for item in sublist]

# remove duplicates
results = list(set(results))

s = sched.scheduler(time.time, time.sleep)
def change_wallpaper(sc): 

    # random image path
    rand_image_path = (path_prefix + results[random.randint(0, len(results) - 1)])
    
    # run wallpaper changing command
    map(lambda command: os.system((command % rand_image_path) if "%s" in command else (command)), commands)
    
    # reschedule the function to run
    s.enter(period, 1, change_wallpaper, (sc,))

s.enter(period, 1, change_wallpaper, (s,))
s.run()
