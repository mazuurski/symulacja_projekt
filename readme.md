# Symulacja pracy dziekanatu W4

## Obiekt
Dziekanat Wydziału W4, obsługujący kierunki:
- Inżynieria systemów  
- Informatyka stosowana  
- Cyberbezpieczeństwo  

---

## Cel
Ocena efektywności pracy dziekanatu oraz identyfikacja optymalnych strategii obsługi studentów w zależności od parametrów takich jak liczba pracowników, godziny otwarcia i sposób organizacji kolejek.

---

## Hipotezy
1. Jeśli kolejka jest priorytetyzowana od najszybszych spraw, to średni czas oczekiwania się skróci.  
2. Jeśli będziemy losować ludzi z kolejki, to średni czas oczekiwania będzie krótszy.  
3. Istnieje optymalna liczba stanowisk, powyżej której nie skróci się średni czas oczekiwania.  
4. Przy podziale na kierunki, średni czas oczekiwania jest krótszy niż przy podziale na specjalności lub przy braku podziału.  

---

## Wejścia (+ Zakłócenia)

### Wejścia:
- Liczba studentów przychodzących do dziekanatu w określonych godzinach.  
- Typy spraw studentów: odbiór dokumentów, składanie wniosków, pytania informacyjne.  
- Czas obsługi pojedynczego studenta w zależności od rodzaju sprawy.  
- Liczba stanowisk obsługi oraz liczba pracowników.  
- Godziny otwarcia dziekanatu.  

### Zakłócenia:
- Nieregularne napływy studentów (np. w szczytach związanych z rejestracją, składaniem podań).  
- Nieobecność pracowników (choroby, urlopy).  
- Studenci z wydłużonym czasem obsługi (np. złożone sprawy, błędne dokumenty).  

---

## Wyjścia
- Czas oczekiwania studentów w kolejce.  
- Liczba obsłużonych studentów w ciągu dnia.  
- Średni czas obsługi jednego studenta.  
- Wykorzystanie zasobów: czas wolny pracowników.  

## Macierz parametrów dla symulacji dziekanatu

| **Kategoria**                | **Deterministyczne**                                                                 | **Losowe**                                                                  |
|-------------------------------|-------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Zależne**                  | - Czas oczekiwania w kolejce (zależny od liczby studentów i stanowisk)               | - Czas trwania obsługi zależny od rodzaju sprawy i doświadczenia pracownika |
|                               | - Liczba obsłużonych studentów (zależna od liczby stanowisk i godzin otwarcia)       | - Liczba studentów w szczycie zależna od okresu w roku (np. rekrutacja)     |
|                               | - Wykorzystanie pracowników (zależne od liczby stanowisk i napływu studentów)       | - Obciążenie pracowników zależne od zmiennych losowych (np. zakłócenia)     |
| **Niezależne**               | - Liczba stanowisk obsługi                                                           | - Przypadkowy czas przybycia studentów do dziekanatu                        |
|                               | - Godziny otwarcia dziekanatu                                                       | - Zakłócenia (np. nagła awaria systemu)                                     |
|                               | - Organizacja kolejek (np. losowe przydzielanie, priorytetyzacja)                   | - Liczba nieobecnych pracowników z przyczyn losowych                        |



## Wskaźniki oceny:

- Średni czas oczekiwania
- Maksymalny czas oczekiwania

## Rodzaje badań:
- Podział na kierunki vs podział na specjalności vs brak podziału
- Kolejka kto pierszy ten lepszy vs kolejka priorytetyzowana vs kolejka losowa 

