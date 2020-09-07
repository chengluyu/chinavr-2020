#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""
import argparse
import shutil
import sounddevice as sd

usage_line = ' press <enter> to quit, +<enter> or -<enter> to change scaling '

try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 80


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def parse_args():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__ + '\n\nSupported keys:' + usage_line,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        '-b', '--block-duration', type=float, metavar='DURATION', default=50,
        help='block size (default %(default)s milliseconds)')
    parser.add_argument(
        '-c', '--columns', type=int, default=columns,
        help='width of spectrogram')
    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')
    parser.add_argument(
        '-g', '--gain', type=float, default=10,
        help='initial gain factor (default %(default)s)')
    parser.add_argument(
        '-r', '--range', type=float, nargs=2,
        metavar=('LOW', 'HIGH'), default=[100, 2000],
        help='frequency range (default %(default)s Hz)')
    args = parser.parse_args(remaining)
    low, high = args.range
    if high <= low:
        parser.error('HIGH must be greater than LOW')
    return parser, args, remaining


def create_gradient():
    # Create a nice output gradient using ANSI escape sequences.
    # Stolen from https://gist.github.com/maurisvh/df919538bcef391bc89f
    colors = 30, 34, 35, 91, 93, 97
    chars = ' :%#\t#%:'
    gradient = []
    for bg, fg in zip(colors, colors[1:]):
        for char in chars:
            if char == '\t':
                bg, fg = fg, bg
            else:
                gradient.append('\x1b[{};{}m{}'.format(fg, bg + 10, char))
    return gradient
