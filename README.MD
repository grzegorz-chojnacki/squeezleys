# Squeezley's

## Inicjalizacja
1. Utwórz plik `docker/.env` z adresem email i hasłem administratora:
    ```sh
      ADMIN_MAIL=<email>
      ADMIN_PASSWD=<hasło>
    ```

1. Wygeneruj kategorie i produkty w celu ich zaimportowania:
   ```console
   $ cd ./data/
   $ python3 ./gen-imports.py
   ```
   Wygenerowane dane znajdują się w plikach:
    - `data/products.csv`
    - `data/categories.csv`

   Należy je potem zaimportować w panelu administracyjnym: `Konfiguruj > Zaawansowane > Importuj`


## Uruchamianie

```console
$ cd ./docker/
$ docker-compose up
```

## Dostep:

| Endpoint                | Opis                  |
| ----------------------- | --------------------- |
| `localhost:8080`        | Sklep                 |
| `localhost:8080/admin2` | Panel administracyjny |
| `localhost:8081`        | Panel PHPMyAdmin      |
