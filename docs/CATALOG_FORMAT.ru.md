# Формат каталога Filamentra

[English](CATALOG_FORMAT.md)

> **Предрелизная схема v1.** Документ описывает текущий контракт исходных данных. Точные свойства, наследование, происхождение и сопоставление с Autodesk Fusion API приведены в [спецификации внешнего вида материала](MATERIAL_APPEARANCE_SPEC.md).

## Структура каталогов

```text
catalog/
├── brands/
│   ├── README.md
│   └── bambu-lab/
│       ├── brand.json
│       └── pla-matte.json
├── presets/
│   ├── pla-matte.json
│   ├── pla-glossy.json
│   ├── pla-silk.json
│   ├── petg-standard.json
│   ├── petg-translucent.json
│   ├── fiber-matte.json
│   └── sparkle-polymer.json
├── assets/                     # Optional future maps with redistribution rights
└── schema/
    ├── line.schema.json
    └── preset.schema.json
```

**Логическая иерархия:** производитель → базовый полимер (PLA или PETG) → линейка → цвет. Для каждой линейки создаётся один JSON-файл; полимер хранится как свойство, а не физический каталог. Отделка и оптические эффекты остаются атрибутами.

## Идентификаторы продуктов

- ID бренда: `bambu-lab`
- ID линейки: `bambu-lab/pla-matte`
- ID цвета: `ash-gray`
- Полный идентификатор внешнего вида: `bambu-lab/pla-matte/ash-gray`

Полный ID должен оставаться стабильным независимо от SKU и переведённого отображаемого названия. Размеры упаковки, катушки и сменные блоки не являются отдельными цветами.

## JSON линейки

```json
{
  "schema_version": 1,
  "id": "bambu-lab/pla-matte",
  "brand": "bambu-lab",
  "name": "PLA Matte",
  "polymer": "PLA",
  "finish": "matte",
  "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
  "appearance_preset": "pla-matte",
  "colors": [
    {
      "id": "ash-gray",
      "name": "Ash Gray",
      "manufacturer_color_code": "11102",
      "hex": "#9B9EA0",
      "hex_source": "manufacturer",
      "source_url": "https://bambu-lab-global.myshopify.com/products/pla-matte",
      "verified_on": "2026-11-04"
    }
  ]
}
```

В этом фрагменте указан один цвет. [Текущий файл Bambu Lab PLA Matte](../catalog/brands/bambu-lab/pla-matte.json) содержит **25 официальных цветовых вариантов** из закреплённого [реестра производителя BambuStudio](../catalog/sources/bambu-lab.json).

## Наследование внешнего вида и происхождение полей

Аддон последовательно обрабатывает `preset.appearance`, необязательный `appearance` линейки и необязательный `appearance` конкретного цвета **по каждому ключу**. Базовый цвет задаётся полем `hex` варианта, а не свойством пресета.

Рендерер поддерживает `surface_type`, `roughness`, `opacity`, оценочное `transmission` (0–1), `ior`, `attenuation_distance_mm` и необязательное `textures`. В Pages Three.js использует оценочное пропускание для образца толщиной 2 мм; будущий адаптер Fusion должен сопоставлять прозрачность через поддерживаемую модель свойств Fusion. Расширенная шкала прозрачности требует проверки в Fusion.

Линейка или цвет с переопределением `appearance` должны включать `appearance_sources`, где каждый изменённый ключ помечен как `manufacturer`, `measured` или `filamentra_estimate`. Для опубликованного HEX происхождение `hex_source` задаётся отдельно.

Пресеты являются **явными оценками**, пока не будут отдельно откалиброваны и проверены в Fusion. Они не становятся автоматически спецификациями производителя. Отсутствующие значения цветов остаются отсутствующими.

### Многоцветность и прозрачность

- `rgba_swatches` сохраняет один или несколько точных отображаемых производителем образцов RGBA из восьми символов, если они доступны (сейчас BambuStudio).
- `color_mode`: `solid`, `gradient`, `multicolor` или `unknown`. Gradient и multicolor сохраняют все опубликованные цвета, **а не выдуманный единый HEX**.
- Альфа-канал RGBA из интерфейса поставщика **не** является измеренным коэффициентом оптического пропускания; Clear в BambuStudio представлен как `#00000000` и намеренно не имеет `hex`.
- `visual_data_status: name_only` означает, что продукт или оттенок подтверждён, но надёжный числовой цвет для отображения недоступен. Аддон **не должен заявлять корректный по цвету Appearance**, пока не задан цвет с подтверждённым источником или явно обозначенная оценка.
- `manufacturer_color_code` и `manufacturer_palette_code` — необязательные идентификаторы, отличные от стабильного ID цвета Filamentra. Сохраняйте исходные ID для прослеживаемости.
- `catalog_status: listed_in_manufacturer_software` не подтверждает наличие в продаже сейчас. BambuStudio может содержать исторические варианты.

## Валидаторы

- [Схема линейки](../catalog/schema/line.schema.json)
- [Схема пресета](../catalog/schema/preset.schema.json)
- [Сценарий проверки](../tools/validate_catalog.py)
- [Спецификация внешнего вида материала](MATERIAL_APPEARANCE_SPEC.md)

Несовместимые изменения после первого релиза требуют новой версии схемы. Версии содержимого набора данных независимы и распространяются через [GitHub Releases](DISTRIBUTION.md).

## Права на содержимое и качество

Названия брендов производителей и фактические свойства продукции приводятся как справочные сведения и не означают одобрение. Не распространяйте фотографии, логотипы и текстуры шейдеров без прав на них. Опубликованные значения HEX предназначены для отображения; это **не калиброванные измерения отпечатков**. Filamentra создаёт визуальные Appearances, а не инженерные физические Materials.
