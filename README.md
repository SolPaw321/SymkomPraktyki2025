```bash
pip install ansys-geometry-core


# Temat: Modelowanie turbin wiatrowych

Cel: opracowanie szczegółowego tutorialu w formie prezentacji PowerPoint ukazującego proces przygotowywania geometrii, siatkowania i prowadzenia symulacji wariantowych na przykładzie turbiny wiatrowej o pionowej osi obrotu w środowisku PyAnsys, celem przeprowadzenia obliczeń w sposób zautomatyzowany.

Format: prezentacja w udostępnionym szablonie Symkom

Struktura: tutorial powinien ukazywać kolejno wszystkie etapy, w tym zawierać:
 - konieczny kod  w Pythonie wraz z komentarzem i istotnymi uwagami z punktu widzenia użytkownika, 
 - zrzuty z wygenerowaną geometrią
-  zrzuty z wygenerowaną siatką obliczeniową
Fragment kodu na slajdzie powinien pokrywać się z ukazywanymi grafikami i komentarzem.

Kroki do uwzględnienia: tworzenie turbin o pionowej osi obrotu VAWT, gdzie użytkownik będzie mógł sterować:
 - liczbą łopatek
 - kątem natarcia łopatek
 - rodajem profilu
 - długością łopatek
 - odległością łopatek od środka. 

Środek turbiny powinien leżeć w środku układu współrzędnych, profil wyciągnięty w kierunku osi Z. Geometria powinna zawierać dodatkową objętość z polem zagęszczeń (tzw. Body of Influence). Zalecany algorytm siatkowania to Sweep/Mutlizone. 

Symulacja we Fluencie powinna uwzględniąć analizę wariantową dla różnych:
 - geometrii
 - prędkości nawiewu wiatru
 - prędkości obrotowych turbiny

W prowadzonej analizie użytkownik powinien mieć wgląd w raporty z każdej symulacji ukazujące residua, moment i moc na turbinie, prędkość obrotową, bilans masy. Użytkownik powinien móc na bazie symulacji ocenić ich wiarygodność i przeprowadzić konieczny post-processing danych, z możliwością podglądu konturu modułu prędkości w domenie co n iteracji. Na dysku został zamieszczony przykładowy projekt turbiny 3D_3_mrf jako punkt odniesienia











