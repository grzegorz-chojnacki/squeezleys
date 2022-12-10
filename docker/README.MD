# Odpalenie

## Pierwsze odpalenie

Ze wzgledu na brak sprawdania heartbeatu miedzy DB a prestashop, przy pierwszym odpaleniu prestashop wstanie zanim DB sie odpali

Wystarczy zrobic

``docker-compose up``

zamknac kontenery po odpaleniu bazy

usunac volume prestashop

i ponownie ``docker-compose up``

## Kolejne odpalenia

``docker-compose up``