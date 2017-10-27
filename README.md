# bmb

## Getting started

Assuming you have docker,

```bash
cp settings.example.py settings.py
# fill in settings in settings.py
docker run -v $(pwd):/src -it -P geritol/blackmamba
```

## Building

```bash
docker build -t <build-name> .
```