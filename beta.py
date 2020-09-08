from colored import fg, bg, attr, stylize

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

def print_vertical_bar(n: int) -> str:
    results = []
    fb = '▓▓▓▓▓▓▓▓▓'
    eb = '░░░░░░░░░'
    for i in range(n):
        results.append(fb)
    for i in range(10 - n):
        results.append(eb)
    return f'''
        {results[7]}                    {' '}
        {results[6]}  root
        {results[5]}
        {results[4]}  Total: 100 GB
        {results[3]}  Used: 60 GB
        {results[2]}  FREE: 40 GB
        {results[1]}  60% Usage
        {results[0]}
    '''

print(print_vertical_bar(6))
print(print_vertical_bar(3))

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