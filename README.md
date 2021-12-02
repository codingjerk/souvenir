# Souvenir

> Little CLI program which helps creating and viewing flashcards

## Usage

```sh
$ cat words.yml

- fr: souvenir
  en: to remember
  ru: помнить

- fr: parler
  en: to speak
  ru: говорить
```

```sh
$ sv list words
+----------+-------------+----------+
| fr       | en          | ru       |
|----------+-------------+----------|
| souvenir | to remember | помнить  |
| parler   | to speak    | говорить |
+----------+-------------+----------+
```

```sh
$ sv repeat words fr
=> souvenir
   en: to remember
   ru: помнить
=| correct? [y/n]

=> parler
   en: to speak
   ru: говорить
=| correct? [y/n]
```
