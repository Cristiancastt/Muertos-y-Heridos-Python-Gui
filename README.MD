# Mastermind

Mastermind es un juego de lógica en el que debes adivinar un número secreto de 4 dígitos. Muertos son los dígitos correctos en la posición correcta y Heridos son los dígitos correctos en la posición incorrecta.

## Requisitos

Asegúrate de tener instalado Python en tu sistema. Además, necesitarás instalar el módulo `customtkinter` para la interfaz gráfica. Puedes instalarlo con el siguiente comando:

```bash
pip install customtkinter
```
O ejecutar un cmd en la carpeta local y ejecutar:
```bash
pip install -r requirements.txt
```

## Cómo jugar

    Ejecuta el juego proporcionando tu nombre.
    Se generará un número de 4 dígitos aleatorio que deberás adivinar.
    Introduce un número de 4 dígitos en el campo de entrada y presiona el botón "Comprobar".
    El juego te dará pistas en forma de Muertos (dígitos correctos en la posición correcta) y Heridos (dígitos correctos en la posición incorrecta).
    Continúa adivinando hasta que adivines el número secreto o alcances el límite de intentos.

## Características

    Modo Debugger: Si introduces "debugger" como tu nombre, se mostrará el número secreto al inicio del juego.
    Ranking: El juego guarda tus mejores resultados en un ranking, incluyendo el número de intentos y el tiempo que te llevó adivinar el número.
    Historial de Números: Puedes navegar por los números que has ingresado previamente con las teclas de flecha arriba y abajo en el campo de entrada.
    Salida del juego: Puedes salir del juego en cualquier momento.

## Comandos

    Para jugar, presiona el botón "Jugar" en el menú principal.
    Puedes consultar el ranking de los mejores jugadores presionando el botón "Ranking".
    Para salir del juego, utiliza el botón "Salir".

## Autor
Este juego fue desarrollado por Cristian Castiñeiras como un proyecto para SGE.
