# No Code

The best way to write secure and reliable applications. Write nothing; deploy nowhere.

Inspired by [Kelsey Hightower's project](https://github.com/kelseyhightower/nocode).

## Getting started

After cloning the repository, do:

```
poetry install
```

## REPL

Try out the interpreter:

```
nocode
```

## Compile

Compile your program to distribute it more easily.

```
nocode compile <FILE> --output <OUTPUT_FILE>
```

Supports many languages such as C, C++ or Python:

```
nocode compile <FILE> --target <c|cpp|py>
```

## Run

Run your blazingly fast 🚀 program in one command.

```
nocode run <FILE>
```

## Deploy

Your reliable software deserves to be seen by noone. Deploy nowhere in one command.

```
nocode deploy
```

To deploy on a specific port:

```
nocode deploy --port <PORT>
```

## Format

Format your project at the speed of light.

```
nocode format --file <FILE>
```

## Autofix

Fix automatically your boilerplate using the power of AI, in the blink of an eye.

```
nocode autofix <FILE>
```
