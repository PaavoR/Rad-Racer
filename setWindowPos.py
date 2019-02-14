
from gi.repository import Gtk, Wnck

Gtk.init([])  # necessary only if not using a Gtk.main() loop
screen = Wnck.Screen.get_default()
screen.force_update()  # recommended per Wnck documentation

# loop all windows
for window in screen.get_windows():
    name = window.get_name()
    print (name)
    if name == "Rad Racer (U)":
        print("Right window founded")
        window.set_geometry(0,Wnck.WindowMoveResizeMask.X | \
                          Wnck.WindowMoveResizeMask.Y | \
                          Wnck.WindowMoveResizeMask.WIDTH | \
Wnck.WindowMoveResizeMask.HEIGHT,100,100,800,600)

    # ... do whatever you want with this window

# clean up Wnck (saves resources, check documentation)
window = None
screen = None
Wnck.shutdown()