import os
import shutil
import subprocess

def check_and_copy_output_original():
    if not os.path.exists("_OUTPUT_ORIGINAL"):
        print("No _OUTPUT_ORIGINAL folder found.")
        return False

    if os.path.exists("temp"):
        shutil.rmtree("temp")
    shutil.copytree("_OUTPUT_ORIGINAL", "temp")
    return True

def convert_to_alac():
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
                "ffmpeg", "-i", file_path, "-c:a", "alac", "-metadata", f"artist={artist_name}",
                "-metadata", f"title={song_name}", "-metadata", f"album={album_name}",
                "-metadata", f"album_artist={album_artist}", output_file
            ]
            subprocess.run(command, check=True)

            os.remove(file_path)  # Remove the original file after conversion

def delete_temp():
    shutil.rmtree("temp")

def main():
    if not check_and_copy_output_original():
        return
    convert_to_alac()
    delete_temp()
    print("Conversion completed successfully.")

if __name__ == "__main__":
    main()
