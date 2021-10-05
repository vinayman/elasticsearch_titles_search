import sys
import logging
import subprocess
import argparse
import signal
import time

from dashboard import config


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        help="The port on which to run the server",
        default=config.getint("ws", "port"),
    )
    parser.add_argument(
        "-H",
        "--host",
        help="Set the hostname on which to run the server",
        default=config.get("ws", "host"),
    )
    parser.add_argument(
        "-P",
        "--protocol",
        help="Set the communication protocol",
        default=config.get("ws", "protocol"),
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Use the server with Flask in debug mode",
        default=config.getboolean("ws", "debug"),
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        help="Number of workers to run",
        default=config.getint("ws", "workers"),
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        help="Number of threads to run",
        default=config.getint("ws", "threads"),
    )
    parser.add_argument(
        "-l",
        "--logfile",
        help="The logfile to store the logs",
        default=config.get("ws", "logfile"),
    )
    return parser


def run_server(args):
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        from dashboard.app import app

        app.run(host=args.host, port=args.port, debug=True)
    else:
        run_args = [
            "uwsgi",
            "--protocol",
            str(args.protocol),
            "--processes",
            str(args.workers),
            "--threads",
            str(args.threads),
            "--socket",
            args.host + ":" + str(args.port),
            "--module",
            "dashboard.app:app",
        ]
        if args.logfile:
            run_args.extend(["--logto", args.logfile])

        wsgi_proc = subprocess.Popen(run_args)

        def kill_proc(dummy_signum, dummy_frame):
            wsgi_proc.terminate()
            wsgi_proc.wait()
            sys.exit(0)

        signal.signal(signal.SIGINT, kill_proc)
        signal.signal(signal.SIGTERM, kill_proc)

        while True:
            time.sleep(1)
