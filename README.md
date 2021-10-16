# Jupyter Testbench

## Unit testing za polaznike

Na platformi JupyterHub polaznici na početku sveske učitaju `testbench` modul sa:
```py
from testbench import Testbench
```
Nakon toga pišu kod unutar funkcija **unapred dogovorenih imena i potpisa**, koje testiraju sa `Testbench(ime_funkcije)`. U primeru ispod je napisana i testirana funkcija za računanje faktorijala.

```py
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)

Testbench(factorial)
```

Pokretanjem ovog koda polaznici mogu očekivati 
```
✅ Funkcija 'fac stranetorial' uspešno prolazi sve testove.
```
ukoliko njihova implementacija funkcije prolazi sve testove,
```
⚠️ Funkcija 'factorial' uspešno prolazi 33% testova.
```
ukoliko njihova funkcija prolazi deo test primera, a
```
⛔ Funkcija 'factorial' ne može da se testira! Proverite da li se dobro zove.
```
ako je ime funkcije ili njen potpis pogrešan.

Test primeri koje `Testbench` poziva **nisu** vidljivi polaznicima kako ne bi mogli da kod prilagode da prolazi samo te testove.

## Pisasnje testova

Testovi koje `Testbench` pokreće se nalaze u [`testbench/tests/`](./testbench/tests/) direktorijumu, gde test za svaku funkciju treba da bude u istoimenom Python fajlu. U slučaju `factorial` funkcije, to je [`testbench/tests/factorial.py`](./testbench/tests/factorial.py) koji **mora** da sadrži funkciju potpisa `def test_factorial(bench: 'Testbench')` bez povratne vrednosti. Pomoćne funkcije su dozvoljene.

Parametar `bench` je `Testbench` objekat koji ima sledeće metode potrebne za testiranje:

- `function(...) -> ...` — funkcija koju polaznik piše i prosleđuje `Testbench`-u. Parametri i povratna vrednost zavise od zadatog potpisa funkcije.
- `assert(expr: bool)` — provera da li prosleđena ekspresija vraća `True`.
- `assert_eq(value, truth)` — proverava da li je vrednost `value` jednaka `truth`.
- `assert_range(value: int|float, truth: int|float, error: int|float)` — proverava da li broj `value` pripada opsegu [`truth` - `error`, `truth` + `error`].

Metode za proveru beleže broj uspešnih i neuspešnih testova.

U primeru za računanje faktorijala, funkcija `test_factorial` može izgledati ovako:
```py
def test_factorial(bench: 'Testbench'):

    bench.assert_eq(bench.function(0), 1)
    bench.assert_eq(bench.function(1), 1)
    bench.assert_eq(bench.function(2), 2)
    bench.assert_eq(bench.function(3), 6)
    bench.assert_eq(bench.function(5), 120)
```

Parametar `value`, u metodi za proveru jednakosti `assert_eq`, је povratna vrednost funkcije koja se testira, a `truth` je tačna vrednost koja se očekuje. Provera ne mora biti mnogo, ali je bitno da **pokrivaju sve razumne granične slučajeve**.

Na kraju je potrebno da se u [ `testbench/tests/__init__.py`](./testbench/tests/__init__.py) eksportuju sve napisane funkcije za testiranje:
```py
from .fibonacci import test_fibonacci
```

### Poređenje kompleksnijih podataka

Ako funkcija koja se testira radi na podacima poput slika ili matrica brojeva, takvi podaci se mogu čuvati unutar direktorijuma sa imenom funkcije u `testbench/tests/`; u slučaju primera `factorial` to bi bio direktorijum `testbench/tests/factorial/`.

Učitavanje podataka pred poređenje se može vršiti u pomoćnim funkcijama unutar test fajla ili u samoj funkciji za testiranje.

Ukoliko tip podataka zahteva spoljne biblioteke za učitavanje i obradu, one se `import`-uju u test fajl i dodaju se u niz `install_requires` unutar [`setup.py`](./setup.py)

### Podaci za poređenje pristupni polaznicima

Slično prethodnoj podsekciji, fajlove sa podacima nad kojima polaznici mogu samostalno da pozivaju implementiranu funkciju smestiti u direktorijum [`datasets/`](./datasets/); u slučaju primera to bi bio direktorijum `datasets/factorial/`.

Podaci treba da budu jasno organizovani i smisleno imenovani da ne zbune polaznike.

### Referentna implementacija i provera unit testova

U fajlu [`user_demo.py`](./user_demo.py) treba napisati referentnu implementaciju funkcije koja se testira i pozvati `Testbench(ime_funkcije)` nad njom kao što je to urađeno za primere u tom fajlu.

## Slanje izmena u git repozitorijum

Testovi napisani za svaku radionicu se čuvaju **u zasebnoj git grani** sa imenom oblika `prezime-saradnika_ime-radionice` kako ne bi došlo do konflikata.

Primere `fibonacci`, `factorial` i `is_even` treba obrisati.

Ako neki saradnik pošalje izmene na `master` granu, one će biti obrisane!
