# Symulacja dziekanatu

obiekt: dziekanat W4 (wersja skrócona, kierunki:
inżynieria systemów, informatyka stosowana, cyberbezpieczeństwo)

cel: (+hipotezy)
Ocena efektywności pracy dziekanatu oraz identyfikacja optymalnych strategii obsługi studentów w zależności od parametrów takich jak liczba pracowników, godziny otwarcia i sposób organizacji kolejek.

Hipotezy:
'Jeśli kolejka jest priorytetyzowana od najszybszych spraw, to średni czas oczekiwania się skróci'
'Jeśli będziemy losować ludzi z kolejki, to średni czas oczekiwania będzie krótszy'
'Istnieje optymalna ilość stanowisk, powyżej której nie skróci się średni czas oczekiwania'
'Przy podziale na kierunki, średni czas oczekiwania jest krótszy niż przy podziale na specjalności lub przy braku podziału'

wejścia(+zakłócenia)/wyjścia:
Wejścia i zakłócenia:
Wejścia:
Liczba studentów przychodzących do dziekanatu w określonych godzinach.
Typy spraw studentów: odbiór dokumentów, składanie wniosków, pytania informacyjne.
Czas obsługi pojedynczego studenta w zależności od rodzaju sprawy.
Liczba stanowisk obsługi oraz liczba pracowników.
Godziny otwarcia dziekanatu.
Zakłócenia:
Nieregularne napływy studentów (np. w szczytach związanych z rejestracją, składaniem podań).
Nieobecność pracowników (choroby, urlopy).
Dodatkowe zadania dla pracowników (np. nagłe polecenia z administracji).
Niepełne dane dostarczane przez studentów (wydłużenie czasu obsługi).
Wyjścia:
Czas oczekiwania studentów w kolejce.
Liczba obsłużonych studentów w ciągu dnia.
Średni czas obsługi jednego studenta.
Wykorzystanie zasobów: obciążenie stanowisk obsługi, czas wolny pracowników.
Zadowolenie studentów: na podstawie czasu obsługi i czasu oczekiwania.
Podział parametrów:
Parametry deterministyczne:
Liczba stanowisk obsługi.
Godziny otwarcia dziekanatu.
Liczba pracowników na zmianie.
Maksymalna liczba studentów mogąca wejść do dziekanatu w jednej chwili (ograniczenie przestrzeni).
Parametry losowe:
Czas przybycia studentów do dziekanatu (zmienny w ciągu dnia).
Czas trwania obsługi dla różnych typów spraw.
Liczba studentów w ciągu dnia (szczególnie w okresach wzmożonej aktywności).
Przypadki nieregularnych zakłóceń (np. awaria systemu komputerowego).
Parametry zależne:
Czas oczekiwania w kolejce zależy od liczby studentów i liczby dostępnych stanowisk obsługi.
Obciążenie pracowników zależy od liczby i rodzaju spraw.
Średni czas obsługi zależy od skomplikowania spraw i doświadczenia pracownika.
Parametry niezależne:
Harmonogram godzin otwarcia.
Liczba stanowisk obsługi.
Polityka organizacji kolejek (np. priorytetyzacja, losowe przydzielanie).


podzial parametrow na: deterministyczne/losowe i zalezne/niezalezne

wskaźniki oceny:
efektywnosc
'sredni czas oczekiwania'
'maksymalny czas oczekiwania'

rodzaje badań:
'podział na kierunki vs podział na specjalności vs brak podziału'\
'kolejka kto pierszy ten lepszy vs kolejka priorytetyzowana vs kolejka losowa' 

