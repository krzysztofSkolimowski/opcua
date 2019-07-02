# Stacja Pogodowa OPC-UA
W oparciu o kody źródłowe utworzenie serwera oraz skonfigurowanie przestrzeni adresowej serwera zrealizować wirtualną stację pogodową o następujących funkcjach:

1. Odczyt danych pogodowych z różnych źródeł poprzez Internet oraz ich udostępnienie w postaci danych serwera OPC UA. Zaprojektować odpowiednią przestrzeń adresową.

    **status:gotowe**    
    
    serwer zbiera dane za pomocą publicznego  API: <https://openweathermap.org/api> openweathermap pokazuje pogodę mierzoną na stacjach pogodowych. Możliwa jest zmiana lokalizacji pomiarów pogody.
	Wykorzystywany jest restowy klient http. 


1. Odczyt prognozy pogody (2-3 dni) oraz jej udostępnienie poprzez OPC UA.

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

	 i wystawiane poprzez zdefiniowany endpoint: ```opc.tcp://127.0.0.1:4840/weather```
	 
	 | Unix Time? Dlaczego nie timestamp, w określonym formacie? |
	 | --- |
	 |  Unix Time Stamp - czas POSIX system reprezentacji czasu mierzący liczbę sekund od początku 1970 roku UTC | 
	 | Zastosowanie go było świadomą decyzją z następujących powodów: serwer freeopcua, z którego korzystałem, ma już zaimplementowane zapisywanie timestampa ostatniej modyfikacji każdej zmiennej w formacie `yyyy-mm-dd[T]hh:mi:sec.nanosec`-  ponowna implementacja już gotowej funkcjonalności nie jest dobrym rozwiązaniem. 
	 |Czas unixowy został stworzony nie bez pozodów, jest to najbardziej uniwersalny format, który działa bardzo szybko, ze względu na brak konieczności parsowania stringów, których format na każdym urządzeniu (systemie) może być różnym w dodatku ze względu na wygodę w użytkowaniu, wyklucza ogromną ilość błędów.|
	 |Jego główne wady: okropna czytelność dla człowieka i maksymalna dokładność 1s nie są istotne w przypadku aplikacji - nie ma potrzeby częstego wyświetlania czasu w interfejsie graficznym, a częstotliwość odświeżania pomiarów to 15 minut.| 
    
1. Okresowe (np. co 15 minut) odczytywanie danych pogodowych oraz prognozy. Czas odczytu danych ustawiać jako stemple czasowe udostępnianych danych. W przypadku braku łączności odpowiednio ustawiać informacje o jakości danych. Zrealizować metodę określającą częstotliwość odświeżania.

    **status:gotowe**
    
    Serwer impelentuje okresowe odświeżanie danych pogodowych. Dodatkowo czas odświeżania jest konfigurowalny przy pomocy pliku konfiguracyjnego.
    Czas jest zapisywany w formacie czas POSIX, ze względu na już gotową implementacje timestampu po stronie serwera. 
    
    W przypadku braku łączności serwer będzie oczekiwać na odzyskanie łączności i automatycznie zaktualizuje dane w momencie jej odzyskania. Cały czas widoczny jest 


1. Zaimplementować metodę wymuszającą natychmiastowy odczyt ww. danych.

1. Zaimplementować opcję logowania wszystkich danych udostępnianych przez serwer.

1. Opcjonalnie opcja korzystania z więcej niż jednego źródła informacji o pogodzie wraz z metodą wyboru aktualnego źródła lub odpowiednio rozszerzoną przestrzenią adresową.