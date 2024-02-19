import datetime
import re
import unicodedata


def re_search(text, search):
    m = re.search(search, text)
    if m:
        found = m.group(1)
    else:
        # print(search + ' --- was not found')
        found = None
    return found


def get_anrede(text):
    m = re.search('Herr', text)
    if m:
        anrede = 'Herr'
    else:
        m = re.search('Frau', text)
        if m:
            anrede = 'Frau'
        else:
            'KEINE ANREDE GEFUNDEN'
            anrede = ''
    return anrede


def get_ad(text):
    found = re.search(r'a\. D\.', text)
    if found:
        return 'a. D.'
    else:
        found = re.search(r'a\.D\.', text)
        return 'a.D.'



def get_funktion(text, anrede, ad):
    return re_search(search=anrede + ' (.+?) ' + ad, text=text)



def get_name(text, ad):
    return re_search(search=ad +' (.+?) hat', text=text)


def get_taetigkeit(text, multi_no):
    # Über den Plural von "Tätigkeit" wird die Aufnahme mehrerer Tätigkeiten detektiert
    if re.search(unicodedata.normalize("NFC", 'nachamtliche Tätigkeiten aufnehmen'), text):      # Falls Plural
        if multi_no == str(1):       # Bei der Ersten der mehreren Tätigkeiten wird die Gesamtanzahl ermittelt
            # Beschreibung der Tätigkeiten separieren
            taet_str = re_search(search='aufnehmen zu wollen:   (.+?)     Die Bundesregierung', text=text)
            # detektiere nur Zahlen und wandle die höchste zu Typ int
            multi = max(map(int, [e for e in re.split("[^0-9]", taet_str) if e != '' and len(e) == 1]))
            # ermittle erste Tätigkeit
            found = re_search(search=multi_no + r'\.  (.+?)  ' + str(int(multi_no) + 1), text=text)
            return found, multi
        else:
            found = re_search(search=multi_no + r'\.  (.+?)  ', text=text)
            return found, multi_no
    else:
        multi = 1
        found = re_search(search=unicodedata.normalize("NFC", 'nachamtliche Tätigkeit (.+?) aufnehmen'),
                          text=text)
        if found:
            return found, multi
        else:
            found = re_search(
                search=unicodedata.normalize("NFC", 'nachamtliche Tätigkeit (.+?) angezeigt'),
                text=text)
            if found:
                return found, multi
            else:
                found = re_search(
                    search=unicodedata.normalize("NFC", 'die Tätigkeit als (.+?) aufnehmen zu wollen'),
                    text=text)
                if found:
                    return found, multi
                else:
                    found = re_search(search='angezeigt, (.+?).   Die Bundesregierung', text=text)
                    if found:
                        return found, multi
                    else:
                        print('NO TÄTIGKEIT FOUND')
                        return None, multi



def get_date_sitzung(text):
    found = re_search(search='in ihrer Sitzung am (.+?) der Empfehlung', text=text)
    if found:
        try:
            found = datetime.datetime.strptime(found, '%d. %B %Y')
        except:
            found = datetime.datetime.strptime(found, '%d. %B %Y ')
    return found


def get_date_bekannt(text, anrede):
    found = re_search(search='Bundesministergesetzes Vom (.+?)  ' + anrede, text=text)
    if found:
        try:
            found = datetime.datetime.strptime(found, '%d. %B %Y')
        except:
            found = datetime.datetime.strptime(found, '%d. %B %Y ')
    return found


def get_folgend(text):
    found = re_search(search='Gremiums (.+?) beschlossen', text=text)
    if found:
        return True
    else:
        return False


def get_beschluss(text, multi):
    if multi == 1:
        found = re_search(search=unicodedata.normalize("NFC", 'beschlossen, (.+?) dieser Tätigkeit'),
                          text=text)
        if found:
            return found
        else:
            found = re_search(search='beschlossen, (.+?).  Berlin', text=text)
            return found
    else:
        return re_search(search='beschlossen, (.+?)  Berlin', text=text)
