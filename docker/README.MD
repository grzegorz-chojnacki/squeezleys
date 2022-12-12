# Odpalenie

1. Utwórz plik `docker/.env` z adresem email i hasłem administratora:
    ```sh
      ADMIN_MAIL=<email>
      ADMIN_PASSWD=<hasło>
    ```
1. Skomponuj obrazy:
    ```console
    $ docker-compose up
    ```

# Dostep:

| Endpoint                | Opis      |
| ----------------------- | --------- |
| `localhost:8080`        | Sklep     |
| `localhost:8080/admin2` | Dashboard |
