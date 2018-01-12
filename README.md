# PKM2
Rozproszony system wizyjny,pozwalający obserwować widok z kabiny z lokomotywy. Zaimplementowane zostały różne algorytmy rozpoznowania obrazu oraz sieć nieuronowa. Dodany został również moduł wskazujący, które z torów są zajęte.

Wersja kliencka pozwaląjąca kontrolować cały system została zaimplementowana na urządzenia klasy PC oraz z zainstalowanym Androidem.

# Instalacja

## Konfiguracja Python
* Ściągnij aktualną wersję projektu z [GitHub](https://github.com/Medioxx/PKM2.2)
* Zainstaluj Anaconde [Anaconda](https://docs.anaconda.com/anaconda/install/windows). W tym projekcie używany jest Python 3.6
* Skonfiguruj ścieżkę systemową,aby ta wersja Pythona oraz Pip była używana w przypadku odpalania projektu z konsoli
* Przejdź do folderu, w którym znajduje się repozytorium 
* Włącz konsolę, a następnie ``pip install -r requirements.txt``
* W przypadku uruchamiana projektu w sali PKM możliwe jest udostępnianie projektu na sieć WETI, aby to zrobić należy najpierw połączyć się z siecią WETI, a następni połączyć z sięcią utworzoną przez kamerę. Na końcu jako administrotor należy wpisać komendę ``route ADD 192.168.2.0 MASK 255.255.255.0 @brama_kamery``

## Konfiguracja Android
* Ściągnij aktualną wersję projektu z [GitHub](https://github.com/Medioxx/PKM2.2)
* Ściągnij oraz zainstaluj Android Studio =>3 [Android Studio](https://developer.android.com/studio/index.html)


# Dostępne moduły

## Rest api

Plik startowy rest api ``rest_api_pkm2/rest_api_pkm2.py`` należy włączyć po zainstalowaniu wszystkich zależności.
To właśnie on jest odpowiedzialny za całą część serwerową. Obsługuje on wszystkie zapytania oraz zwraca odpowiedzi wedle ustalonej zasady. Backend ten oprócz tego,że wystawia rest api hostuje stronę internetową znajdującą się pod adresem ``http:ip_urządzenia:5000``. Na tej stronie możemy jako zwykły użytkownik obejrzeć wybrany film,zobaczyć,który z algorytmów jest aktualnie włączony,obejrzeć transmisję z streamu,dowiedzieć się,który tor jest zajęty oraz otrzymać wyniki z sieci neuronowej wraz z zdjęciem,które było przetwarzane.

Należy zaznaczyć,że na potrzeby developmentu,system odpowiedzialny za zapisywanie zdjęć został podpięty pod filmy,a nie pod stream.
## Algorytmy

Folder ten zawiera wszystkie zaimplementowane algorytmy. List algorytmów:
1.wykrywanie ruchu             
2.wykrywanie zajezdni          
3.wykrywanie peronu            
4.wykrywanie przeszkod         
5.wykrywanie reki              
6.wykrzwanie twarzy            
7.wykrywanie banana 

Ponad to każdy z tych algorytmów został przystosowany do samodzielnego działania. Każdy z nich na wejście przyjmuje klatkę z filmu ewentualnie zdjęcie.

## Sieć neuronowa

Ścieżka do tego modułu jest następująca ``rest_api_pkm2/siec/detect_train.py``. Jest to kolejny komponent,który działa w sposób niezależny. Podczas jego wywoływania należy podać nazwę zdjęcia. Aktualnie ścieżka do zdjęcia została ustawiona na ``rest_api_pkm2/static/``. Flask wymusza taką strukturę projektu,dlatego w tym folderze zdecydowaliśmy się przechowywać zdjęcia do przetwarzania,aby móc je wyświetlić na stronie. Sieć ta została przystosowana do rozróżniania 3 rozdzajów pociągów oraz zajezdni i 2 peronów(Strzyża oraz Kiełpinek). Jako wyjście z sieci neurnowej otrzymujemy plik ``output.txt``,w którym znajdują się informacja co zostało wykryte.


## Rozpoznawanie zajętości torów

Moduł ten można znaleźć ``ALGORYTMY/kamera_z_gory/widok_z_gory.py``. Aby moduł ten działał poprawnie należy wcześniej włączyć rest api. Ponad to podczas uruchamiania algorytmu zaleca się,aby tory nad którymi znajduje się kamera były zupełnie puste. Dzięki temu algorytm będzie w stanie rozpoznać ilość torów na obrazie. Do działania wymagane jest również podpięcie do sieci WETI.

## Aplikacja na Androida

Aby móc poprawnie zainstalować aplikację należy posiadać Android Studio w wersji conajmniej 3.0 oraz posiadać urządzenie z Androidem z Api równym lub wyższym 25. 
Pozwala ona na sterowanie pociągiem(Nr.5) podpiętym do kamery. Wyborem algorytmów w tym sprawdzenie,który jest już ustawiony. Zdecydowanie, w którym momencie ma zostać wykonany zapis ramki do pliku. Możliwe jest także jednoczesne oglądanie streama.

## GUI 

Aplikacja deskoptowa umożliwia dokładnie to samo co aplikacja na Androida,z tym rozszerzeniem,że możliwe jest również oglądanie filmów. Należy pamiętąć,aby wpisać odpowiedni adres IP do pól tesktowych odpowiadającym filmowy lub streamowi.


W razie problemów z konfiguracją lub ewentualne pytania na temat kodu proszę kierować na maila ``marek1cz@gmail.com``
