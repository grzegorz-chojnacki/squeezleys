# Squeezley's

## Inicjalizacja
Utwórz plik `docker/.env` z adresem email i hasłem administratora:
```sh
  ADMIN_PASSWORD=<hasło>
  SMTP_PASSWORD=<haslo>
```

## Uruchamianie

```console
$ cd ./docker/
$ docker-compose up
```

Po zainstalowaniu PrestaShop należy wejść do panelu administracyjnego i przejść do widoku importu:

`Konfiguruj > Zaawansowane > Importuj`

Tu należy kolejno zaimportować pliki CSV z katalogu `./data/`:
1. `./data/categories.csv`
2. `./data/products.csv`
3. `./data/combinations.csv`

Przy imporcie warto zaznaczyć usunięcie istniejących kategorii/produktów/kombinacji i wymuszenie używania ID.

Należy upewnić się, że kolumny zostały dobrze odwzorowane w narzędziu importowania.

## Przywrócenie ustawień domyślnych

```console
$ cd ./docker/
$ docker-compose down
$ docker volume rm docker_db_data docker_shop
```

## Dostep

| Endpoint                | Opis                  |
| ----------------------- | --------------------- |
| `localhost:8080`        | Sklep                 |
| `localhost:8080/admin2` | Panel administracyjny |
| `localhost:8081`        | Panel PHPMyAdmin      |


## Ponowny scrapping

W celu ponownego przeprowadzenia scrappingu należy wykonać następujące kroki:
1. Upewnić się, że zależności środowiska python (`./requirements.txt`) są spełnione

2. Wejść do katalogu `./scrap/`

3. Zescrapować produkty (widoczne podczas przeglądania kategorii):
   ```console
   $ python3 ./scrap.py
   ```

4. Powstały plik `scrapped.json` zawiera zduplikowane produkty, należy je usunąć:
   ```console
   $ python3 ./deduplicate.py
   ```

5. Niektóre produkty posiadają warianty, do których niestety nie prowadzą żadne linki dostępne w źródłach stron. Żeby pobrać ich dane należy uruchomić skrypt `./variants.py` **(wykorzystujący Selenium i przeglądarkę Chromium)**.
   ```console
   $ python3 ./variants.py
   ```
   ***TODO:** dołączyć pobieranie wariantów do skryptu `./scrap.py`*

6. Pełne zescrapowane dane można teraz przekształcić do bardziej użytecznej struktury produktów sklepowych:
   ```console
   $ python3 ./transform.py
   ```
   Powstałe pliki `./products.json` oraz `image-urls` zawierają dump produktów i odnośniki do zdjęć do nich przypisanych.
   Skrypt automatycznie przekształca linki zdjęć do nazw plików trzymanych lokalnie.

7. Należy pobrać zdjęcia za pomocą skryptu `./image-scrap.sh`
   ```console
   $ bash ./image-scrap.sh
   ```
   Skrypt automatycznie zapisuje zdjęcia pod takim samym formatem nazwy, jak robi to skrypt `./transform.py`.

8. Mając zdjęcia i listę produktów można teraz wygenerować pliki CSV, które posłużą do importowania danych do sklepu:
   ```console
   $ python3 ./gen-imports.csv
   ```
