"""Convert an SVG file or folder content to PNG."""

import glob
import subprocess
import os.path as path
from os import getcwd
from argparse import ArgumentParser

def main():
    args = parse_args()
    export_width, export_height = args.size.split('x')
    dir_path = getcwd()
    if path.isdir(args.input):
        files = glob.glob(args.input + "/*.svg")
        for in_file in files:
            out_file = path.join(dir_path, path.splitext(path.basename(in_file))[0] + '.png')
            convert_with_inkscape(in_file, out_file, export_width, export_height)
    else:
        out_file = path.splitext(path.basename(args.input))[0] + '.png'
        convert_with_inkscape(args.input, out_file, export_width, export_height)

def convert_with_inkscape(in_file, out_file, export_width=128, export_height=128):
    try:
        inkscape_path = subprocess.check_output(["which", "inkscape"]).strip()
    except subprocess.CalledProcessError:
        raise SystemExit("ERROR: Inkscape needs to be installed to use this script.")

    args = [
        inkscape_path,
        "--without-gui",
        "-f", in_file,
        "--export-area-page",
        "-w", export_width,
        "-h", export_height,
        "--export-png=" + out_file
    ]
    subprocess.check_call(args)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('input', help="SVG file/folder to open")
    parser.add_argument('-s', '--size', required=True, help="Target size to render in format 'WxH'")
    return parser.parse_args()

if __name__ == '__main__':
    main()
