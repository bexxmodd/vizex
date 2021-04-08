import cProfile, pstats, io

def speedometer(fnc):

    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        return_value = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sort_by = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
        ps.print_stats()
        with open("profile_vixez1.txt", 'a') as f:
            f.write(s.getvalue())
        return return_value

    return wrapper
