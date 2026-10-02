# Drowsiness and Yawn Detection

A Windows webcam script that estimates eye aspect ratio (EAR) and mouth opening from dlib's 68 facial landmarks, then displays alerts for detected drowsiness or yawning.

## Requirements

- Windows
- Python 3.14 (the pinned `dlib-bin` build is for this environment)
- A webcam
- The dlib 68-point facial landmark model
- A WAV file for the alert sound

## Setup

Open PowerShell in this project folder and create a virtual environment:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Download the dlib landmark model from [dlib's model downloads](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2), extract the `.bz2` archive, and place `shape_predictor_68_face_landmarks.dat` in this folder. Review the model's terms before redistribution or commercial use; this repository ignores the model file by default.

Place a WAV audio file named `alert.wav` in this folder. The audio file is also ignored by Git by default.

## Run

```powershell
python .\prj.py
```

If the files are stored elsewhere, provide their paths:

```powershell
python .\prj.py --predictor "C:\path\to\shape_predictor_68_face_landmarks.dat" --alert-sound "C:\path\to\alert.wav"
```

Press `q` while the video window is focused to quit.

## Push to GitHub

Create an empty repository on GitHub, then run these commands from this folder. Replace the URL with your repository URL:

```powershell
git init -b main
git add prj.py README.md requirements.txt .gitignore
git commit -m "Add drowsiness detection project"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

The model and WAV alert are intentionally excluded from Git. Do not commit files unless you have permission to redistribute them.
