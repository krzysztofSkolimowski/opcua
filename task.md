# Stacja Pogodowa OPC-UA
W oparciu o kody źródłowe utworzenie serwera oraz skonfigurowanie przestrzeni adresowej serwera zrealizować wirtualną stację pogodową o następujących funkcjach:

#### 1. Odczyt danych pogodowych z różnych źródeł poprzez Internet oraz ich udostępnienie w postaci danych serwera OPC UA. Zaprojektować odpowiednią przestrzeń adresową.

**status:gotowe**    

serwer zbiera dane za pomocą publicznego  API: <https://openweathermap.org/api> openweathermap pokazuje pogodę mierzoną na stacjach pogodowych. 

Możliwa jest zmiana lokalizacji pomiarów pogody.

Wykorzystywany jest restowy klient http. 

Przestrzeń adresowa, w przez którą udostępniana jest pogoda, składa się z 4 węzłów: 

| BrowseName | NodeID   | opis | 
|---|---|---|
| 2:time |  ns=2 i=1| przechowuje czas ostatniej aktualizacji pogody |
| 3:today | ns=3 i=1 | przechowuje obecną pogodę |
| 4:tomorrow | ns=4 i=1 | przechowuje jutrzejszą prognozę pogody |
| 5:day_after | ns=5 i=1 | przechowuje prognozę pogody na pojutrze |
   
Ich dokładne parametry są opisane w następnym punkcie. 


#### 2. Odczyt prognozy pogody (2-3 dni) oraz jej udostępnienie poprzez OPC UA.
**status:gotowe**
Odczytywana jest pogoda: 
1. bieżąca
1. jutrzejsza
1. następnego dnia
   
w formie:
```
"temperature" : przwidywana średnia temperatura [C°]
"humidity" : wilgotność [%]
"pressure" : ciśnienie [hPA]
"wind_speed" : prędkość wiatru [m/s]
"wind_direction" : kierunek wiatru [°] 
"clouds" : zachmurzenie [%] 
"conditions" : warunki [status:string] np "clear sky" lista dostępnych: https://openweathermap.org/weather-conditions
"time" : [int - UNIX TIME]
```
Dane są rzutowane i zapiywane w węzłach:

| BrowseName | NodeID   |
|---|---|
| 3:today |  ns=2 i=1|
| 4:tomorrow | ns=3 i=1 |
| 3:day_after | ns=4 i=1 |

i wystawiane poprzez zdefiniowany endpoint opcua: ```opc.tcp://127.0.0.1:4840/weather```
  
 
| Unix Time? Dlaczego nie timestamp, w określonym formacie? |
| --- |
|  Unix Time Stamp - czas POSIX system reprezentacji czasu mierzący liczbę sekund od początku 1970 roku UTC | 
| Zastosowanie go było świadomą decyzją z następujących powodów: serwer freeopcua, z którego korzystałem, ma już zaimplementowane zapisywanie timestampa ostatniej modyfikacji każdej zmiennej w formacie `yyyy-mm-dd[T]hh:mi:sec.nanosec`-  ponowna implementacja już gotowej funkcjonalności nie jest dobrym rozwiązaniem. 
| Czas unixowy został stworzony nie bez pozodów, jest to najbardziej uniwersalny format, który działa bardzo szybko, ze względu na brak konieczności parsowania stringów, których format na każdym urządzeniu (systemie) może być różnym w dodatku ze względu na wygodę w użytkowaniu, wyklucza ogromną ilość błędów.|
| Jego główne wady: okropna czytelność dla człowieka i maksymalna dokładność 1s nie są istotne w przypadku aplikacji - nie ma potrzeby częstego wyświetlania czasu w interfejsie graficznym, a częstotliwość odświeżania pomiarów to 15 minut.| 
| Dodatkowo zaimplementowane jest logowanie po stronie serwera, które również powiela tą samą funkcjonalność | 
  
#### 3. Okresowe (np. co 15 minut) odczytywanie danych pogodowych oraz prognozy. Czas odczytu danych ustawiać jako stemple czasowe udostępnianych danych. W przypadku braku łączności odpowiednio ustawiać informacje o jakości danych. Zrealizować metodę określającą częstotliwość odświeżania.
**status:gotowe**

Serwer impelentuje okresowe odświeżanie danych pogodowych. 
Dodatkowo czas odświeżania jest konfigurowalny przy pomocy pliku konfiguracyjnego ".env" (więcej informacji w następnym punkcie).
Czas jest zapisywany w formacie czas POSIX, ze względu na już gotową implementacje timestampu po stronie serwera. 

