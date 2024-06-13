import radio_user, importlib


class Radio:
    rock        =   "https://hls-01-radiorecord.hostingradio.ru/record-rock/112/playlist.m3u8"
    disco       =   "https://hls-01-radiorecord.hostingradio.ru/record-sd90/playlist.m3u8"
    record_80   =   "https://hls-01-radiorecord.hostingradio.ru/record-1980/112/playlist.m3u8" 
    dance_70    =   "https://hls-01-radiorecord.hostingradio.ru/record-1970/playlist.m3u8"
    dance_60    =   "https://hls-01-radiorecord.hostingradio.ru/record-cadillac/playlist.m3u8"
    eurodance   =   "https://hls-01-radiorecord.hostingradio.ru/record-eurodance/playlist.m3u8"
    christmas   =   "https://hls-01-radiorecord.hostingradio.ru/record-christmas/playlist.m3u8"
    record      =   "https://hls-01-radiorecord.hostingradio.ru/record/playlist.m3u8"
    russian_mix =   "https://hls-01-radiorecord.hostingradio.ru/record-rus/playlist.m3u8"
    nashasliki  =   "https://hls-01-radiorecord.hostingradio.ru/record-nashashlyki/playlist.m3u8"
    chill_out   =   "https://hls-01-radiorecord.hostingradio.ru/record-chil/playlist.m3u8"
    deep        =   "https://hls-01-radiorecord.hostingradio.ru/record-deep/playlist.m3u8"
    remix       =   "https://hls-01-radiorecord.hostingradio.ru/record-rmx/playlist.m3u8"
    summer      =   "https://hls-01-radiorecord.hostingradio.ru/record-summerparty/playlist.m3u8"
    fuko        =   "https://hls-01-radiorecord.hostingradio.ru/record-mf/playlist.m3u8"
    techno      =   "https://hls-01-radiorecord.hostingradio.ru/record-technopop/playlist.m3u8"
    simphony    =   "https://hls-01-radiorecord.hostingradio.ru/record-symph/playlist.m3u8"
    naftalin    =   "https://hls-01-radiorecord.hostingradio.ru/record-naft/playlist.m3u8"
    hardstyle   =   "https://hls-01-radiorecord.hostingradio.ru/record-teo/playlist.m3u8"
    medljak     =   "http://radio.loveprod.ru:8000/live"
    
    
    radio_urls = {
            "1": rock,
            "2": disco,
            "3": record_80,
            "4": dance_70,
            "5": dance_60,
            "6": eurodance,
            "7": christmas,
            "8": record,
            "9": russian_mix,
            "10": nashasliki,
            "11": chill_out,
            "12": deep,
            "13": remix,
            "14": summer,
            "15": fuko,
            "16": techno,
            "17": simphony,
            "18": naftalin,
            "19": hardstyle,
            "20": medljak,
            }
 
    radio_names = {
            "1": "Rock",
            "2": "Супердискотека 90х",
            "3": "Record 80‑х",
            "4": "70's Dance",
            "5": "60's Dance",
            "6": "Eurodance",
            "7": "Christmas",
            "8": "Record",
            "9": "Russian mix",
            "10": "На шашлыки!",
            "11": "Chill-Out",
            "12": "Deep",
            "13": "Remix",
            "14": "Summer Dance",
            "15": "Маятник Фуко",
            "16": "Technoshop",
            "17": "Симфония FM",
            "18": "Нафталин FM",
            "19": "Hardstyle",
            "20": "Медляк FM",
            }

#refresh variable after user update
importlib.reload(radio_user)
# Find the last key and increment it
last_key = max(map(int, Radio.radio_names.keys()))
new_key = str(last_key + 1)
# Add new name and value to the dictionary
Radio.radio_names[new_key] = radio_user.custom_radio_name
# Find the last key and increment it
last_keys = max(map(int, Radio.radio_urls.keys()))
new_keys = str(last_keys + 1)
Radio.radio_urls[new_keys] = radio_user.custom_radio_url