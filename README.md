# gkmas_inst_convert

## 概要

[公式が配布しているInst音源](https://gakuen-label.idolmaster-official.jp/news/dqtqf141g8ne)の命名規則があまりにも酷かったので、誤字修正＋ファイル名の正規化＋ALAC&FLACに変換するパッチ的なものを作りました。

## ファイル構成

- main.py `_INPUT`ディレクトリのファイル名の修正を行い、`_OUTPUT_ORIGINAL`に出力します。
- alac.py `main.py`で変換した`_OUTPUT_ORIGINAL`のデータをALACに変換し、`_OUTPUT_ALAC`に出力します。
- flac.py `main.py`で変換した`_OUTPUT_ORIGINAL`のデータをFLACに変換し、`_OUTPUT_FLAC`に出力します。

(※alac.pyとflac.pyはffmpegを使っているので事前にパスを通しといてください)

## 使い方

1. [公式が配布しているInst音源](https://gakuen-label.idolmaster-official.jp/news/dqtqf141g8ne)をGoogleDriveからダウンロード
2. `_INPUT/学園アイドルマスター_初星学園_～～`になるようにファイルを設置
3. `python main.py`でファイル名を変更（`_OUTPUT_ORIGINAL/月村手毬/Luna say maybe/Luna say maybe (Instrumental).wav`のように正規化されます）
4. お好みで`alac.py`や`flac.py`も実行

## 注意事項

- 非公式だからどうなっても知らんよ
- Copilotにほぼ全部書かせたから細かいことは知らん
- 自己責任で使ってください
- ファイル名正規化については楽曲が追加され次第多分更新します
