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
$ sv list words fr
+----------+-------------+----------+----------+
| fr       | en          | ru       | bucket   |
|----------+-------------+----------|----------|
| souvenir | to remember | помнить  | 1        |
| parler   | to speak    | говорить | 3        |
+----------+-------------+----------+----------+
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
