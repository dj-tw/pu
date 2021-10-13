import cProfile
import sys


def run_python_script(script_name, args, profiler=False):
    if profiler:
        print("running with profiler")

    if script_name == "pipeline":
        from scripts import pipeline as script
    else:
        message = "Script_name (%s) unknown" % script_name
        raise ValueError(message)

    if profiler:
        command = "script.main(*args)"
        filename = "%s.prof" % script_name
        cProfile.runctx(command, None, locals(), filename=filename)
        print("To see profiler result, run:\nsnakeviz %s" % filename)
    else:
        script.main(*args)


if __name__ == "__main__":
    profiler = ' -p' in ' '.join(sys.argv)
    script_name = sys.argv[1]
    args = sys.argv[2:]
    # remove the profile flag
    args = [i for i in args if i != '-p']

    run_python_script(script_name, args, profiler=profiler)
