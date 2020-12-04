# ファイルアクセスとスリープのため、osとtimeをインポート
import os
import time

# 画像処理
import cv2

# 監視対象ディレクトリを指定する
target_dir = os.path.abspath(os.path.dirname(__file__)) + '/static/upload_images/'
output_dir = os.path.abspath(os.path.dirname(__file__)) + '/static/output_images/'
# 監視対象ファイルのパターンマッチを指定する
target_file = '*.*'

def on_created(filename):
    print(filename)

# コマンド実行の確認
if __name__ == "__main__":
    # ファイル監視の開始
    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            oldFilenamesSet = set(os.listdir(target_dir))
            time.sleep(0.1)
            newFilenamesSet = set(os.listdir(target_dir))
            if len(newFilenamesSet) > len(oldFilenamesSet):
                newFiles = newFilenamesSet - oldFilenamesSet
                for f in newFiles:
                    on_created(f)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()