import libxmplite

print("Supported module formats: ", libxmplite.get_formats())

xmp = libxmplite.Xmp()
xmp.load("jt-pools.xm")
xmp.start(44100)

info = xmp.module_info()    # grab name, comment, number of patterns, ....

frame_info = xmp.play_frame()

# ... process the frame buffer bytes ...
# ... repeat until satisfied

xmp.release()