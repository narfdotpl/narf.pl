from os.path import dirname, join, realpath

import json
import multiprocessing
import os
import subprocess


CURRENT_DIR = dirname(realpath(__file__))
REPLAY_DIR = join(CURRENT_DIR, 'replays')
PROTOCOL_DIR = join(CURRENT_DIR, 'heroprotocol')
XP_PATCH_VERSION = (2, 41, 0)


class GameMode:
    # https://github.com/ebshimizu/hots-parser/blob/aae1f1763bde61f617ee8ac3ca93a738d2b3ef2d/constants.js#L316
    AI = 50021
    Practice = 50041
    QuickMatch = 50001
    Brawl = 50031
    UnrankedDraft = 50051
    HeroLeague = 50061
    TeamLeague = 50071
    Custom = -1


def get_stdout(arguments):
    command = ['python', join(PROTOCOL_DIR, 'heroprotocol.py')] + arguments
    proc = subprocess.Popen(command, stdout=subprocess.PIPE)
    return proc.stdout


def get_replay_paths():
    for name in os.listdir(REPLAY_DIR):
        yield join(REPLAY_DIR, name)


def get_replay_header(replay_path):
    stdout = get_stdout(['--header', '--json', replay_path])
    header = json.load(stdout)
    return header


def get_replay_data(replay_path):
    stdout = get_stdout(['--header', '--initdata', '--trackerevents', '--json', replay_path])
    header = stdout.next()
    stdout.next()
    init = stdout.next()
    tracker_events = [line for line in stdout]

    return (
        json.loads(header),
        json.loads(init),
        tracker_events,
    )


def get_game_mode(init):
    return init['m_syncLobbyState']['m_gameDescription']['m_gameOptions']['m_ammId']


def get_version(header):
    v = header['m_version']
    return (v['m_major'], v['m_minor'], v['m_revision'])


def get_duration(lines):
    gates_open_gameloop = None
    gates_open_pattern = '"m_eventName": "GatesOpen"'

    # https://github.com/ebshimizu/hots-parser/blob/aae1f1763bde61f617ee8ac3ca93a738d2b3ef2d/constants.js#L241
    core_pairs = []
    core_names = [
        'KingsCore',
        'VanndarStormpike',
        'DrekThar',
    ]
    core_patterns = ['"m_unitTypeName": "%s"' % core for core in core_names]
    born_pattern = '"_event": "NNet.Replay.Tracker.SUnitBornEvent"'
    died_pattern = '"_event": "NNet.Replay.Tracker.SUnitDiedEvent"'

    def get_pair(data):
        return (data['m_unitTagIndex'], data['m_unitTagRecycle'])

    for line in lines:
        if gates_open_gameloop is None and gates_open_pattern in line:
            data = json.loads(line)
            gates_open_gameloop = data['_gameloop']

        if len(core_pairs) < 2 and born_pattern in line and any(pattern in line for pattern in core_patterns):
            data = json.loads(line)
            pair = get_pair(data)
            core_pairs.append(pair)

        if died_pattern in line:
            data = json.loads(line)
            pair = get_pair(data)
            if pair in core_pairs:
                fps = 16.0
                duration = (data['_gameloop'] - gates_open_gameloop) / fps
                return duration


def make_csv_line(replay_path):
    path = replay_path
    header, init, tracker_events = get_replay_data(path)

    mode = get_game_mode(init)
    if mode == GameMode.QuickMatch:
        mode_string = 'QM'
    elif mode == GameMode.TeamLeague:
        mode_string = 'TL'
    else:
        return None

    version = get_version(header)
    version_string = '.'.join(map(str, version))
    is_after_xp_changes = version >= XP_PATCH_VERSION
    duration = get_duration(tracker_events)

    return ','.join(map(str, [
        int(os.path.getmtime(path)),
        version_string,
        is_after_xp_changes,
        mode_string,
        duration,
        os.path.basename(path),
    ]))


# process replays in parallel
with multiprocessing.Manager() as manager:
    lines = manager.list()

    def append_line(path):
        line = make_csv_line(path)
        if line:
            lines.append(line)

    pool = multiprocessing.Pool(8)
    pool.map(append_line, get_replay_paths())
    pool.terminate()

    print 'time,version,after_xp_changes,mode,duration,replay'
    for line in sorted(lines):
        print line
