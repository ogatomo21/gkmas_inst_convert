import os
import shutil
import sys

# 定数
INPUT_FOLDER = "_INPUT"
TEMP_FOLDER = "temp"
OUTPUT_FOLDER = "_OUTPUT_ORIGINAL"

# 1. _INPUTフォルダに何も無いまたはフォルダがなければエラーで終了
if not os.path.exists(INPUT_FOLDER) or not os.listdir(INPUT_FOLDER):
    print(f"エラー: {INPUT_FOLDER} フォルダが存在しないか、空です。")
    sys.exit(1)
print(f"{INPUT_FOLDER} フォルダが存在し、処理を開始します。")

# 2. tempフォルダがなかったら作成
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)
    print(f"{TEMP_FOLDER} フォルダを作成しました。")
else:
    print(f"{TEMP_FOLDER} フォルダが既に存在します。")

# 3. tempフォルダの中身をすべて削除
print(f"{TEMP_FOLDER} フォルダの中身を削除します。")
for item in os.listdir(TEMP_FOLDER):
    item_path = os.path.join(TEMP_FOLDER, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
        print(f"ファイル削除: {item_path}")
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)
        print(f"フォルダ削除: {item_path}")

# 4. _INPUTフォルダの中身をtempにコピー
print(f"{INPUT_FOLDER} フォルダの中身を {TEMP_FOLDER} にコピーします。")
for item in os.listdir(INPUT_FOLDER):
    src_path = os.path.join(INPUT_FOLDER, item)
    dest_path = os.path.join(TEMP_FOLDER, item)
    if os.path.isfile(src_path):
        shutil.copy2(src_path, dest_path)
        print(f"ファイルコピー: {src_path} -> {dest_path}")
    elif os.path.isdir(src_path):
        shutil.copytree(src_path, dest_path)
        print(f"フォルダコピー: {src_path} -> {dest_path}")

# 5. temp内のサブフォルダでにある拡張子がwavであるもの以外をすべて削除
print(f"{TEMP_FOLDER} 内の .wav 以外のファイルを削除します。")
for root, dirs, files in os.walk(TEMP_FOLDER):
    for file in files:
        if not file.lower().endswith(".wav"):
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"削除: {file_path}")

# 6. フォルダ名を変更
print(f"{TEMP_FOLDER} 内のフォルダ名とファイル名を変更します。")
for root, dirs, files in os.walk(TEMP_FOLDER, topdown=False):
    for dir_name in dirs:
        if dir_name.startswith("学園アイドルマスター_初星学園_"):
            old_dir_path = os.path.join(root, dir_name)
            new_dir_name = dir_name.replace("学園アイドルマスター_初星学園_", "", 1)
            new_dir_path = os.path.join(root, new_dir_name)
            os.rename(old_dir_path, new_dir_path)
            print(f"フォルダ名変更: {old_dir_path} -> {new_dir_path}")

    for file_name in files:
        if file_name.startswith("学園アイドルマスター_初星学園_"):
            old_file_path = os.path.join(root, file_name)
            new_file_name = file_name.replace("学園アイドルマスター_初星学園_", "", 1)
            new_file_path = os.path.join(root, new_file_name)
            os.rename(old_file_path, new_file_path)
            print(f"ファイル名変更: {old_file_path} -> {new_file_path}")

# 7. 変換ルールに従ってフォルダの名前を変更
print("変換ルールに従ってフォルダ名とファイル名を変更します。")
rename_rules = {
    "White_Night_White_Wish": "White Night! White Wish!",
    "BOOMBOOMPOW": "Boom Boom Pow",
    "FragileHeart": "Fragile Heart",
    "COSMETIC": "Cosmetic",
    "YellowBigBang": "Yellow Big Bang!",
    "KiraKira": "Kira Kira",
    "MarbleHeart": "marble heart",
    "Marble_Heart": "marble heart",
    "FeelLewlDream": "Feel Jewel Dream",
    "Ride_On_Beat": "Ride on beat",
    "叶えたいことばかり": "叶えたい、ことばかり",
    "CampusMode!!": "Campus Mode!!",
    "Sweet magic": "Sweet Magic",
    "初(はじめ)": "初",
    "WAKEUP!!": "Wake up!!",
    "Luna say maybe_logo": "Luna say maybe",
    "TopSecret": "Top Secret",
    "Top secret": "Top Secret",
    "Endress Dance": "ENDLESS DANCE",
    "SWEET_MAGIC": "Sweet Magic",
}

