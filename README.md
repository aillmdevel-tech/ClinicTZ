# CLINIC 13 — ТЗ, концепт и референсы

Кооп-хоррор на 1–4 игрока. Вы — ночные врачи клиники №13 в 1998 году: принимаете пациентов, лечите настоящих и вычисляете двойников. Стек: Unity 6.3 + URP, FishNet, Steam.

Статус: **только документация и концепт, разработка не начата** (2026-11-21).

## С чего начать
1. [`docs/GAME_SPEC.md`](docs/GAME_SPEC.md) — единое ТЗ v3, главный документ.
2. [`docs/PROJECT_STATE.md`](docs/PROJECT_STATE.md) — текущее состояние, решения, следующий шаг.
3. [`docs/plans/2026-11-21-mvp-coop-steam.md`](docs/plans/2026-11-21-mvp-coop-steam.md) — план по этапам 0–8, ред. 3 (≈11–14 недель).
4. [`docs/USER_BRIEFS.md`](docs/USER_BRIEFS.md) — все запросы Alex по порядку; исходные ТЗ — в [`docs/original/`](docs/original/).

## Документы
| Файл | Что внутри |
|---|---|
| `docs/concept/MVP_CONCEPT.md` | состав MVP, игроки, больница, аномалии, история, раскадровка трейлера |
| `docs/art/CHARACTERS.md` + `docs/art/concept/` | персонажи, лайнап-блокаут, нормы по моделям |
| `docs/trailer/` | разбор 22 трейлеров, чек-лист съёмки |
| `reference/ANIMAL_HOSPITAL_ANALYSIS.md` | Animal Hospital (Roblox) — главный референс по механикам |
| `reference/SHIFT_AT_MIDNIGHT_ANALYSIS.md` | Shift At Midnight — главный референс по стилю |
| `CLINIC_13_AUDIT.md`, `CLINIC_13_GDD_v2_1_PROPOSED.md` | аудит исходного ТЗ и GDD v2.1 |
| `references/boards/` | доски кадров 01–06 |
| `references/trailers/analysis/` | контакт-листы, склейки, громкость |
| `clinic13_probe/` | стилевой зонд палаты (Blender, v1–v3) |
| `tools/` | скрипты Blender для рендера концептов |
| `.claude/memory-bank/` | память проекта для нового чата |

## Игры-референсы
| Игра | Роль | Ссылка |
|---|---|---|
| Animal Hospital (Roblox) | главный по механикам | [Roblox](https://www.roblox.com/games/78515283254292/Animal-Hospital) · [Wiki](https://animal-hospital.fandom.com/wiki/Animal_Hospital_Wiki) |
| Shift At Midnight | главный по стилю, филингу и трейлеру | [Steam](https://store.steampowered.com/app/3722330/Shift_At_Midnight/) |
| Lethal Company | кооп, форма, модели | [Steam](https://store.steampowered.com/app/1966720/Lethal_Company/) |
| No, I'm not a Human | ТВ-новости, странные лица | [Steam](https://store.steampowered.com/app/3180070/No_Im_not_a_Human/) |
| Who's at the door? | ТВ-новости с багами, осмотр | [Steam](https://store.steampowered.com/app/3690010/Whos_at_the_door/) |
| КЛЕТЬ | СНГ-сеттинг, кооп, локации | [Steam](https://store.steampowered.com/app/1699480/) |
| CRACK | темп трейлера | [Steam](https://store.steampowered.com/app/4312190/CRACK/) |

**Источники по Animal Hospital:**
- [TheSpike — аномалии](https://www.thespike.gg/roblox/animal-hospital/all-anomalies);
- [TheSpike — враги](https://www.thespike.gg/roblox/animal-hospital/all-enemies);
- [BloxGuides](https://bloxguidesgg.com/games/animal-hospital);
- [animal-hospital.me](https://animal-hospital.me/);
- [BlueStacks](https://www.bluestacks.com/blog/game-guides/roblox/rl-animal-hospital-anomaly-guide-en.html);
- [GameRant](https://gamerant.com/roblox-animal-hospital-patient-anomalies/);
- [FandomWire](https://fandomwire.com/all-characters-in-animal-hospital-explained/).

## Чего здесь нет
Видео трейлеров (`references/trailers/videos/`, 528 МБ) не загружены: это чужие ролики, они нужны только для локального анализа. Список и ссылки — в `references/trailers/list.tsv` и `app_*.json`. Скачать заново можно через `references/trailers/dl.sh`.

Скриншоты чужих игр на досках используются только как референс. Из чужих игр не копируем ни модели, ни текстуры, ни код, ни UI.
