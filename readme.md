# NoteMania iiXD

Gra zręcznościowo-rytmiczna skupiona wokół testowania ludzkiego czasu reakcji oraz dobrej zabawy. Inspirowana japońską serią gier beatmania IIDX.
# Krótko co i jak
Gra wymaga zainstalowania python3 oraz pygame. Grę można otworzyć otwierając katalog w wierszu poleceń i wpisując ``python .\main.py``, gra polega na wciskaniu odpowiednich klawiszy w rytm muzyki oraz lecących z góry note'ów. Kolejność przycisków lewo-prawo to ``A S D SPACJA J K L``. Muzykę wybieramy przyciskiem ``Enter``.  Gra do wyświetlania note'ów wykorzystuje specjalny format BMS.

# Dokumentacja/Bibliografia/Creditsy
Data dostępu 01.01.2026-27.01.2026
 - https://docs.python.org/3/ - Język gry
 - https://www.pygame.org/docs/ - Silnik gry
 - https://en.wikipedia.org/wiki/Be-Music_Source - autor: Urao Yane, format BMS
 - https://hitkey.nekokan.dyndns.info/cmds.htm - autor: hitkey, kompendium wiedzy o BMS
 - https://bm98.yaneu.com/bm98/bmsformat.html - autor: Urao Yane, syntax plików BMS
 - społeczność gry Beatmania IIDX oraz BMS
 - Deepseek-V3.2 (Wykorzystywane w celach pomocy)
# Wykorzystana muzyka (również autorzy plików BMS)
 - xi - Freedom Dive - https://bmssearch.net/bmses/RC2HpISObTN12o
 - SHIKI - Angelic Layer - https://bmssearch.net/bmses/5Twa4CMzFF3GgZ
 - -45 - Total Eclipse of the Sun - https://bmssearch.net/bmses/5Lp9xFtUN-ew4J
 - Est - Angelic Snow - https://bmssearch.net/bmses/k_H73mzAdlG7YT
# Najcięższa część developmentu
Parsowanie plików BMS okazało się najtrudniejszym zadaniem całego projekty. Format BMS to bardzo duża specyfikacja z dziesiątkami typów komend, manipulowaniem tempem w trakcie utwory, podziału na segmenty i innych różnych, dziwnych zagwostek które ze sobą niesie. Moja implementacja do której potrzebowałem pomocy AI oraz powyższej dokumentacji jest uproszczeniem, obsługuje jedynie pojedyncze, podstawowe noty z jednym stałym tempem. Po długiej walce w końcu zadziałało tak jak chciałem i note'y spadały tak jak powinny. Mimo wszystko, jestem zadowolony z wyniku jaki osiągnąłem, zainicjowanie właśnie formatu BMS przyszło z tego, że jestem wielkim fanem Beatmanii IIDX oraz jego rozgałęzień typu LR2oraja/beatoraja i jestem nałogowym graczem gier rytmicznych od dzieciństwa.
