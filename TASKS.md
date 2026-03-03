# TASKS.md

## Inbox


## Next (max 3)
- [ ] 蜈ｱ騾唏TTP繝｡繧ｽ繝・ラ縺ｮ萓句､匁婿驥昴ｒ謨ｴ逅・  - Done: `request_json_get/post` 縺ｮ `retry_on_timeout` 繧貞他縺ｳ蜃ｺ縺怜・隕∽ｻｶ縺ｫ蜷医ｏ縺帙※驕狗畑繝ｫ繝ｼ繝ｫ蛹悶〒縺阪※縺・ｋ
  - Entry: `bot.py`
  - Scope: `bot.py`, `POLICY.md` or decision log


## Doing (max 1)


## Waiting
- [ ] ...

## Done
- [x] 蜈ｨcog縺ｮ request 螟夂畑邂・園繧・bot.py 蜈ｱ騾壹Γ繧ｽ繝・ラ縺ｸ邨ｱ荳
  - Done: `cogs` 蜀・・ `requests.get/post` 逶ｴ蜻ｼ縺ｳ蜃ｺ縺励ｒ髯､蜴ｻ縺励～self.bot.request_json_get/post` 縺ｫ鄂ｮ謠・  - Entry: `bot.py`
  - Scope: `bot.py`, `cogs/bazzer_commands.py`, `cogs/networth.py`, `cogs/ranking.py`, `cogs/role_check.py`
  - Commit: not committed
  - Notes:
    - ReadTimeout譎ゅΜ繝医Λ繧､縺ｮ譌｢蟄俶嫌蜍輔ｒ `bot.py` 蛛ｴ繝｡繧ｽ繝・ラ縺ｫ髮・ｴ・    - `ranking.py` 縺ｫ譌｢蟄倥・ `"\_"` 縺ｫ髢｢縺吶ｋ `SyntaxWarning` 縺後≠繧具ｼ井ｻ雁屓繧ｹ繧ｳ繝ｼ繝怜､悶・縺溘ａ譛ｪ菫ｮ豁｣・・
- [x] ranking コマンドの安全分割（Option 1 / 第1段）
  - Done: `cogs/ranking_helpers.py` を新設し、`ranking.py` から共通計算を外出し
  - Entry: `cogs/ranking.py`
  - Scope: `cogs/ranking.py`, `cogs/ranking_helpers.py`
  - Commit: not committed
  - Notes:
    - `build_catacombs_level_table` / `format_bmk` / `count_golden_dragons` / `escape_rank_name` を分離
    - `ranking.py` の壊れた文字列リテラルを修正し、`py_compile` 通過まで復旧
