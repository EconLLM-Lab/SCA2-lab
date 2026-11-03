"""Abstract body word count (tokens; hyphenated words count once). Usage: python3 voice_pass/abstract_words.py [--rev HEAD]"""
import re, subprocess, sys
def body(t):
    t = t.split('\\begin{abstract}')[1].split('\\end{abstract}')[0].replace('\\noindent', '')
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-]*", t)), len(t.split())
if '--rev' in sys.argv:
    t = subprocess.run(['git', 'show', sys.argv[-1] + ':misc/paper_b/abstract.tex'], capture_output=True, text=True).stdout
else:
    t = open('abstract.tex').read()
tok, ws = body(t)
print(f"abstract words: {tok} (tokens), {ws} (whitespace split)")
