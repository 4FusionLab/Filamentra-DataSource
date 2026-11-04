# Неопределённые цвета PLA/PETG — полный аудит

Снимок исходных данных: **4 ноября 2026 года**. Это список **каждого** оставшегося цвета, у которого в каталоге нет ни `hex`, ни `rgba_swatches`, ни `measured_sample`. Новые товары не добавлялись. Наличие названия в каталоге само по себе **не доказывает** существования корректного цветового кода.

**До текущей партии:** 138 записей без цвета. **Заполнено:** 19 (только с точными ссылками на источники, со статусом `estimated`). **Остаётся:** 119.

## Разбивка по производителям

| Производитель | Без цвета | Причина |
| --- | ---: | --- |
| creality | 6 | Смешение оттенков PETG-CF, прозрачность, вспененный PLA |
| deeplee | 1 | Нет точной карточки цвета |
| elegoo | 59 | Особые Silk, CMYK, Glow, Translucent и базовые цвета без точной плашки |
| kingroon | 53 | Дополнительные оттенки PLA/PETG и отсутствие числовых данных |
| **Всего** | **119** | **Не заменять догадками** |

## Построчный реестр

Каждый источник ниже — существующая ссылка из JSON-файла каталога, **не подтверждение наличия измеренного HEX**. Объекты перечислены без пропусков.

### creality → PETG → CR-PETG (2)

