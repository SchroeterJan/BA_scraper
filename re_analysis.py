import datetime
import re
import unicodedata


def re_search(pattern, text, group_=1):
    # patterns is inserted as raw string into the function
    pattern = unicodedata.normalize("NFC", pattern)
    pattern = re.compile(pattern)
    m = re.search(pattern, text)
    if m:
        found = m.group(group_)
    else:
        # print(search + ' --- was not found')
        found = None
    return found


def get_anrede(text):
    found = re_search(pattern=r'Herr', text=text, group_=0)
    if found:
        anrede = found
    else:
        found = re_search(pattern=r'Frau', text=text, group_=0)
        if found:
            anrede = found
        else:
            print('KEINE ANREDE GEFUNDEN')
            anrede = ''
    return anrede


def get_ad(text):
    found = re_search(pattern=r'a\. D\.', text=text, group_=0)
    if found:
        return found
    else:
        found = re_search(pattern=r'a\.D\.', text=text, group_=0)
        if found:
            return found
        else:
            print('No außer Dienst found')
            return ''


def get_funktion(text, anrede, ad):
    found = re_search(pattern=anrede + r' (.+?) ' + ad, text=text)
    if found:
        return found
    else:
        print('No Funktion found')


def get_name(text, ad):
    found = re_search(pattern=ad + r' (.+?) hat', text=text)
    if found:
        return found
    else:
        print('No Name found')


def get_taetigkeit(text, multi_no):
    # Über den Plural von "Tätigkeit" wird die Aufnahme mehrerer Tätigkeiten detektiert
    if re_search(pattern=r'nachamtliche Tätigkeiten aufnehmen', text=text, group_=0):      # Falls Plural
        if multi_no == str(1):       # Bei der Ersten der mehreren Tätigkeiten wird die Gesamtanzahl ermittelt
            # Beschreibung der Tätigkeiten separieren
            taet_str = re_search(pattern=r'aufnehmen zu wollen:   (.+?)     Die Bundesregierung', text=text)
            # detektiere nur Zahlen und wandle die höchste zu Typ int
            multi = max(map(int, re.findall(re.compile(r'([0-9])\.'), taet_str)))
            # multi = max(map(int, [e for e in re.split("[^0-9]", taet_str) if e != '' and len(e) == 1]))
            # ermittle erste Tätigkeit
            found = re_search(pattern=multi_no + r'\.  (.+?)  ' + str(int(multi_no) + 1), text=text)
            return found, multi
        else:
            found = re_search(pattern=multi_no + r'\.  (.+?)  ', text=text)
            return found, multi_no
    else:
        multi = 1
        found = re_search(pattern=r'nachamtliche Tätigkeit (.+?) aufnehmen', text=text)
        if found:
            return found, multi
        else:
            found = re_search(pattern=r'nachamtliche Tätigkeit (.+?) angezeigt', text=text)
            if found:
                return found, multi
            else:
                found = re_search(pattern=r'die Tätigkeit als (.+?) aufnehmen zu wollen', text=text)
                if found:
                    return found, multi
                else:
                    found = re_search(pattern=r'angezeigt, (.+?).   Die Bundesregierung', text=text)
                    if found:
                        return found, multi
                    else:
                        found = re_search(pattern=r'angezeigt, (.+?). Die Bundesregierung', text=text)
                        if found:
                            return found, multi
                        else:
                            print('NO TÄTIGKEIT FOUND')
                            return None, multi


def get_date_sitzung(text):
    found = re_search(pattern=r'in ihrer Sitzung am (.+?) der Empfehlung', text=text)
    if found:
        empfehlung = True
        try:
            found = datetime.datetime.strptime(found, '%d. %B %Y')
        except:
            found = datetime.datetime.strptime(found, '%d. %B %Y ')
    else:
        found = re_search(pattern=r'in ihrer Sitzung am (.+?) beschlossen', text=text)
        if found:
            empfehlung = False
        else:
            found = re_search(r'Die Bundesregierung hat am (.+?) der Empfehlung', text=text)
            if found:
                empfehlung = True
            else:
                print('No date of Sitzung found')
    return found, empfehlung


def get_date_bekannt(text, anrede):
    found = re_search(pattern=r'Bundesministergesetzes Vom (.+?)  ' + anrede, text=text)
    if found:
        try:
            found = datetime.datetime.strptime(found, '%d. %B %Y')
        except:
            found = datetime.datetime.strptime(found, '%d. %B %Y ')
    else:
        print('No date of Bekanntmachung found')
    return found


def get_folgend(text, empfehlung):
    if empfehlung:
        found = re_search(pattern=r'Gremiums (.+?) beschlossen', text=text)
        if found == 'folgend':
            return True
        else:
            found = re_search(pattern=r'Gremiums (.+?) angeschlossen', text=text)
            if found:
                return True
            else:
                return False
    else:
        found = re_search(pattern=r'Gremiums (.+?)\.', text=text)
        if found == 'angeschlossen':
            return True
        else:
            found = re_search(pattern=r'schließt sich damit den Empfehlungen des beratenden Gremiums (.+?)\.',
                              text=text)
            if found == 'an':
                return True
            else:
                return False


def get_beschluss(text, multi, empfehlung):
    if multi == 1:
        found = re_search(pattern=r'beschlossen, (.+?) dieser Tätigkeit', text=text)
        if found:
            return found
        else:
            found = re_search(pattern=r'beschlossen, (.+?).  Berlin', text=text)
            if found:
                return found
            else:
                print('No Beschluss gefunden')
    else:
        found = re_search(pattern=r'beschlossen, (.+?)  Berlin', text=text)
        if found:
            return found
        else:
            print('No Beschluss gefunden')
