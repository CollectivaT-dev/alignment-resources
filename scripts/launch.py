import os
import re
import sys
import subprocess

FILEPATH = os.path.dirname(os.path.realpath(__file__))
RAW_PATH = os.path.join(FILEPATH, '../raw')
PROC_PATH = os.path.join(FILEPATH, '../process')
N2W_PATH = os.path.join(FILEPATH, '../num2word')

def main():
    '''Checks the path raw compares it to process
       for the directories that don't exist it does the pre-processing
    '''
    raw_dirs = set([convert(d) for d in os.listdir(RAW_PATH)])
    raw_dirs_dict = {convert(d):d for d in os.listdir(RAW_PATH)}
    proc_dirs = get_processed_dirs(PROC_PATH, '.wav')
    missing_dirs = list(raw_dirs.difference(proc_dirs))
    print(missing_dirs)
    for directory in missing_dirs:
        print(directory)
        process(raw_dirs_dict[directory], directory)

    norm_dirs = get_processed_dirs(PROC_PATH, '_norm.txt')
    missing_norm_dirs = list(raw_dirs.difference(norm_dirs))
    for directory in missing_norm_dirs:
        print('normalizing text of %s'%(directory))
        text_source = os.path.join(PROC_PATH, directory, 'wav',
                                   directory+'.txt')
        text_target = text_source.replace('.txt', '_norm.txt')
        args = ['python',os.path.join(N2W_PATH, 'num2word_multilang.py'),
                '-i', text_source, '-o', text_target, '-l', 'lad']
        subprocess.call(args)

def convert(string):
    return string.replace(' ','_').lower()

def get_processed_dirs(top_path, query):
    paths = os.listdir(top_path)
    dirs = []
    for path in paths:
        if os.path.isfile(os.path.join(top_path, path,
                                       'wav', path+query)):
            dirs.append(path)
    return dirs

def process(in_dir, out_dir):
    '''Create MFA compatible dir, convert the doc files 
and the wav files
    '''
    rel_in_dir = os.path.join(RAW_PATH, in_dir)
    rel_out_dir = os.path.join(PROC_PATH, out_dir, 'wav')
    rel_ali_dir = os.path.join(PROC_PATH, out_dir, 'alignment')
    if not os.path.isdir(rel_out_dir):
        os.makedirs(rel_out_dir)
    doc_file, wav_file = get_doc_wav(rel_in_dir)
    convert_doc(doc_file, rel_out_dir, out_dir+'.txt')
    convert_wav(wav_file, rel_out_dir, out_dir+'.wav')

def get_doc_wav(path):
    for f in os.listdir(path):
        f_low = f.lower()
        f_path = os.path.join(path, f)
        if f_low.endswith('doc') or f_low.endswith('docx'):
            doc = f_path
        elif f_low.endswith('wav') or f_low.endswith('mp3'):
            wav = f_path
    return doc, wav

def convert_doc(doc_file, out_dir, filename):
    args = ['soffice', '--headless', '--convert-to', 'txt', doc_file,
            '--outdir', out_dir]
    subprocess.call(args)
    # Assumes there only one txt file exists
    txt = [f for f in os.listdir(out_dir) if f.endswith('txt')][0]
    conv_file_path = os.path.join(out_dir, txt)
    with open(conv_file_path) as conv_file,\
         open(os.path.join(out_dir, filename), 'w') as final_file:
        clean_text = clean(conv_file.read())
        final_file.write(clean_text)
    os.remove(conv_file_path)

def clean(text):
    text = re.sub('\ufeff| {2,}|\t', ' ', text)
    text = re.sub('\n{2,}', '\n', text)
    text = re.sub('\w\w\d\d\d.+', '', text)
    return text

def convert_wav(wav_file, out_dir, filename):
    out_filepath = os.path.join(out_dir, filename)
    args = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'panic',\
            '-i', wav_file, '-ac', '1', '-ar', '16000', out_filepath]
    subprocess.call(args)

if __name__ == "__main__":
    main()
