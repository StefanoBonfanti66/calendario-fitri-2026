import json
import re

def extract_potential_race_components(raw_text):
    potential_entries = []
    lines = raw_text.split('\n')
    
    # Mappatura mesi in italiano a numeri (per riferimento)
    month_map = {
        'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'mag': '05', 'giu': '06',
        'lug': '07', 'ago': '08', 'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'
    }

    # Ignoriamo le righe di navigazione e header noti
    ignore_lines_lc = set([
        "home", "il mio profilo", "i miei risultati", "esci", "calendario", "risultati", "circuiti", "rank", "archivi",
        "myfitri build: 145", "calendario eventi", "ricerca veloce", "nome o località e premere invio", "regione",
        "seleziona una regione", "tutte", "distanza", "seleziona una distanza", "anno", "seleziona l'anno",
        "filtro attivo: 100 eventi 2026", "coni", "cip", "itu", "etu", "stadio olimpico", "curva sud - 00135 roma",
        "partita iva 04515431007", "2026", "triathlon", "duathlon", "aquathlon", "winter triathlon", "cross country",
        "no-draft", "ips", "u23nextgen", "coppa italia", "trofeo giovanissimi"
    ])

    current_block_info = {
        "main_title": "",
        "main_date_raw": "",
        "main_location": "",
        "potential_sub_events": []
    }

    # Regex per vari tipi di linee che ci interessano
    main_title_line_pattern = re.compile(r'^(?:[0-9]+\°\s+)?([A-Z0-9\s&,-]+(?: TRIATHLON|DUATHLON|AQUATHLON|WINTER|CROSS|IRONMAN|CHALLENGE)[A-Z0-9\s&,-]*)$', re.IGNORECASE)
    date_loc_line_pattern = re.compile(r'^(dal )?(\d{2}-\d{2}-2026)( al \d{2}-\d{2}-2026)?([A-Za-zÀ-ÿ\s\'-]+)\s*\(([A-Za-zÀ-ÿ]+)\)\s*\|\s*([A-Za-zÀ-ÿ\s\'-]+)$', re.IGNORECASE)
    date_loc_concatenated_pattern = re.compile(r'^(dal )?(\d{2}-\d{2}-2026)( al \d{2}-\d{2}-2026)?([A-Za-zÀ-ÿ\s\'-]+)\s*\(([A-Za-zÀ-ÿ]+)\)\s*\|\s*([A-Za-zÀ-ÿ\s\'-]+)$', re.IGNORECASE)

    sub_event_line_pattern = re.compile(r'(\d{1,2})-(\S{3})\s+(.*?)\s*(Silver|Gold|Bronze|Giovanile|Paratriathlon|Internazionale|\d°)?$', re.IGNORECASE)

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if not stripped_line or stripped_line.lower() in ignore_lines_lc or len(stripped_line) < 3:
            continue
        
        # Tentativo di identificare un nuovo blocco di evento principale
        if main_title_line_pattern.match(stripped_line):
            # Se abbiamo un blocco precedente con informazioni valide, aggiungilo
            if current_block_info["main_title"] and current_block_info["main_date_raw"] and current_block_info["main_location"]:
                potential_entries.append(current_block_info)
            
            # Inizia un nuovo blocco
            current_block_info = {
                "main_title": stripped_line,
                "main_date_raw": "",
                "main_location": "",
                "potential_sub_events": []
            }
            continue

        # Cerca la data e la località in righe successive al titolo principale
        if current_block_info["main_title"] and not current_block_info["main_date_raw"]:
            date_loc_match = date_loc_line_pattern.match(stripped_line)
            if not date_loc_match: # Prova con il pattern concatenato
                date_loc_match = date_loc_concatenated_pattern.match(stripped_line)

            if date_loc_match:
                current_block_info["main_date_raw"] = date_loc_match.group(2) if not date_loc_match.group(1) else date_loc_match.group(0)
                current_block_info["main_location"] = date_loc_match.group(len(date_loc_match.groups())).strip()
                continue
        
        # Cerca i sotto-eventi
        if current_block_info["main_date_raw"] and current_block_info["main_location"]:
            sub_event_match = sub_event_line_pattern.match(stripped_line)
            if sub_event_match:
                current_block_info["potential_sub_events"].append({
                    "raw_line": stripped_line,
                    "day": sub_event_match.group(1),
                    "month_abbr": sub_event_match.group(2),
                    "title": sub_event_match.group(3).strip(),
                    "category_suffix": sub_event_match.group(4) or ""
                })
                continue
    
    # Aggiungi l'ultimo blocco se valido
    if current_block_info["main_title"] and current_block_info["main_date_raw"] and current_block_info["main_location"]:
        potential_entries.append(current_block_info)

    return potential_entries

