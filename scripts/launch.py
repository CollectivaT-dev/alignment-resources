import os
import sys

FILEPATH = os.path.dirname(os.path.realpath(__file__))
RAW_PATH = os.path.join(FILEPATH, '../raw')
PROC_PATH = os.path.join(FILEPATH, '../process')

def main():
    '''Checks the path raw compares it to process
       for the directories that don't exist it does the pre-processing
    '''
    raw_dirs = set([convert(d) for d in os.listdir(RAW_PATH)])
    raw_dirs_dict = {convert(d):d for d in os.listdir(RAW_PATH)}
    proc_dirs = set(os.listdir(PROC_PATH))
    missing_dirs = list(raw_dirs.difference(proc_dirs))
    print(missing_dirs, raw_dirs_dict)
    for directory in missing_dirs[:1]:
        print(directory)
        process(raw_dirs_dict[directory], directory)

def convert(string):
    return string.replace(' ','_').lower()

def process(in_dir, out_dir):
    '''Create MFA compatible dir, convert the doc files 
and the wav files
    '''
    rel_in_dir = os.path.join(RAW_PATH, in_dir)
    rel_out_dir = os.path.join(PROC_PATH, out_dir, 'wav')
    os.makedirs(rel_out_dir)
    doc_file, wav_file = get_doc_wav(rel_in_dir)
    convert_doc(doc_file, rel_out_dir, out_dir+'.txt')
    convert_wav(wav_file, rel_out_dir, out_dir+'.wav')

def get_doc_wav(path):
    for f in os.listdir(path):
        f_low = f.lower()
        if f_low.endswith('doc') or f_low.endswith('docx'):
            doc = f
        elif f_low.endswith('wav') or f_low.endswith('mp3'):
            wav = f
    return doc, wav

def convert_doc(doc_file, out_dir, filename):
    pass

def convert_wav(wav_file, out_dir, filename):
    pass

if __name__ == "__main__":
    main()
