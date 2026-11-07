# Разработка Filamentra DataSource

[English](AGENTS.md)

Отдельный каталог реальных 3D-филаментов для будущей интеграции с Filamentra. Это не аддон и не база сертифицированных материалов.

## Общие правила 4FusionLab

- Общие стандарты: https://github.com/4FusionLab/.github/blob/main/AGENTS.md; модель общего CI: https://github.com/4FusionLab/.github/blob/main/RELEASE_PLATFORM.md.
- Общайся и составляй планы на русском, код и UI Fusion — на английском. Сохраняй независимые README.md и README.ru.md.
- Перед изменениями изучай текущие файлы и Git-статус. Conventional Commits; предпочтительно PR с успешными проверками, прямой push в main допускается.
- Не меняй UUID Fusion manifest, IDs команд, поддержку ОС и формат пакета без миграционного плана. Не коммить секреты, токены или личные CAD-файлы.
- Где есть runtime, релиз создаёт push или merge в main только для файлов из .github/release-paths.txt после успешного CI. GitVersion.Tool 6.8.2, неизменяемый автоматический тег и GitHub Release; теги вручную не создавай.
- Изменение docs, README, тестов, AGENTS.md или CI само по себе не должно выпускать релиз. Общие Actions подключай только по конкретному commit SHA.
- Unit-тесты и ZIP не заменяют нативную проверку Autodesk Fusion. Сохраняй существующие ограничения и доказательства совместимости.

## Правила качества данных

- Источники истины: docs/CATALOG_FORMAT.md, docs/VISUAL_DATA_QUALITY.md, docs/MATERIAL_APPEARANCE_SPEC.md и catalog/schema/*.json.
- Не выдумывай производителя, продуктовую линейку, SKU, цвет или измерения. Сохраняй ссылки на официальные источники, единицы, provenance, даты и уверенность.
- Не выдавай маркетинговые swatches за калиброванный цвет. Соблюдай авторские права на фото и текстуры.
- Не ломай стабильные идентификаторы каталога и схему без миграции; учитывай ранее установленные Appearances в пользовательских Fusion-документах.
- Релизными данными считаются только курируемые catalog/brands/**.json, catalog/presets/**.json и catalog/schema/**.json. Исследовательские catalog/sources/** и demo/** не должны сами по себе создавать GitHub Releases.
- Публикация Pages через .github/workflows/publish-demo.yml остаётся ручной; не связывай её автоматически с релизом каталога.
- Для проверки запускай `python tools/validate_catalog.py`, `python -m unittest discover -s tests -v`, `python scripts/build_release.py --version X.Y.Z` и прочие шаги .github/workflows/validate.yml. Ошибка валидации блокирует публикацию.
