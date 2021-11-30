# Souvenir

> Little CLI program which helps creating and viewing flashcards

## Usage

```sh
$ sv new french
```

```sh
$ sv add souvenir memory
```

```sh
$ sv list
+------------+----------+---------+--------+----------+
| Question   | Answer   |   Views |   Hits |   Misses |
|------------+----------+---------+--------+----------|
| souvenir   | memory   |       0 |      0 |        0 |
+------------+----------+---------+--------+----------+
```

```sh
$ sv repeat --times 50
... [ Interactive repeat session ] ...
```
