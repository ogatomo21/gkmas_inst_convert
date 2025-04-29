# gkmas_inst_convert

## 概要

[公式が配布しているInst音源](https://gakuen-label.idolmaster-official.jp/news/dqtqf141g8ne)の命名規則があまりにも酷かったので、誤字修正＋ファイル名の正規化＋ALAC&FLACに変換するパッチ的なものを作りました。

## 使い方

1. [公式が配布しているInst音源](https://gakuen-label.idolmaster-official.jp/news/dqtqf141g8ne)をGoogleDriveからダウンロード
2. `_INPUT/学園アイドルマスター_初星学園_～～`になるようにファイルを設置
3. `python main.py`でファイル名を変更（`_OUTPUT_ORIGINAL/月村手毬/Luna say maybe (Instrumental).wav`のように正規化されます）
4. お好みでオプションも付ける(後述)

## オプション

```
C:\ogatomo21\gkmas_inst_convert> python main.py --help
usage: main.py [-h] [--no-music-folder] [--no-artist-folder] [--output-flac] [--output-alac] [--output-mp3] [--output-m4a]

学園アイドルマスターのInst楽曲のファイル名を正規化します。

options:
  -h, --help          show this help message and exit
  --no-music-folder   曲ごとのフォルダを作成しない
  --no-artist-folder  アーティストごとのフォルダを作成しない
  --output-flac       FLAC形式でも出力する
  --output-alac       ALAC形式でも出力する
  --output-mp3        MP3形式でも出力する
  --output-m4a        M4A形式でも出力する
```

- `--no-music-folder` 楽曲ごとのフォルダを生成しない（例: `_OUTPUT_ORIGINAL/月村手毬/Luna say maybe (Instrumental).wav`）
- `--no-artist-folder` アーティストごとのフォルダーを生成しない（例: `_OUTPUT_ORIGINAL/Luna say maybe/Luna say maybe (Instrumental).wav`）
- `--output-flac` FLAC形式でも出力する(1411kbpsで`_OUTPUT_FLAC`フォルダに出力します。ffmpeg必須です。)
- `--output-alac` ALAC形式でも出力する(1411kbpsで`_OUTPUT_ALAC`フォルダに出力します。ffmpeg必須です。)
- `--output-mp3` MP3形式でも出力する(320kbpsで`_OUTPUT_MP3`フォルダに出力します。ffmpeg必須です。)
- `--output-m4a` M4A形式でも出力する(320kbpsで`_OUTPUT_M4A`フォルダに出力します。ffmpeg必須です。)

(※1 `--no-music-folder` と `--no-artist-folder` を同時に指定した場合、`_OUTPUT_ORIGINAL/Luna say maybe (Instrumental).wav` のようなフォルダ構造になります。)
(※2 `--output-(flac|alac|mp3|m4a)` を実行した場合でも、`_OUTPUT_ORIGINAL` フォルダに元のwavファイルは出力されます。)

## ファイル正規化に対応している楽曲

現在、2025年4月発表楽曲までに対応しています。その他の楽曲も発表され次第随時更新する予定です。

`main.py` 15行目の `RENAME_RULES` という定数を弄ることでご自身でも追加していただけます。

## 注意事項

- 非公式だからどうなっても知らんよ
- Copilotにほぼ全部書かせたから細かいことは知らん
- 自己責任で使ってください
- ファイル名正規化については楽曲が追加され次第多分更新します
