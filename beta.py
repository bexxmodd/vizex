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
    print('''
    ⠮⠩⠕⠉⠲⠭ Total
    ''')

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