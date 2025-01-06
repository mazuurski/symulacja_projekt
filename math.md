# Model Matematyczny Symulacji Dziekanatu W4

---

## **Opis systemu**
Model matematyczny opisuje pracę dziekanatu W4 jako system kolejkowy, w którym studenci przychodzą losowo i są obsługiwani przez pracowników przy ograniczonej liczbie stanowisk. System uwzględnia różne strategie organizacji kolejek i zmienne parametry obsługi.

---

## **Założenia modelu**
- **Przyjścia studentów** są zgodne z procesem Poissona o średniej intensywności \(\lambda\) (liczba studentów na jednostkę czasu).
- **Czas obsługi** ma rozkład wykładniczy o średniej \(\mu\) (odwrotność średniego czasu obsługi).
- System posiada \(S\) stanowisk obsługi.
- Organizacja kolejek może działać według strategii:
  - FIFO (pierwszy wchodzi, pierwszy obsługiwany),
  - Losowe przydzielanie,
  - Priorytetyzacja (szybkie sprawy obsługiwane jako pierwsze).

---

## **Parametry modelu**
- \(\lambda\): Intensywność przyjścia studentów.
- \(\mu\): Intensywność obsługi (średnia liczba studentów obsługiwanych na jednostkę czasu przez jedno stanowisko).
- \(S\): Liczba stanowisk obsługi.
- \(L_q\): Średnia liczba studentów w kolejce.
- \(W_q\): Średni czas oczekiwania w kolejce.
- \(L\): Średnia liczba studentów w systemie (kolejka + obsługa).
- \(W\): Średni czas przebywania studenta w systemie (oczekiwanie + obsługa).
- \(P_0\): Prawdopodobieństwo pustego systemu.
- \(P_n\): Prawdopodobieństwo, że w systemie jest \(n\) studentów.

---

## **Równania modelu**

### **Obciążenie systemu:**
\[
\rho = \frac{\lambda}{S \cdot \mu}
\]

### **Prawdopodobieństwo pustego systemu (\(P_0\)):**
\[
P_0 = \left[\sum_{n=0}^{S-1} \frac{(\lambda / \mu)^n}{n!} + \frac{(\lambda / \mu)^S}{S!} \cdot \frac{1}{1 - \rho}\right]^{-1}
\]
gdzie \(\rho < 1\).

### **Średnia liczba studentów w kolejce (\(L_q\)):**
\[
L_q = \frac{P_0 \cdot (\lambda / \mu)^S \cdot \rho}{S! \cdot (1 - \rho)^2}
\]

### **Średni czas oczekiwania w kolejce (\(W_q\)):**
\[
W_q = \frac{L_q}{\lambda}
\]

### **Średnia liczba studentów w systemie (\(L\)):**
\[
L = L_q + \frac{\lambda}{\mu}
\]

### **Średni czas przebywania w systemie (\(W\)):**
\[
W = W_q + \frac{1}{\mu}
\]

---

## **Zakłócenia uwzględniane w modelu**
1. **Nieregularne napływy studentów**: Intensywność \(\lambda\) zmienia się w czasie (\(\lambda(t)\)).
2. **Zróżnicowane czasy obsługi**: Parametr \(\mu\) jest zależny od rodzaju sprawy:
   \[
   \mu_i = \frac{1}{\text{średni czas obsługi typu } i}
   \]
   gdzie \(i\) to indeks typu sprawy.
3. **Nieobecności pracowników**: Losowe zmniejszenie liczby dostępnych stanowisk.

---

## **Wskaźniki oceny**
1. Średni czas oczekiwania (\(W_q\)).
2. Maksymalny czas oczekiwania.
3. Liczba obsłużonych studentów w ciągu dnia.
4. Wykorzystanie stanowisk (procent czasu pracy pracowników).