W przypadku braku łączności z siecią lub błędem po stronie API pogodowego, 
serwer będzie oczekiwać na odzyskanie łączności i automatycznie zaktualizuje 
dane w momencie jej odzyskania. Cały czas widoczny jest 

#### 4. Zaimplementować metodę wymuszającą natychmiastowy odczyt ww. danych.
**status:gotowe, z drobnym problemem**

Implementacja metod w kodzie serwera, którego używam nie do końca działa. 
Naprawienie go wymagałoby commitowania do zewnętrznego repozytorium 
i zaakceptowania przez twórców serwera. 
W dodatku nie będzie to takie proste.

Z tego powodu postanowiłem zaimplementować RESTowy
endpoint działający na HTTP, który umożliwia 
wymuszenie akutalizacji wartości pogody. 
Implementacja metody opcua jest pozostawiona w komentarzach, oznaczona jako "todo"

#### 5. Zaimplementować opcję logowania wszystkich danych udostępnianych przez serwer.
**status:gotowe**

Domyślny poziom logowania ustawiony jest na poziom: INFO. 
logi domyślnie zapisują się w pliku: weather_station.log

logowanie także można skonfigurować z poziomu pliku konfiguracyjnego (poziom logowania i plik z logami).

Tabela z poziomami logowania: 

| poziom | kod |
| --- | --- | 
| CRITICAL |  50 |
| FATAL |  50 |
| ERROR |  40 |
| WARN |  30 |
| INFO |  20 |
| DEBUG |  10 |
| NOTSET |  0 |

uwaga: terminal pythonowy logger domyślnie wyświetla w terminalu logi o poziomie WARN lub wyższym. Można to zmienić w konfiguracji środowiska. 
#### 6. Opcjonalnie opcja korzystania z więcej niż jednego źródła informacji o pogodzie wraz z metodą wyboru aktualnego źródła lub odpowiednio rozszerzoną przestrzenią adresową.

Domyślam się, że chodzi tutaj o większą ilość providerów API - to zaimplementowane nie jest. 
Można natomiast wybrać stację pogodową, z której odczytywany jest pomiar - funkcjonalność ta udostępniena jest prze <https://openweathermap.org/api>
Czasami dwóch różnych providerów korzysta z tej samej stacji. 


#### 7. Dodkatkowe rzeczy, których nie było w poleceniu: 

Stacja jest konfigurowalna, poprzez plik konfiguracyjny. Można zdefiniować kilka własnych środowisk i odpalać inne na każdej instancji1. Domyślnie zdefiniowane jest dev. Zdefiniowane jest środowisko testowe. 

Automatycznie testuje czy serwer opcua działa i czy workspace został poprawnie ziinicjalizowany. Działa to dopiero po wcześniejszym uruchomieniu stacji. 

***Jak uruchumoić stację?***
Mimo, że wszystko powinno działać na Windowsie, najlepiej uruchomić na Linuxie - nie posiadam niestety Windowsa, żeby to sprawdzić. 

- najpier należy upewnić się, że zainstalowane są wymagania: 
```sudo pip install -r requirements.txt```
- następnie: 
```python3 main.py```
- w przypadku problemów usunąć katalog ```venv``` i stworzyć go ponownie ```python3 -m venv /path/to/new/virtual/environment```, następnie ponownie zainstalować wymagane pakiety: ```sudo pip install -r requirements.txt```
Jak uruchomić test? 
```python -m unittest```


#### 8. Dalszy rozwój: 
Poza ostatnim opcjonalnym podpunktem, udało się zrealizować wszystkie wytyczne. Żeby doprowadzić projekt do możliwego udostępnienia go światu i użytkowania przez zewnętrznych użytkwoników, w przyszłości można zaimplementować: 
- tls - szyfrowanie zapytań
- uwierzytelnianie klientów najlepiej przez generowane tokeny albo przez hasło
- z uwagi na dużą ilość logów, możńaby je wysyłać na elastic searcha, albo inną bazę danych do tego przeznaczoną - przy większym ruchu (generowanym automatycznie) pliki mogą okazać się mało wyydajne po dłuższym czasie.
- konteneryzacja aplikacji - żeby umożliwić deploy serwera do chmury, umożliwić skaowania, orkiestrować serwisami.