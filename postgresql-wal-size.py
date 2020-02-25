#!/usr/bin/env python3
#
# Calculates WAL size over time
# Use '--cron' to run from crontab
#
import psycopg2
import os
import sys
import re
import argparse
from datetime import datetime

# Configuration
POS_FILE = "/var/tmp/wal-size.pos"
LOG_FILE = "/var/log/postgresql/wal-size.log"
POSTGRES_CONNECTION = "user=postgres"

# CLI arguments
parser = argparse.ArgumentParser(
    description='Calculates WAL size over time')
parser.add_argument('-c', '--cron', action='store_true', default=False,
                    help='Save output to a log file ({})'.format(LOG_FILE))
parser.add_argument('-r', '--reset', action='store_true',
                    default=False, help='Reset last position saved')
args = parser.parse_args()

# Postgresql connection
conn = psycopg2.connect(POSTGRES_CONNECTION)
cur = conn.cursor()

# Get current log position
cur.execute("SELECT pg_current_wal_lsn()")
current_pos = cur.fetchone()[0]

# Get last log position
if os.path.exists(POS_FILE) and not args.reset:
    with open(POS_FILE, 'r') as f:
        last_pos = f.readline().strip()
else:
    with open(POS_FILE, 'w') as f:
        f.write(current_pos)
        sys.exit(0)

# Check last log position
pos_pattern = re.compile('^[A-F0-9]+/[A-F0-9]+$')
if not pos_pattern.match(last_pos):
    raise ValueError("Last log position ('{}') found in '{}' does not match pattern".format(
        last_pos, POS_FILE))

# Calculate log size
cur.execute("SELECT pg_wal_lsn_diff(%s, %s)", (current_pos, last_pos))
pos_diff_bytes = cur.fetchone()[0]
pos_diff_gb = float(pos_diff_bytes / 1024 / 1024 / 1024)

# Save last log position
with open(POS_FILE, 'w') as f:
    f.write(current_pos)

# Output
output = "{:%Y-%m-%d %H:%M:%S} {:>16s} {:>16s} {:>16.0f} bytes {:>8.2f} GB\n".format(
    datetime.now(),
    last_pos, current_pos,
    pos_diff_bytes, pos_diff_gb)

if args.cron:
    with open(LOG_FILE, 'a+') as f:
        f.write(output)
else:
    print(output, end='')
