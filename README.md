# open-vn-en-dict

## Virtual environment
```sh
python3 -m venv env
```
then active virtual environment
```
source env/bin/activate
```

## Install dependencies
```

pip install -r requirements.txt

```

## Run
```sh
python3 main.py
```

## Git commit
To avoid slow git commit because huge number of file run below command during script running 

```sh
watch  -n 30 "git add --all; git commit  -m \"Update Json\"; git push"