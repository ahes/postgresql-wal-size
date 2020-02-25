# PostgreSQL WAL size

## Usage

```
usage: postgresql-wal-size.py [-h] [-c] [-r]

Calculates WAL size over time

optional arguments:
  -h, --help   show this help message and exit
  -c, --cron   Save output to a log file (/var/log/postgresql/wal-size.log)
  -r, --reset  Reset last position saved
```

## Sample output

When running from command line:

```
$ /usr/local/bin/postgresql-wal-size.py
2020-02-25 17:53:49   2708A/72290000   2708A/8D3FC000        454475776 bytes     0.42 GB
```

When running as cron job:

```
$ tail /var/log/postgresql/wal-size.log
2020-02-25 08:00:01   27073/C701FC58   27077/49956EA0      15075603016 bytes    14.04 GB
2020-02-25 09:00:01   27077/49956EA0   27079/D9791FC8      11003998504 bytes    10.25 GB
2020-02-25 10:00:01   27079/D9791FC8   2707B/DC996CD0       8642383112 bytes     8.05 GB
2020-02-25 11:00:01   2707B/DC996CD0   2707D/EBCE74A8       8845068248 bytes     8.24 GB
2020-02-25 12:00:01   2707D/EBCE74A8   2707F/BEAF4088       7832914912 bytes     7.29 GB
2020-02-25 13:00:01   2707F/BEAF4088   27081/6C65A668       7209379296 bytes     6.71 GB
2020-02-25 14:00:01   27081/6C65A668   27083/53C59CF0       8176793224 bytes     7.62 GB
2020-02-25 15:00:01   27083/53C59CF0   27085/5927DC00       8680259344 bytes     8.08 GB
2020-02-25 16:00:01   27085/5927DC00   27087/1B2B6000       7549977600 bytes     7.03 GB
2020-02-25 17:00:01   27087/1B2B6000   27088/DD9F9E78       7557365368 bytes     7.04 GB
```

## Crontab

Run every hour:

```
0 * * * * postgres timeout 60 /usr/local/bin/postgresql-wal-size.py --cron
```

When using `--cron` output will be saved to `/var/log/postgresql/wal-size.log`

