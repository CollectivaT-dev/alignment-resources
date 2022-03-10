# Alignment resources
This is a repository of scripts for a long audio alignment pipeline. It
basically puts multiple tools together, and launches them for a specific
directory structure of text and audio files. Instructions are prepared for
judeo-spanish (ladino), but it can work for any language given that there are
alignment models for them.

# Installation
Alignment resources consists of scripts plus two submodules, STT-align which
uses Coqui TTS to do alignment and num2word-multilang for normalizing the
numbers. 

In order to clone with all the submodules:
```
git clone --recurse-submodules https://github.com/CollectivaT-dev/alignment-resources.git
```

After create a virtualenvironment and install all the requirements
```
python -m venv venv
source venv/bin/activate
python -m pip install -U pip
python -m pip install -r num2word/requirements.txt
python -m pip install -r STT-align/requirements.txt
```

`num2word` needs apertium to run, since it first converts the numbers to words
in English and then translates them to the desired language. Hence that should
be installed locally

```
sudo apt install apertium apertium-en-es apertium-en-ca
```

Finally we need to download the desired STT model of Coqui from
[here](https://coqui.ai/models). Preferebly can be put to the path
`STT-align/models/xx`.

A note on the Spanish model, the alphabet file of the model downloaded from
Coqui might not be correct (missing the accented letters). For a better
alignment please use the alphabet file in `resources/es/alphabet.txt`

```
cp resources/es/alphabet.txt STT-align/models/es/
```

Document conversion is done using libreoffice command-line tools. To install:

```
sudo apt install libreoffice-common
sudo apt-get install libreoffice-writer
```

# Data preparation
The `scripts/launch.py` script looks for directories in `raw`, which each
directory would have an audio file and a doc(x) file with its transcriptions.
Then the script checks if there are corresponding directries in `process` and
if not processes them. 

For example:
```
raw/
├── karen_artikolo01
│   ├── 1 Karen Amaneser 200 baş yazı.wav
│   └── 1 Karen Ya yegimos al numero 200.docx
├── karen_artikolo02
│   ├── 2 grosman AMAN 2021 Ekim kontrol edilid karen.doc
│   └── 2 Moşe Grosman Amaneser 200.wav
├── karen_artikolo03
│   ├── 3 ALDO SEVİ AMANESER 200.wav
│   └── 3 Aldo SEVI - para el Amaneser 200 kontrol edildi karen.docx
├── karen_artikolo04
│   ├── 4 MIRIAM RAYMOND AMANESER 200.wav
│   └── 4 myriam raymond ARTICOLO kontrol edildi karen 636.docx
└── karen_artikolo05
    ├── 5 EDMOND COHEN AMANESER 200.wav
    └── 5 Edmond El 5 de Novyembre 1942 15 11 12 - 1831 kontrol edildi karen.docx
```

If launched, `python/launch.py` generates:
```
process
├── karen_artikolo01
│   └── wav
│       ├── karen_artikolo01_norm.txt
│       ├── karen_artikolo01.txt
│       └── karen_artikolo01.wav
├── karen_artikolo02
│   └── wav
│       ├── karen_artikolo02_norm.txt
│       ├── karen_artikolo02.txt
│       └── karen_artikolo02.wav
├── karen_artikolo03
│   └── wav
│       ├── karen_artikolo03_norm.txt
│       ├── karen_artikolo03.txt
│       └── karen_artikolo03.wav
├── karen_artikolo04
│   └── wav
│       ├── karen_artikolo04_norm.txt
│       ├── karen_artikolo04.txt
│       └── karen_artikolo04.wav
└── karen_artikolo05
    └── wav
        ├── karen_artikolo05_norm.txt
        ├── karen_artikolo05.txt
        └── karen_artikolo05.wav
```
The `_norm.txt` are the versions of the text that have numbers normalized
(written with letters). 

# Alignment
Currently the alignment is not automatized, because each file might need
tuning. Before launching the alignment please check if Coqui STT is installed
correctly and `align.py` launches.

```
stt -h
python STT-align/align/align.py -h
```

It is preferable to have all the alignment files in the `aligned` folder, and the logs in `logs` folder. Hence an example alignment task is launched by:

```
python STT-align/align/align.py --audio process/karen_artikolo01/wav/karen_artikolo01.wav --script process/karen_artikolo01/wav/karen_artikolo01_norm.txt --aligned aligned/karen_artikolo01_aligned.json --tlog logs/karen_artikolo01.log --stt-model-dir STT-align/models/es --output-pretty
```

This generates a single json file in the aligned folder. By using that and the audio file, the audio segments can be created.

# Segmentation

Altough generic the `STT-align/scripts/segment.py` is designed to work with [label-studio](https://github.com/heartexlabs/label-studio) and generate a `task.json` that is importable to label-studio for quality control. 

```
python STT-align/scripts/segment.py aligned/karen_artikolo01_aligned.json process/karen_artikolo01/wav/karen_artikolo01.wav /home/baybars/label_data/karen_artikolo01
```
Command puts the segmented files to `/home/baybars/label_data/karen_artikolo01` for which the `/home/baybars/label_data/` is the locally configured label-studio directory. 
