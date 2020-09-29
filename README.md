# getref
Download reference file (such as RIS) of paper you want, from scholar engines (such as ResearchGate)

# Environments
This is developed with Python 3.6.
Several dependencies are necessary to run this script.
* **bs4** to parse the html
* **fake-useragent** to acquire UserAgent

# Usage

## Command line

### Interactive

Directly run:
```shell
python main.py
```

The reference file will be saved to directory "./References" in default. You can change it accordding to the hint.

You can paste your wanted paper title or description to download reference file.

## from local file

Run
```shell
python main.py demo_titles.txt
```

You can download all reference files listed in the file.