if __name__ == "__main__":
    raw_text_from_user = """
Home
il mio profilo
i miei risultati
Esci
Calendario
Risultati
Circuiti
Rank
Archivi
myFITri build: 145
CALENDARIO EVENTI
RICERCA VELOCE
nome o località e premere Invio
REGIONE
Seleziona una regione
TUTTE
TUTTE
DISTANZA
Seleziona una distanza
TUTTE
TUTTE
ANNO
Seleziona l'anno
2026
2026
Tutte
Tutte
Triathlon
Triathlon
Duathlon
Duathlon
Aquathlon
Aquathlon
Winter triathlon
Winter triathlon
Cross country
Cross country
Triathlon
No-draft
Duathlon
Aquathlon
Winter triathlon
Cross country
IPS
U23NEXTGEN
Coppa Italia
Trofeo Giovanissimi
Filtro attivo: 100 eventi 2026
5° WINTER TRIATHLON & WINTER DUATHLON PREDAZZO
10-01-2026Predazzo (Trento) | Trentino-Alto Adige/Südtirol
11-gen	

WinterTriathlon Sprint		
11-gen	

WinterTriathlon		Giovanile
10-gen	


Winter Duathlon Classico		
10-gen	

Winter Duathlon Kids		Giovanile
GRAN PARADISO WINTER TRIATHLON
dal 24-01-2026 al 25-01-2026Cogne (Aosta) | Valle d'Aosta/Vallée d'Aoste
24-gen	

WinterTriathlon Super Sprint		Giovanile
24-gen	


WinterTriathlon Super Sprint		Giovanile
25-gen	


WinterTriathlon Classico		
1° COPPA S. AGATA DUATHLON SUPER SPRINT
01-02-2026Catania (Catania) | Sicilia
01-feb	

Duathlon Super Sprint		
C.I. WINTER TRIATHLON A SQUADRE
07-02-2026Alagna Valsesia (Vercelli) | Piemonte
08-feb	

WinterTriathlon Staffetta		
08-feb	

WinterTriathlon Atipico		Giovanile
08-feb	

WinterTriathlon Sprint		
07-feb	

Winter Duathlon Sprint		
07-feb	

Winter Duathlon Atipico		Giovanile
DUATHLON SPRINT DI BARZANO'
22-02-2026Barzanò (Lecco) | Lombardia
22-feb	

Duathlon Sprint		Silver
SABAUDIA DUATHLON DI CARNEVALE VII EDIZIONE
22-02-2026Sabaudia (Latina) | Lazio
22-feb	

Duathlon Sprint		Silver
22-feb	

Duathlon Kids		Giovanile
1° WINTER TRIATHLON MONTE BONDONE
22-02-2026Trento (Trento) | Trentino-Alto Adige/Südtirol
22-feb	

WinterTriathlon Sprint		Giovanile
22-feb	

WinterTriathlon		
2026 WORLD TRIATHLON WINTER DUATHLON CHAMPIONSHIPS PADOLA
dal 27-02-2026 al 28-02-2026Comelico Superiore (Belluno) | Veneto
27-feb	

Winter Duathlon Sprint		
27-feb	

Winter Duathlon		
28-feb	

Winter Duathlon Sprint		
2026 WORLD TRIATHLON WINTER CHAMPIONSHIPS PADOLA
dal 28-02-2026 al 01-03-2026Comelico Superiore (Belluno) | Veneto
28-feb	

WinterTriathlon Classico		
28-feb	

WinterTriathlon Sprint		
01-mar	

WinterTriathlon Sprint		
01-mar	

WinterTriathlon Staffetta		
DUATHLON NETIUM
01-03-2026Binetto (Bari) | Puglia
01-mar	

Duathlon Sprint		Silver Paratriathlon 
01-mar	

Duathlon Super Sprint		Giovanile
01-mar	

Duathlon Kids		Giovanile
4° DUATHLON GIOVANILE SESTO FIORENTINO - YOUTH
01-03-2026Sesto Fiorentino (Firenze) | Toscana
01-mar	

Duathlon Super Sprint		Giovanile
01-mar	

Duathlon Kids		Giovanile
DUATHLON SPRINT DI FORLÌ
01-03-2026Forlì (Forlì) | Emilia-Romagna
01-mar	

Duathlon Sprint		Silver
01-mar	

Duathlon Kids		Giovanile
01-mar	

Duathlon Miniduathlon		Giovanile
8 MUD DUATHLON MTB TELGATE
01-mar	

Duathlon Kids		Giovanile
01-mar	

Duathlon Youth		Giovanile
01-mar	

Duathlon Super Sprint		Paratriathlon 
DUATHLON SPRINT DI PUNTA SECCA
dal 07-03-2026 al 08-03-2026Santa Croce Camerina (Ragusa) | Sicilia
08-mar	

Duathlon Sprint		Silver
07-mar	

Duathlon Youth		Giovanile
07-mar	

Duathlon Kids		Giovanile
CAMPIONATO ITALIANO DUATHLON CROSS
08-03-2026Spresiano (Treviso) | Veneto
08-mar	


Duathlon		Silver
08-mar	


Duathlon Super Sprint MTB		Giovanile
IX DUATHLON SPRINT CITTÀ DI FOLIGNO - MEMORIAL DANILO PASCUCCI - DUATHLON YOUTH - DUATHLON KIDS
08-03-2026Foligno (Perugia) | Umbria
08-mar	

Duathlon Sprint		Silver
08-mar	

Duathlon Kids		Giovanile
DUATHLON SAN DAMIANO
15-03-2026San Giorgio Piacentino (Piacenza) | Emilia-Romagna
15-mar	

Duathlon Sprint		Silver
1° DUATHLON SPRINT DI OSTIA "EGIDIO E FRANCESCO"
15-03-2026Roma (Roma) | Lazio
15-mar	

Duathlon Sprint		Bronze
FREESTYLE CAMPIONATO REGIONALE DUATHLON DI CATEGORIA
15-03-2026Ponte Buggianese (Pistoia) | Toscana
15-mar	

Duathlon Sprint		Silver
CAMPIONATO ITALIANO DUATHLON SPRINT ASSOLUTO / AGE GROUP / PARADUATHLON / COPPA CRONO
dal 21-03-2026 al 22-03-2026Imola (Bologna) | Emilia-Romagna
21-mar	


Duathlon Sprint		Gold 
21-mar	


Duathlon Sprint		Silver
22-mar	


Duathlon Super Sprint		Silver
22-mar	


Duathlon Super Sprint		Silver Paratriathlon 
22-mar	


Duathlon Sprint		Silver
22-mar	

Duathlon Sprint		Bronze
DUATHLON DELL'ECOLOGIA
29-03-2026Viterbo (Viterbo) | Lazio
29-mar	

Duathlon Sprint		Silver
29-mar	

Duathlon Kids		Giovanile
29-mar	

Duathlon Miniduathlon		Giovanile
29-mar	

Duathlon Youth		Giovanile
29-mar	

Duathlon Super Sprint		Paratriathlon 
3° DUATHLON CLASSICO SILVER NO DRAFT DEL LITORALE PISANO
29-03-2026Pisa (Pisa) | Toscana
29-mar	

Duathlon Classico		Silver
ADRIATIC SERIES DUATHLON SPRINT TOLENTINO
29-03-2026Tolentino (Macerata) | Marche
29-mar	

Duathlon Sprint		Silver
DUATHLON SPRINT CITTÀ DI SANTENA
29-03-2026Santena (Torino) | Piemonte
29-mar	

Duathlon Sprint		Silver
1° DUATHLON DELLA LUNIGIANA
29-03-2026Aulla (Massa) | Toscana
29-mar	

Duathlon Sprint		Bronze
22° DUATHLON SPRINT CITTA' DELLO ZAFFERANO
29-03-2026San Gavino Monreale (Carbonia) | Sardegna
29-mar	

Duathlon Youth		Giovanile
29-mar	

Duathlon Kids		Giovanile
29-mar	

Duathlon Sprint		Silver
ASTICO DUATHLON 2026
29-mar	

Duathlon Sprint		Bronze
29-mar	

Duathlon Kids		Giovanile
CAMPIONATI ITALIANI DI DUATHLON CLASSICO NO DRAFT - ASSOLUTI - DI CATEGORIA - ELITE E AGE GROUP
12-04-2026Pontoglio (Brescia) | Lombardia
12-apr	


Duathlon Classico		Gold 
15 DUATHLON CITTÀ DI VIGEVANO
12-04-2026Vigevano (Pavia) | Lombardia
12-apr	

Duathlon Kids		Giovanile
12-apr	

Duathlon Youth		Giovanile
MANGIA'S TRIATHLON SICILY
12-04-2026Sciacca (Agrigento) | Sicilia
11-apr	

Duathlon Kids		Giovanile Paratriathlon 
11-apr	

Duathlon Youth		Giovanile Paratriathlon 
12-apr	

Triathlon Sprint		Silver
4° DUATHLON DEL PIAVE
12-04-2026San Donà di Piave (Venezia) | Veneto
12-apr	

Duathlon Sprint MTB		Bronze
OVERCOME EVENTS: 3° DUATHLON KIDS E GIOVANI CASTELBOLOGNESE
12-04-2026Castel Bolognese (Ravenna) | Emilia-Romagna
12-apr	

Duathlon Kids		Giovanile
OVERCOME EVENTS: 3° DUATHLON KIDS + GIOVANI CASTELBOILOGNESE
12-04-2026Castel Bolognese (Ravenna) | Emilia-Romagna
12-apr	

Duathlon Miniduathlon		Giovanile
SANTA MARINELLA TRIATHLON SPRINT
12-04-2026Santa Marinella (Roma) | Lazio
12-apr	

Triathlon Sprint		Silver
C.I. GIOVANI INDIVIDUALE E MIXED RELAY 2+2
18-04-2026Magione (Perugia) | Umbria
18-apr	


Duathlon Super Sprint		Giovanile
18-apr	


Duathlon Super Sprint		Giovanile
18-apr	


Duathlon Youth		Giovanile
19-apr	


Duathlon Staffette		Giovanile
ADRIATIC SERIES TRIATHLON CESENATICO ITALIA
dal 18-04-2026 al 19-04-2026Cesenatico (Forlì) | Emilia-Romagna
19-apr	

Triathlon Sprint		Silver
19-apr	

Triathlon Olimpico		Silver
18-apr	

Triathlon Atipico		
ELBA WEEKEND TRI
dal 18-04-2026 al 19-04-2026Marciana (Livorno) | Toscana
19-apr	

Triathlon Sprint		Silver
18-apr	

Triathlon Olimpico		Silver
MILANOTRI - FOLLOWYOURPASSION
18-04-2026Segrate (Milano) | Lombardia
18-apr	

Triathlon Olimpico		Gold 
18-apr	

Triathlon Sprint		Gold 
32° TRIATHLON DI ANDORA
19-04-2026Andora (Savona) | Liguria
19-apr	

Triathlon Sprint		Silver
19-apr	

Triathlon Olimpico		Silver
DE SORTIS ARGONAUTI TRI
19-apr	

Triathlon Olimpico		Gold 
19-apr	

Triathlon Sprint		Silver
9° LIGNANO “EYOF EUROPEAN TEST EVENT” TRIATHLON MEMORIAL ARDITO
25-04-2026Lignano Sabbiadoro (Udine) | Friuli-Venezia Giulia
25-apr	

Triathlon Sprint		Silver
25-apr	

Triathlon Sprint		Silver
ADRIATIC SERIES TRIATHLON CUPRA MARITTIMA
25-04-2026Cupra Marittima (Ascoli Piceno) | Marche
26-apr	

Triathlon Olimpico		Gold 
25-apr	

Triathlon Sprint		Silver
25-apr	

Triathlon Atipico		
IRON ISLAND HALF TRIATHLON - TRIATHLON OLIMPICO NO DRAFT
26-apr	

Triathlon Olimpico		Silver
26-apr	

Triathlon Medio		Silver
26-apr	

Triathlon Medio		
26-apr	

Triathlon Olimpico		Silver
TRIATHLON SPRINT DEI PRINCIPI
26-apr	

Triathlon Sprint		Silver
SABAUDIA TRIATHLON OLIMPICO XIII EDIZIONE "MEMORIAL RICCARDO GIORGI E SIMONE BESCO"
26-apr	

Triathlon Olimpico		Silver
CHIATRI - FOLLOWYOURPASSION
01-05-2026Domus de Maria (Carbonia) | Sardegna
01-mag	

Triathlon Sprint		Silver
01-mag	

Triathlon Olimpico		Silver
01-mag	

Triathlon Medio		Silver
CAMPIONATI ITALIANI TRIATHLON CROSS - CAPOLIVERI
01-05-2026Capoliveri (Livorno) | Toscana
01-mag	


Triathlon Cross Triathlon		
13°IRON TOUR CROSS - TRIATHLON OFF-ROAD A TAPPE-ISOLA D'ELBA
dal 02-05-2026 al 03-05-2026Capoliveri (Livorno) | Toscana
02-mag	

Triathlon Sprint MTB		Silver
03-mag	

Triathlon Sprint MTB		Silver
GALLIPOLI OLYMPIC TRIWAVE CAROLI EDITION
03-05-2026Gallipoli (Lecce) | Puglia
03-mag	

Triathlon Olimpico		Silver
TRIATHLON SPRINT ALTOTEVERE
03-05-2026San Giustino (Perugia) | Umbria
03-mag	

Triathlon Sprint		Silver
VENICE JESOLO IRONMAN 70.3
03-05-2026Jesolo (Venezia) | Veneto
03-mag	

Triathlon Medio		Internazionale 
EUROPE TRIATHLON JUNIOR CUP
dal 08-05-2026 al 09-05-2026Caorle (Venezia) | Veneto
08-mag	

Triathlon Super Sprint		
09-mag	

Triathlon Staffetta		
37.TRIATHLON DI CALDARO - OLIMPICO
09-05-2026Caldaro sulla strada del vino/Kaltern an der Weinstraße (Bolzano) | Trentino-Alto Adige/Südtirol
09-mag	

Triathlon Olimpico		Silver
EUROPEAN TRIATHLON CUP CAORLE
09-05-2026Caorle (Venezia) | Veneto
09-mag	

Triathlon Sprint		
CHALLENGE CESENATICO 2026
10-05-2026Cesenatico (Forlì) | Emilia-Romagna
09-mag	

Duathlon Kids		Giovanile Paratriathlon 
09-mag	

Duathlon Miniduathlon		Giovanile Paratriathlon 
10-mag	

Triathlon Medio		Internazionale 
09-mag	

Triathlon Sprint		Silver
10-mag	

Aquabike Lungo		
AQUATHLON DELLE ALPI
10-05-2026Bolzano/Bozen (Bolzano) | Trentino-Alto Adige/Südtirol
10-mag	

Aquathlon Sprint		Giovanile
10-mag	

Aquathlon Super Sprint		Giovanile
10-mag	

Aquathlon Kids		Giovanile
MONDELLO CUP 10
10-05-2026Palermo (Palermo) | Sicilia
09-mag	

Aquathlon Kids		Giovanile
09-mag	

Aquathlon Super Sprint		Giovanile
10-mag	

Triathlon Sprint		Silver
GARGANO TRIATHLON SPRINT
10-05-2026Manfredonia (Foggia) | Puglia
10-mag	

Triathlon Sprint		Bronze
TRIATHLON MEDIO E OLIMPICO NO-DRAFT CITTÀ DI CANDIA
10-05-2026Candia Canavese (Torino) | Piemonte
10-mag	

Triathlon Medio		Silver
10-mag	

Triathlon Olimpico		Silver
7° TRIATHLON CITTÀ DI VAREDO
10-05-2026Varedo (Monza) | Lombardia
10-mag	

Triathlon Super Sprint		Giovanile
10-mag	

Triathlon Youth		Giovanile
10-mag	

Triathlon Kids		Giovanile
10-mag	

Triathlon Minitriathlon		Giovanile
LATINA TRIATHLON SPRINT VII EDIZIONE "MEMORIAL FEDERICO SALVAGNI"
10-05-2026Latina (Latina) | Lazio
10-mag	

Triathlon Sprint		Silver
VENICE CAORLE TRI 2026
10-mag	

Triathlon Olimpico		Silver
10-mag	

Triathlon Sprint		Silver
IRON TOUR ROAD
dal 13-05-2026 al 17-05-2026Capoliveri (Livorno) | Toscana
13-mag	

Triathlon Sprint		Silver
14-mag	

Triathlon Sprint		Silver
15-mag	

Triathlon Sprint		Silver
16-mag	

Triathlon Sprint		Silver
17-mag	

Triathlon Sprint		Silver
CAMPIONATO ITALIANO UNIVERSITARIO CAMPIONATO ITALIANO PARATRIATHLON
dal 16-05-2026 al 17-05-2026Loano (Savona) | Liguria
17-mag	

Triathlon		Paratriathlon 
17-mag	


Triathlon Sprint		
16-mag	

Triathlon Youth		
16-mag	

Triathlon Kids		
17-mag	

Triathlon Sprint		Silver
TRIATHLON CITTA’ DI CAGLIARI - CAMPIONATO ITALIANO INTERFORZE TRIATHLON SPRINT
dal 16-05-2026 al 17-05-2026Cagliari (Cagliari) | Sardegna
17-mag	

Triathlon Sprint		Silver
16-mag	

Triathlon Youth		
16-mag	

Triathlon Kids		Giovanile
ADRIATIC SERIES TRIATHLON SPRINT SILVER GROTTAMMARE (AP)
17-05-2026Grottammare (Ascoli Piceno) | Marche
17-mag	

Triathlon Sprint		Silver
VIII TRIATHLON LE BANDIE DEGLI EROI
17-05-2026Spresiano (Treviso) | Veneto
17-mag	

Triathlon Super Sprint		Giovanile
17-mag	

Triathlon Kids		Giovanile
17-mag	

Triathlon Minitriathlon		Giovanile
17-mag	

Triathlon Sprint		Silver
FITCENTER TRIATHLON SPRINT BISCEGLIE 2026
17-05-2026Bisceglie (Barletta) | Puglia
17-mag	

Triathlon Sprint		Silver
6° TRIATHLON CITTA' DI GORIZIA
24-05-2026Gorizia (Gorizia) | Friuli-Venezia Giulia
24-mag	

Triathlon Kids		Giovanile
24-mag	

Triathlon Minitriathlon		Giovanile
24-mag	

Triathlon Youth		Giovanile
24-mag	

Triathlon Sprint		Silver
9° TRIATHLON SPRINT CITTA' DI SALO'
24-05-2026Salò (Brescia) | Lombardia
24-mag	

Triathlon Sprint		Gold 
13 TRIATHLON SPRINT PIASCO E GIOVANILI
24-05-2026Piasco (Cuneo) | Piemonte
24-mag	

Triathlon Sprint		Silver
LYKOS FOR OTHERS
30-05-2026Pisogne (Brescia) | Lombardia
31-mag	

Aquathlon Atipico		Paratriathlon 
30-mag	

Triathlon Super Sprint		Paratriathlon 
2°TRIATHLON SPRINT PUSIANO LAKE
31-05-2026Pusiano (Como) | Lombardia
31-mag	

Triathlon Sprint		Silver
TRANI TRIATHLON OLIMPICO 8^ EDIZIONE - CAMPIONATO ITALIANO INTERFORZE
31-05-2026Trani (Barletta) | Puglia
31-mag	

Triathlon Olimpico		Silver
6° AQUATHLON DELLA VITTORINO - MEMORIAL AARON BERTONCINI
02-06-2026Piacenza (Piacenza) | Emilia-Romagna
02-giu	

Aquathlon		Giovanile
02-giu	

Aquathlon Kids		Giovanile
DIAMOND TRI & GRANDATRIATHLON 20°TRIATHLON SPRINT DEL ROERO
02-06-2026Sommariva Perno (Cuneo) | Piemonte
02-giu	

Triathlon Sprint		BronzeGiovanile
IRONLAKE MUGELLO - CAMPIONATO ITALIANO TRIATHLON MEDIO
02-06-2026Barberino di Mugello (Firenze) | Toscana
02-giu	


Triathlon Medio		Gold 
CAMPIONATO ITALIANO AQUATHLON COPPA ITALIA E TROFEO SVILUPPO TRIATHLON
dal 06-06-2026 al 07-06-2026Porto Sant'Elpidio (Fermo) | Marche
06-giu	


Aquathlon Sprint		Giovanile
06-giu	


Aquathlon Super Sprint		Giovanile
06-giu	


Aquathlon Sprint		Giovanile
06-giu	

Aquathlon MiniAquathlon		Giovanile
06-giu	

Aquathlon Super Sprint		Giovanile
07-giu	

Triathlon Super Sprint		Giovanile
07-giu	

Triathlon Minitriathlon		Giovanile
23° TRIATHLON OLIMPICO CITTÀ DI PIETRA LIGURE
06-06-2026Pietra Ligure (Savona) | Liguria
06-giu	

Triathlon Olimpico		Silver
ADRIATIC SERIES TRIATHLON OLIMPICO CITTÀ DI VIESTE
07-06-2026Vieste (Foggia) | Puglia
07-giu	

Triathlon Olimpico		Gold 
IRONMAN 70.3 ALGHERO
07-06-2026Alghero (Sassari) | Sardegna
07-giu	

Triathlon Medio		Internazionale 
2° TRIATHLON CRONO TAVERNOLA
13-06-2026Tavernola Bergamasca (Bergamo) | Lombardia
13-giu	

Triathlon Sprint		Silver
13-giu	

Triathlon Sprint		Silver
MANDELLO: TRIATHLON CROSS + AQUATHLON
13-06-2026Mandello del Lario (Lecco) | Lombardia
14-giu	

Aquathlon		Giovanile
14-giu	

Aquathlon Sprint		Bronze
13-giu	

Triathlon Sprint MTB		Bronze
AQUATHLON DEL CASTELLO
dal 14-06-2026 al 21-06-2026Santa Marinella (Roma) | Lazio
14-giu	

Aquathlon Classico		
14-giu	

Aquathlon Super Sprint		Giovanile
14-giu	

Aquathlon MiniAquathlon		Giovanile
21-giu	

Aquathlon Kids		Giovanile
BIM TRIATHLON
14-06-2026Bellaria-Igea Marina (Rimini) | Emilia-Romagna
14-giu	

Triathlon Olimpico		Gold  Paratriathlon 
TRIATHLON SPRINT NETIUM
14-06-2026Giovinazzo (Bari) | Puglia
14-giu	

Triathlon Super Sprint		Giovanile
14-giu	

Triathlon Kids		Giovanile
14-giu	

Triathlon Sprint		Silver
TIVAN TRI TRIATHLON SPRINT
14-06-2026Gravedona ed Uniti (Como) | Lombardia
14-giu	

Triathlon Sprint		Silver
TRIATHLON OLIMPICO LAGO DI VICO
20-06-2026Ronciglione (Viterbo) | Lazio
20-giu	

Triathlon Olimpico		Silver
TRIATHLON SPRINT DI MAZARA DEL VALLO 1.0
dal 20-06-2026 al 21-06-2026Mazara del Vallo (Trapani) | Sicilia
21-giu	

Triathlon Sprint		Silver Paratriathlon 
20-giu	

Triathlon Kids		Giovanile Paratriathlon 
20-giu	

Triathlon Youth		Giovanile Paratriathlon 
XTERRA EUROPEAN CHAMPIONSHIP
20-06-2026Molveno (Trento) | Trentino-Alto Adige/Südtirol
20-giu	

Triathlon Atipico		Internazionale  Paratriathlon 
17° TERRIBILE TRIATHLON IDROMAN
21-06-2026Idro (Brescia) | Lombardia
21-giu	

Triathlon Sprint		Silver
21-giu	

Triathlon Olimpico		Silver
21-giu	

Triathlon Medio		Silver
REVINE LAGO TRI
21-06-2026Revine Lago (Treviso) | Veneto
21-giu	

Triathlon Sprint		Bronze
21-giu	

Triathlon Kids		Giovanile
21-giu	

Triathlon Minitriathlon		Giovanile
DUATHLON SPRINT - SPORT IN FESTA 2026
21-giu	

Duathlon Sprint		Silver
TRIATHLON MARCONI
21-06-2026Sasso Marconi (Bologna) | Emilia-Romagna
21-giu	

Triathlon Olimpico		Silver
MILANO DEEJAY TRI
21-06-2026Segrate (Milano) | Lombardia
20-giu	

Triathlon Olimpico		Gold 
21-giu	

Triathlon Sprint		Gold 
21-giu	

Triathlon Kids		Giovanile
21-giu	

Triathlon Youth		Giovanile
II° NEAPOLIS AQUATHLON
dal 27-06-2026 al 28-06-2026Napoli (Napoli) | Campania
27-giu	

Aquathlon Kids		
28-giu	


Aquathlon Classico		
27-giu	

Aquathlon Super Sprint		
LOVERETRI - FOLLOWYOURPASSION
28-06-2026Lovere (Bergamo) | Lombardia
28-giu	

Triathlon Medio		Gold 
6° TRIATHLON SPRINT LAGO DI MIGNANO - MEMORIAL ALESSANDRO REPETTI
28-06-2026Vernasca (Piacenza) | Emilia-Romagna
28-giu	

Triathlon		Silver
C.I. GIOVANI TRIATHLON IND/C.I. GIOVANI 2+2/COPPA REGIONI JR/YOUTH/ COPPA REGIONI RAGAZZI
dal 03-07-2026 al 05-07-2026Spresiano (Treviso) | Veneto
03-lug	


Triathlon		Giovanile
03-lug	


Triathlon Super Sprint		Giovanile
03-lug	


Triathlon		Giovanile
04-lug	


Triathlon Staffetta		Giovanile
04-lug	


Triathlon Staffetta		Giovanile

Stadio Olimpico

Curva Sud - 00135 Roma

Partita Iva 04515431007
coni
cip
itu
etu
"""
    races = parse_final_raw_text_to_races(raw_text_from_user)
    with open('app/src/races_full.json', 'w', encoding='utf-8') as f:
        json.dump(races, f, ensure_ascii=False, indent=2)
    print(f"Salvate {len(races)} gare nel database ufficiale (dal testo fornito).")
