from colored import fg, bg, attr, stylize
import psutil

# apple = '''
#                        ./+o+-
#                  yyyyy- -yyyyyy+
#               ://+//////-yyyyyyo
#           .++ .:/++++++/-.+sss/`
#         .:++o:  /++++++++/:--:/-
#        o:+o+:++.`..```.-/oo+++++/
#       .:+o:+o/.          `+sssoo+/
#  .++/+:+oo+o:`             /sssooo.
# /+++//+:`oo+o               /::--:.
# +/+o+++`o++o               ++////.
#  .++.o+++oo+:`             %s/BBdHHh.
#       %s.+.o+oo:.          %s`oBBHHHH+
#        %s+.++o+o``-````%s.:ohdHHHHh+
#         %s`:o+++ `%soHHHHHHHHyo++os:
#           %s.o:$`.%ssyHHHHHHh/.oo++o`
#               %s/osyyyyyyo++%sooo+++/
#                   ````` +oo+++o:
#                          `oo++.
# ''' % (fg(1), fg(3), fg(1), fg(3), fg(1), fg(3), fg(1), fg(3), fg(1), fg(3), fg(1))
# print(apple)
def test():
    disks = {}
        # First append the root partition
    disks["root"] = {"total": psutil.disk_usage("/").total,
                        "used": psutil.disk_usage("/").used,
                        "free": psutil.disk_usage("/").free,
                        "fstype": psutil.disk_partitions(all=False)[0][2]}
    disk_parts = psutil.disk_partitions(all=True)
    for disk in disk_parts[:-1]:
        if 'media' in disk[1]:
            disks[disk[1].split('/')[-1]] = {"total": psutil.disk_usage(disk[1]).total,
                                            "used": psutil.disk_usage(disk[1]).used,
                                            "free": psutil.disk_usage(disk[1]).free,
                                            "fstype": disk.fstype}
    for i in disks:
        print(disks[i])

if __name__ == '__main__':
    test()

# from gi.repository import Gtk
# gset = Gtk.Settings.get_default ()
# themename = gset.get_property ("gtk-theme-name")
# cprov = Gtk.CssProvider.get_named (themename)
# print (cprov.to_string())

# "████████████████▒░░░░░░░░"
# print('\n', psutil.sensors_temperatures())
# print('\n', psutil.Process(5622).memory_info())

# print(os.path.abspath('../'))
# folder = os.listdir('.')
# for i in folder:
#     if os.path.isfile('./' + i):
#         print(f'file {i} is:', os.path.getsize('./' + i))