for root, dirs, files in os.walk(TEMP_FOLDER, topdown=False):
    for dir_name in dirs:
        for key, value in rename_rules.items():
            if key in dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_name = dir_name.replace(key, value)
                new_dir_path = os.path.join(root, new_dir_name)
                os.rename(old_dir_path, new_dir_path)
                print(f"フォルダ名変更: {old_dir_path} -> {new_dir_path}")

    for file_name in files:
        base_name, ext = os.path.splitext(file_name)
        for key, value in rename_rules.items():
            if key in base_name:
                old_file_path = os.path.join(root, file_name)
                new_file_name = base_name.replace(key, value) + ext
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"ファイル名変更: {old_file_path} -> {new_file_path}")

# 8. ファイル名をInstだとわかるように変更
print("ファイル名に '(Instrumental)' を追加します。")
for root, dirs, files in os.walk(TEMP_FOLDER):
    for file_name in files:
        if file_name.lower().endswith(".wav"):
            old_file_path = os.path.join(root, file_name)
            base_name, ext = os.path.splitext(file_name)
            if not base_name.endswith(" (Instrumental)"):
                new_file_name = f"{base_name} (Instrumental){ext}"
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"ファイル名変更: {old_file_path} -> {new_file_path}")


# 9.全体曲は初星学園フォルダへ
print("全体曲を初星学園フォルダへ移動します。")
hatsuboshi_folder = os.path.join(TEMP_FOLDER, "初星学園")
if not os.path.exists(hatsuboshi_folder):
    os.makedirs(hatsuboshi_folder)
    print(f"フォルダ作成: {hatsuboshi_folder}")

for item in os.listdir(TEMP_FOLDER):
    item_path = os.path.join(TEMP_FOLDER, item)
    if os.path.isdir(item_path) and "_" not in item and item != "初星学園":
        shutil.move(item_path, os.path.join(hatsuboshi_folder, item))
        print(f"移動: {item_path} -> {hatsuboshi_folder}")

# 10. ソロ曲も分ける
print("ソロ曲を分け、ファイル名から歌手名を削除します。")
for root, dirs, files in os.walk(TEMP_FOLDER, topdown=False):
    if root == hatsuboshi_folder:
        continue  # 初星学園フォルダは除外

    for dir_name in dirs:
        if "_" in dir_name:
            old_dir_path = os.path.join(root, dir_name)
            parts = dir_name.split("_", 1)
            new_parent_dir = os.path.join(root, parts[0])
            new_dir_path = os.path.join(new_parent_dir, parts[1])

            if not os.path.exists(new_parent_dir):
                os.makedirs(new_parent_dir)
                print(f"フォルダ作成: {new_parent_dir}")

            os.rename(old_dir_path, new_dir_path)
            print(f"フォルダ名変更: {old_dir_path} -> {new_dir_path}")

    for file_name in files:
        if "_" in file_name:
            old_file_path = os.path.join(root, file_name)
            parts = file_name.split("_", 1)
            new_file_name = parts[1]
            new_file_path = os.path.join(root, new_file_name)

            os.rename(old_file_path, new_file_path)
            print(f"ファイル名変更: {old_file_path} -> {new_file_path}")

# 11. tempフォルダを移動
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    print(f"フォルダ作成: {OUTPUT_FOLDER}")
# OUTPUTフォルダの中身をすべて削除
print(f"{OUTPUT_FOLDER} フォルダの中身を削除します。")
for item in os.listdir(OUTPUT_FOLDER):
    item_path = os.path.join(OUTPUT_FOLDER, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
        print(f"ファイル削除: {item_path}")
    elif os.path.isdir(item_path):
        shutil.rmtree(item_path)
        print(f"フォルダ削除: {item_path}")
for item in os.listdir(TEMP_FOLDER):
    src_path = os.path.join(TEMP_FOLDER, item)
    dest_path = os.path.join(OUTPUT_FOLDER, item)
    shutil.move(src_path, dest_path)
    print(f"移動: {src_path} -> {dest_path}")

print("\nファイル名正規化の処理が完了しました。")
