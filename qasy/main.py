from subprocess import Popen, PIPE
import requests
import webbrowser
import sys
import api_call
import yt_api_call

# dictionary of extensions and their languages
ext_dict = {'adb': 'Ada', 's': 'Assembler [GCC]', 'sh': 'Bash', 'bc': 'bc', 'bf': 'Brainf**k', 'c': 'C', 'cs': 'C# [Mono]', 'cpp': 'C++ 14 [GCC]', 'cli': 'CLIPS', 'clj': 'Clojure', 'cob': 'COBOL', 'lisp': 'Common Lisp [CLISP]', 'd': 'D [GDC]', 'ex': 'Elixir', 'erl': 'Erlang', 'fs': 'F#', '4th': 'Forth', 'f': 'Fortran', 'go': 'Go', 'groovy': 'Groovy', 'hs': 'Haskell', 'icn': 'Icon', 'i': 'Intercal', 'java': 'Java', 'js': 'JavaScript [SpiderMonkey]', 'kt': 'Kotlin', 'lua': 'Lua',
            'n': 'Nemerle', 'nice': 'Nice', 'Node.js': 56, 'm': 'Objective-C', 'ml': 'Ocaml', 'octave': 'Octave', 'Pascal [FPC]': 22, 'Pascal [GPC]': 2, 'pl': 'Perl 6', 'php': 'PHP', 'pike': 'Pike', 'pro': 'Prolog [SWI]', 'py': 'Python', 'r': 'R', 'rkt': 'Racket', 'rb': 'Ruby', 'rs': 'Rust', 'scala': 'Scala', 'scm': 'Scheme', 'scheme': 'Scheme [Chicken]', 'Scheme [Guile]': 33, 'sed': 'Sed', 'st': 'Smalltalk', 'sql': 'SQLite - queries', 'swift': 'Swift', 'tcl': 'Tcl', 'ts': 'TypeScript', 'vb': 'VB.NET'}

# Sphere engine language detection codes
lang_codes = {'Ada': 7, 'Assembler [GCC]': 45, 'Assembler [NASM 64bit]': 42, 'Assembler [NASM]': 13, 'AWK [GAWK]': 104, 'AWK [MAWK]': 105, 'Bash': 28, 'bc': 110, 'Brainf**k': 12, 'C': 11, 'C# [Mono]': 27, 'C++ 4.3.2': 41, 'C++ [GCC]': 1, 'C++ 14 [GCC]': 44, 'C99 strict': 34, 'CLIPS': 14, 'Clojure': 111, 'COBOL': 118, 'Common Lisp [CLISP]': 32, 'D [DMD]': 102, 'D [GDC]': 20, 'Elixir': 96, 'Erlang': 36, 'F#': 124, 'Forth': 107, 'Fortran': 5, 'Go': 114, 'Groovy': 121, 'Haskell': 21, 'Icon': 16, 'Intercal': 9, 'Java': 10, 'Java - legacy': 55, 'JavaScript [Rhino]': 35, 'JavaScript [SpiderMonkey]': 112,
              'Kotlin': 47, 'Lua': 26, 'Nemerle': 30, 'Nice': 25, 'Node.js': 56, 'Objective-C': 43, 'Ocaml': 8, 'Octave': 127, 'Pascal [FPC]': 22, 'Pascal [GPC]': 2, 'Perl': 3, 'Perl 6': 54, 'PHP': 29, 'Pike': 19, 'Prolog [GNU]': 108, 'Prolog [SWI]': 15, 'Python (Pypy)': 99, 'Python 2.x [Pypy]': 4, 'Python': 116, 'R': 117, 'Racket': 95, 'Ruby': 17, 'Rust': 93, 'Scala': 39, 'Scheme': 18, 'Scheme [Chicken]': 97, 'Scheme [Guile]': 33, 'Sed': 46, 'Smalltalk': 23, 'SQLite - queries': 52, 'SQLite - schema': 40, 'Swift': 85, 'Tcl': 38, 'Text': 62, 'TypeScript': 57, 'VB.NET': 50, 'Whitespace': 6}


def mak_req(error, lang):
    resp = requests.get("https://api.stackexchange.com" +
                        "/2.3/search?order=desc&tagged={}&sort=activity&intitle={}&site=stackoverflow".format(lang, error))
    return resp.json()


def get_file():
    return sys.argv[-1]


def get_urls(json_dict):
    url_list = []
    title_list = []
    count = 0

    for i in json_dict['items']:
        if i['is_answered']:
            url_list.append(i["link"])
            title_list.append(i["title"])
            count += 1
        if count > 4:
            break

    for i in range(len(url_list)):
        if sys.argv[1] == '-w':
            webbrowser.open(url_list[i])
        else:
            print("{}. {} ({})\n".format(i+1, title_list[i], url_list[i]))


def get_yt_urls(json_dict):
    for i in range(len(json_dict['items'])):
        url = "https://www.youtube.com/watch?v=" + \
            json_dict['items'][i]['id']['videoId']
        if sys.argv[1] == '-w':
            webbrowser.open(url)
        else:
            print("{}. {} ({})\n".format(
                i+1, json_dict['items'][i]['snippet']['title'], url))
        if i > 4:
            break


def get_source_code():
    code = ""
    with open(get_file(), "r") as f:
        file = f.readlines()
    for line in file:
        code += line
    return code.strip()


if len(sys.argv) == 1:
    print("No File supplied")
else:
    ext = get_file().split(".")[-1]
    lang = ext_dict[ext]
    res, flag = api_call.runAPI(get_source_code(), lang_codes[lang])
    if flag == 1:
        if ext == 'cpp':
            error = ''
            z = res.strip().split("\n")[-3]
            errIndex = z.strip().split(":").index(" error")
            for i in z.strip().split(":")[errIndex:]:
                error += i.strip() + " "
        else:
            error = res.strip().split("\n")[-1]
        print("Error = {}".format(res.strip()))
        print("\nLoading...")
        yt = yt_api_call.ytApi(error + " " + lang)
        json = mak_req(error, lang)
        print("\nStackoverFlow queries:")
        get_urls(json)
        print("\nYouTube videos:")
        get_yt_urls(yt)
    else:
        print("No error found\nOutput:")
        print(res.strip())
