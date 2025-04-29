import os
import shutil
import sys
import argparse
import subprocess

# 定数
INPUT_FOLDER = "_INPUT"
TEMP_FOLDER = "temp"
OUTPUT_FOLDER = "_OUTPUT_ORIGINAL"

# ファイル名を正規化ルール
# 右端 => 元の名前
# 左端 => 変換する名前
RENAME_RULES = {
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
    "TRY IT Now": "Try it now",
    "Tryitnow": "Try it now"
}

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description='学園アイドルマスターのInst楽曲のファイル名を正規化します。')
parser.add_argument('--no-music-folder', action='store_true', help='曲ごとのフォルダを作成しない')
parser.add_argument('--no-artist-folder', action='store_true', help='アーティストごとのフォルダを作成しない')
parser.add_argument('--output-flac', action='store_true', help='FLAC形式でも出力する')
parser.add_argument('--output-alac', action='store_true', help='ALAC形式でも出力する')
parser.add_argument('--output-mp3', action='store_true', help='MP3形式でも出力する')
parser.add_argument('--output-m4a', action='store_true', help='M4A形式でも出力する')
args = parser.parse_args()

# 1. _INPUTフォルダに何も無いまたはフォルダがなければエラーで終了
if not os.path.exists(INPUT_FOLDER) or not os.listdir(INPUT_FOLDER):
    print(f"エラー: {INPUT_FOLDER} フォルダが存在しないか、空です。")
    sys.exit(1)
print(f"{INPUT_FOLDER} フォルダが存在し、処理を開始します。")

# 2. tempフォルダと出力フォルダがなかったら作成
output_folders = [TEMP_FOLDER, OUTPUT_FOLDER]
if args.output_flac:
    output_folders.append("_OUTPUT_FLAC")
if args.output_alac:
    output_folders.append("_OUTPUT_ALAC")
if args.output_mp3:
    output_folders.append("_OUTPUT_MP3")
if args.output_m4a:
    output_folders.append("_OUTPUT_M4A")
for folder in output_folders:
    os.makedirs(folder, exist_ok=True)
    print(f"{folder} フォルダを作成しました。")

# 3. tempフォルダと出力フォルダの中身をすべて削除
for folder in output_folders:
    print(f"{folder} フォルダの中身を削除します。")
    for item in os.listdir(folder):
        item_path = os.path.join(folder, item)
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

for root, dirs, files in os.walk(TEMP_FOLDER, topdown=False):
    for dir_name in dirs:
        for key, value in RENAME_RULES.items():
            if key in dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_name = dir_name.replace(key, value)
                new_dir_path = os.path.join(root, new_dir_name)
                os.rename(old_dir_path, new_dir_path)
                print(f"フォルダ名変更: {old_dir_path} -> {new_dir_path}")

    for file_name in files:
        base_name, ext = os.path.splitext(file_name)
        for key, value in RENAME_RULES.items():
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

