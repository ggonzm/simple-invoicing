# simple-invoicing
Desarrollo de una aplicación para la expedición de facturas y albaranes en un pequeño negocio.
La aplicación en sí consiste principalmente en operaciones CRUD alrededor de una base de datos, pero
se desea disponer de una gran flexibilidad a la hora de asignar precios a diferentes productos, además
de la funcionalidad principal de generar facturas/albaranes.

El proyecto sigue el libro [Architecture Patterns with Python](https://www.cosmicpython.com/book/preface.html) con el objetivo de profundizar en técnicas de desarrollo de software de calidad, como son:
* Arquitectura hexagonal / _Clean Architecture_ / _Onion Architecture_
* _Domain Driven Devlopment_ (DDD)
* _Test Driven Development_ (TDD)
* Patrones de diseño: 
    * _Repository Pattern_
    * _Unit of Work Pattern_
    * _Model-View-Controller_ (MVC)
    * _Factory Pattern_
    * _Observer Pattern_

Dado que la aplicación resultante será utilizada por un único usuario, dicha aplicación se ajusta a una arquitectura monolítica, por lo que mayoritariamente se implementa la [Parte 1](https://www.cosmicpython.com/book/part1.html) del libro citado, aunque la interfaz gráfica poseerá ciertas funcionalidades basadas en eventos.

## Tecnologías
* [PDM](https://pdm-project.org/latest/)
* Git
* [Ruff](https://docs.astral.sh/ruff/formatter/)
* SQLite
* Pyright
* Pytest
* Tkinter
* Trello