Исходная карточка: [страница линейки](https://vip.creality.com/en/goods-detail/1786). JSON: [`creality/cr-petg`](../catalog/brands/creality/cr-petg.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `creality/cr-petg/yellow` | Yellow | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `creality/cr-petg/transparent-blue` | Transparent Blue | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |

### creality → PLA → Hyper PLA RFID Lightweight (2)

Исходная карточка: [страница линейки](https://store.creality.com/products/hyper-lightweight-pla-3d-printing-filament-1kg). JSON: [`creality/hyper-lightweight-pla-rfid`](../catalog/brands/creality/hyper-lightweight-pla-rfid.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `creality/hyper-lightweight-pla-rfid/white` | White | `foamed_sample_unverified` | Нужна реальная плашка вспененного материала |
| `creality/hyper-lightweight-pla-rfid/black` | Black | `foamed_sample_unverified` | Нужна реальная плашка вспененного материала |

### creality → PETG → Hyper PETG-CF RFID (2)

Исходная карточка: [страница линейки](https://store.creality.com/products/hyper-petg-cf-3d-printing-filament-1kg). JSON: [`creality/hyper-petg-cf-rfid`](../catalog/brands/creality/hyper-petg-cf-rfid.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `creality/hyper-petg-cf-rfid/night-gray-tea` | Night Gray Tea | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `creality/hyper-petg-cf-rfid/rocks-red-milk` | Rocks Red Milk | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### deeplee → PLA → PLA (1)

Исходная карточка: [страница линейки](https://deeplee3d.com/). JSON: [`deeplee/pla`](../catalog/brands/deeplee/pla.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `deeplee/pla/black` | Black | `identity_unconfirmed` | Нужна конкретная карточка производителя и точная цветовая плашка |

### elegoo → PLA → PLA Basic (6)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-basic-filament-1-75mm-colored-1kg). JSON: [`elegoo/pla-basic`](../catalog/brands/elegoo/pla-basic.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-basic/cream-yellow` | Cream Yellow | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-basic/dark-green` | Dark Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-basic/deep-grey` | Deep Grey | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-basic/light-cyan` | Light Cyan | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-basic/megenta` | Megenta | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-basic/olive-green` | Olive Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### elegoo → PLA → PLA-CF (1)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-cf-filament-1-75mm-black-1kg). JSON: [`elegoo/pla-cf`](../catalog/brands/elegoo/pla-cf.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-cf/carbon-fiber-purple` | Carbon Fiber Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### elegoo → PLA → PLA CMYK (4)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-cmyk). JSON: [`elegoo/pla-cmyk`](../catalog/brands/elegoo/pla-cmyk.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-cmyk/rilievo-yellow` | Rilievo Yellow | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-cmyk/rilievo-white` | Rilievo White | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-cmyk/rilievo-cyan` | Rilievo Cyan | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-cmyk/rilievo-magenta` | Rilievo Magenta | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |

### elegoo → PLA → PLA Glow (5)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-glow). JSON: [`elegoo/pla-glow`](../catalog/brands/elegoo/pla-glow.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-glow/glow-blue` | Glow Blue | `emission_underdetermined` | Нужны дневной цвет и отдельный параметр свечения |
| `elegoo/pla-glow/glow-green` | Glow Green | `emission_underdetermined` | Нужны дневной цвет и отдельный параметр свечения |
| `elegoo/pla-glow/glow-yellow` | Glow Yellow | `emission_underdetermined` | Нужны дневной цвет и отдельный параметр свечения |
| `elegoo/pla-glow/glow-orange` | Glow Orange | `emission_underdetermined` | Нужны дневной цвет и отдельный параметр свечения |
| `elegoo/pla-glow/glow-pink` | Glow Pink | `emission_underdetermined` | Нужны дневной цвет и отдельный параметр свечения |

### elegoo → PLA → PLA Pro (4)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-pro-filament-1-75mm-colored-1kg). JSON: [`elegoo/pla-pro`](../catalog/brands/elegoo/pla-pro.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-pro/beige` | Beige | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-pro/hot-pink` | Hot Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-pro/neon-green` | Neon Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-pro/true-red` | True Red | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### elegoo → PLA → PLA Silk (11)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/elegoo-silk-pla-filament-1-75mm-colored-1kg). JSON: [`elegoo/pla-silk`](../catalog/brands/elegoo/pla-silk.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-silk/silk-black-green` | Silk Black Green | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-black-purple` | Silk Black Purple | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-black-red` | Silk Black Red | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-blue-green` | Silk Blue Green | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-blue-green-orange` | Silk Blue Green Orange | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-blue-magenta` | Silk Blue Magenta | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-blue-purple` | Silk Blue Purple | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-blue-purple-black` | Silk Blue Purple Black | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-bluish-purple` | Silk Bluish Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla-silk/silk-green-red` | Silk Green Red | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |
| `elegoo/pla-silk/silk-yellow-purple` | Silk Yellow Purple | `multicolor_underdetermined` | Нужны несколько компонентов цвета и тип соэкструзии |

### elegoo → PLA → PLA Translucent (9)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-translucent). JSON: [`elegoo/pla-translucent`](../catalog/brands/elegoo/pla-translucent.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla-translucent/crytal-white` | Crytal White | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/light-grey` | Light Grey | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/red` | Red | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/yellow` | Yellow | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/light-blue` | Light Blue | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/green` | Green | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/pink` | Pink | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/light-purple` | Light Purple | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `elegoo/pla-translucent/rose-red` | Rose Red | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |

### elegoo → PLA → PLA (19)

Исходная карточка: [страница линейки](https://us.elegoo.com/products/pla-filament-1-75mm-colored-1kg). JSON: [`elegoo/pla`](../catalog/brands/elegoo/pla.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `elegoo/pla/bone-white` | Bone White | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/cherry-red` | Cherry Red | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/chestnut-black` | Chestnut Black | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/chocolate-brown` | Chocolate Brown | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/coffee-brown` | Coffee Brown | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/cold-white` | Cold White | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/dark-purple` | Dark Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/lavender-purple` | Lavender Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/mango-yellow` | Mango Yellow | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/midnight-black` | Midnight Black | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/oak-wood-color` | Oak Wood Color | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/ocean-blue` | Ocean Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/olive-green` | Olive Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/porcelain-white` | Porcelain White | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/pumpkin-orange` | Pumpkin Orange | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/sakura-pink` | Sakura Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/teal-green` | Teal Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/true-green` | True Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `elegoo/pla/true-red` | True Red | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### kingroon → PETG → PETG Basic (25)

Исходная карточка: [страница линейки](https://kingroon.com/products/kingroon-petg-basic). JSON: [`kingroon/petg-basic`](../catalog/brands/kingroon/petg-basic.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `kingroon/petg-basic/sky-blue` | Sky Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/pink` | Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/skin` | Skin | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/grass-green` | Grass Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/mint-green` | Mint Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/light-apricot` | Light Apricot | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/cyan` | Cyan | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/light-pink` | Light Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/dark-green` | Dark Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/purple` | Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/brown` | Brown | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/porcelain-blue` | Porcelain Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/peony-pink` | Peony Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/transparent-pink` | Transparent Pink | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `kingroon/petg-basic/ocean-blue` | Ocean Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/lemon-yellow` | Lemon Yellow | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/wood-color` | Wood Color | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/carrot-orange` | Carrot Orange | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/bamboo-green` | Bamboo Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/olive-green` | Olive Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/navy-blue` | Navy Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/beige` | Beige | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/khaki` | Khaki | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/metallic-copper` | Metallic Copper | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/petg-basic/metallic-silver` | Metallic Silver | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### kingroon → PLA → PLA Basic (13)

Исходная карточка: [страница линейки](https://kingroon.com/products/kingroon-pla-basic). JSON: [`kingroon/pla-basic`](../catalog/brands/kingroon/pla-basic.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `kingroon/pla-basic/cyan` | Cyan | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/light-apricot` | Light Apricot | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/light-pink` | Light Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/sakura-pink` | Sakura Pink | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/sea-blue` | Sea Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/vibrant-orange` | Vibrant Orange | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/apple-green` | Apple Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/mint-green` | Mint Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/turquoise-green` | Turquoise Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/lilac-purple` | Lilac Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/meteor-silver` | Meteor Silver | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/retro-red` | Retro Red | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-basic/wood` | Wood | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### kingroon → PLA → Matte PLA (3)

Исходная карточка: [страница линейки](https://kingroon.com/products/10kg-matte-pla-filament-1-75mm). JSON: [`kingroon/pla-matte`](../catalog/brands/kingroon/pla-matte.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `kingroon/pla-matte/brown` | Brown | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-matte/matte-rainbow` | Matte Rainbow | `gradient_underdetermined` | Нужны цвета переходов и длина градиента |
| `kingroon/pla-matte/skin` | Skin | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

### kingroon → PLA → PLA Plus (PLA+) (12)

Исходная карточка: [страница линейки](https://kingroon.com/products/kingroon-pla-pluspla). JSON: [`kingroon/pla-plus`](../catalog/brands/kingroon/pla-plus.json).

| ID цвета | Официальное название | Причина | Что нужно подтвердить |
| --- | --- | --- | --- |
| `kingroon/pla-plus/blue` | Blue | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/white` | White | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/black` | Black | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/grey` | Grey | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/red` | Red | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/yellow` | Yellow | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/orange` | Orange | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/green` | Green | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/purple` | Purple | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/skin` | Skin | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |
| `kingroon/pla-plus/transparent` | Transparent | `transmission_underdetermined` | Нужны оттенок конкретного SKU и оптические свойства |
| `kingroon/pla-plus/silver` | Silver | `numeric_swatch_not_found` | Точный магазинный образец или измерение для этого SKU |

## Стратегия закрытия

- **Обычный непрозрачный цвет:** точная карточка производителя, дистрибьютора, независимого магазина или запись с измерением; желательно связать SKU с вариантом. Если HEX взят из магазинной плашки, помечать `estimated` и сохранять прямой URL.
- **Silk соэкструзия / Rainbow:** искать `rgba_swatches` из нескольких компонентов и тип распределения; один HEX создаёт ложное представление.
- **Translucent / CMYK:** не подменять реальную прозрачность альфа-каналом плашки. Нужен отдельный профиль светопропускания, а оттенок — из проверяемого образца.
- **Glow:** дневной цвет и люминесценция — разные данные; отсутствие числового значения нельзя «восстановить» из имени.
- **Creality PETG-CF:** рекламные цветовые названия у продавцов расходятся с исходными; требуется сопоставление артикула до импорта.

## Повторяемый аудит

```bash
python tools/audit_missing_colors.py --format summary
python tools/audit_missing_colors.py --format markdown --out dist/unresolved.md
python tools/audit_missing_colors.py --format json --out dist/unresolved.json
```

Скрипт генерирует актуальный список **из JSON**: дальнейшие исправления автоматически уменьшат количество пропусков, а этот отчёт останется историческим снимком.

Важно: табличные причины — это классификация неопределённости по типу материала и источнику. Она **не означает**, что каждая страница дистрибьютора на рынке была проверена или что цвет невозможно восстановить в будущем.