# 11. FLAC形式でも出力する場合の処理
if args.output_flac:
    print("FLAC形式でも出力します。(1411kbps)")
    for root, dirs, files in os.walk("temp"):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.lower().endswith('.wav'):  # Add other formats if needed
                continue

            relative_path = os.path.relpath(root, "temp")
            artist_name = os.path.basename(os.path.dirname(root))
            song_name, _ = os.path.splitext(file)
            album_name = os.path.basename(root)  # Use the directory name as the album name
            album_artist = "初星学園"

            output_dir = os.path.join("_OUTPUT_FLAC", relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{song_name}.flac")
            command = [
                "ffmpeg", "-i", file_path, "-c:a", "flac", "-b:a", "1411k",
                "-metadata", f"artist={artist_name}", "-metadata", f"title={song_name}", 
                "-metadata", f"album={album_name}", "-metadata", f"album_artist={album_artist}", 
                output_file
            ]
            subprocess.run(command, check=True)

# 12. ALAC形式でも出力する場合の処理
if args.output_alac:
    print("ALAC形式でも出力します。(1411kbps)")
    for root, dirs, files in os.walk("temp"):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.lower().endswith('.wav'):  # Add other formats if needed
                continue

            relative_path = os.path.relpath(root, "temp")
            artist_name = os.path.basename(os.path.dirname(root))
            song_name, _ = os.path.splitext(file)
            album_name = os.path.basename(root)  # Use the directory name as the album name
            album_artist = "初星学園"

            output_dir = os.path.join("_OUTPUT_ALAC", relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{song_name}.m4a")
            command = [
                "ffmpeg", "-i", file_path, "-c:a", "alac", "-b:a", "1411k",
                "-metadata", f"artist={artist_name}", "-metadata", f"title={song_name}", 
                "-metadata", f"album={album_name}", "-metadata", f"album_artist={album_artist}", 
                output_file
            ]
            subprocess.run(command, check=True)

# 13. MP3形式でも出力する場合の処理
if args.output_mp3:
    print("MP3形式でも出力します。(320kbps)")
    for root, dirs, files in os.walk("temp"):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.lower().endswith('.wav'):  # Add other formats if needed
                continue

            relative_path = os.path.relpath(root, "temp")
            artist_name = os.path.basename(os.path.dirname(root))
            song_name, _ = os.path.splitext(file)
            album_name = os.path.basename(root)  # Use the directory name as the album name
            album_artist = "初星学園"

            output_dir = os.path.join("_OUTPUT_MP3", relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{song_name}.mp3")
            command = [
                "ffmpeg", "-i", file_path, "-c:a", "libmp3lame", "-b:a", "320k",
                "-metadata", f"artist={artist_name}", "-metadata", f"title={song_name}", 
                "-metadata", f"album={album_name}", "-metadata", f"album_artist={album_artist}", 
                output_file
            ]
            subprocess.run(command, check=True)

# 14. M4A形式でも出力する場合の処理
if args.output_m4a:
    print("M4A形式でも出力します。(320kbps)")
    for root, dirs, files in os.walk("temp"):
        for file in files:
            file_path = os.path.join(root, file)
            if not file.lower().endswith('.wav'):  # Add other formats if needed
                continue

            relative_path = os.path.relpath(root, "temp")
            artist_name = os.path.basename(os.path.dirname(root))
            song_name, _ = os.path.splitext(file)
            album_name = os.path.basename(root)  # Use the directory name as the album name
            album_artist = "初星学園"

            output_dir = os.path.join("_OUTPUT_M4A", relative_path)
            os.makedirs(output_dir, exist_ok=True)

            output_file = os.path.join(output_dir, f"{song_name}.m4a")
            command = [
                "ffmpeg", "-i", file_path, "-c:a", "aac", "-b:a", "320k",
                "-metadata", f"artist={artist_name}", "-metadata", f"title={song_name}", 
                "-metadata", f"album={album_name}", "-metadata", f"album_artist={album_artist}", 
                output_file
            ]
            subprocess.run(command, check=True)

# 15. 音楽ごとのフォルダを作成しない場合の処理
if(args.no_music_folder):
    print("曲ごとのフォルダを作成しない設定で処理します。")
    folders_to_process = [TEMP_FOLDER]
    
    # FLAC/ALAC/MP3/M4A出力が有効な場合、それらのフォルダも処理対象に追加
    if args.output_flac:
        folders_to_process.append("_OUTPUT_FLAC")
    if args.output_alac:
        folders_to_process.append("_OUTPUT_ALAC")
    if args.output_mp3:
        folders_to_process.append("_OUTPUT_MP3")
    if args.output_m4a:
        folders_to_process.append("_OUTPUT_M4A")
    
    for folder in folders_to_process:
        if not os.path.exists(folder):
            continue
            
        for root, dirs, files in os.walk(folder, topdown=False):
            for file in files:
                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in ['.wav', '.flac', '.m4a', '.mp3']:
                    file_path = os.path.join(root, file)
                    # ファイルが最下層（曲ごとのフォルダ）にある場合
                    parent_dir = os.path.dirname(root)
                    if parent_dir and parent_dir != folder:
                        # 1つ上の階層（アーティストフォルダ）に移動
                        new_file_path = os.path.join(parent_dir, file)
                        shutil.move(file_path, new_file_path)
                        print(f"ファイル移動: {file_path} -> {new_file_path}")
            
            # 空になったフォルダを削除
            if not os.listdir(root) and root != folder:
                os.rmdir(root)
                print(f"空フォルダ削除: {root}")

# 16. アーティストごとのフォルダを作成しない場合の処理
if(args.no_artist_folder):
    print("アーティストごとのフォルダを作成しない設定で処理します。")
    folders_to_process = [TEMP_FOLDER]
    
    # FLAC/ALAC/MP3/M4A出力が有効な場合、それらのフォルダも処理対象に追加
    if args.output_flac:
        folders_to_process.append("_OUTPUT_FLAC")
    if args.output_alac:
        folders_to_process.append("_OUTPUT_ALAC")
    if args.output_mp3:
        folders_to_process.append("_OUTPUT_MP3")
    if args.output_m4a:
        folders_to_process.append("_OUTPUT_M4A")
    
    for folder in folders_to_process:
        if not os.path.exists(folder):
            continue
            
        for root, dirs, files in os.walk(folder, topdown=False):
            # Skip the folder itself
            if root == folder:
                continue
            
            # Process only immediate subfolders of the target folder
            if os.path.dirname(root) == folder:
                for file in files:
                    file_path = os.path.join(root, file)
                    new_file_path = os.path.join(folder, file)
                    shutil.move(file_path, new_file_path)
                    print(f"ファイル移動: {file_path} -> {new_file_path}")
                
                # Move all subdirectories to the parent folder
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    new_dir_path = os.path.join(folder, dir_name)
                    shutil.move(dir_path, new_dir_path)
                    print(f"フォルダ移動: {dir_path} -> {new_dir_path}")
            
            # After moving all contents, check if folder is empty and remove it
            if not os.listdir(root) and root != folder:
                os.rmdir(root)
                print(f"空フォルダ削除: {root}")

# 17. tempフォルダを移動
for item in os.listdir(TEMP_FOLDER):
    src_path = os.path.join(TEMP_FOLDER, item)
    dest_path = os.path.join(OUTPUT_FOLDER, item)
    shutil.move(src_path, dest_path)
    print(f"移動: {src_path} -> {dest_path}")

print("\nファイル名正規化の処理が完了しました。")
