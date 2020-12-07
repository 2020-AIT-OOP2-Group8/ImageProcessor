# ファイル変更イベント検出のため、watchdogをインポート
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

# ファイルアクセスとスリープのため、osとtimeをインポート
import os
import time

# 画像処理
import cv2

# 監視対象ディレクトリを指定する
target_dir = 'static/upload_images'
# 監視対象ファイルのパターンマッチを指定する
target_file = '*.*'

# PatternMatchingEventHandler の継承クラスを作成
class FileChangeHandler(PatternMatchingEventHandler):

    # ファイル作成時のイベント
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print(filename)
        img_path = "static/upload_images/" + filename
        # 画像の読み込み
        img = cv2.imread(img_path)
        gray_output_images = "static/gray_output_images/gray_" + filename 
        #グレースケール化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB2〜 でなく BGR2〜 を指定
        #グレースケール画像の保存
        cv2.imwrite(gray_output_images, img_gray)

        thresh_output_images = "static/thresh_output_images/thresh_" + filename 
        th, img_thresh = cv2.threshold(img, 188, 255, cv2.THRESH_BINARY)
        # 二値化画像の保存
        cv2.imwrite(thresh_output_images, img_thresh)
        cv2.destroyAllWindows()

        edges_output_images = "static/edges_output_images/edges_" + filename 
        #Cannyフィルタによる輪郭抽出
        edges = cv2.Canny(img, 150, 200)
        #輪郭抽出画像の保存
        cv2.imwrite(edges_output_images, edges)

    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        print(filename)
        img_path = "static/upload_images/" + filename
        # 画像の読み込み
        img = cv2.imread(img_path)
        gray_output_images = "static/gray_output_images/gray_" + filename 
        #グレースケール化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB2〜 でなく BGR2〜 を指定
        #グレースケール画像の保存
        cv2.imwrite(gray_output_images, img_gray)

        thresh_output_images = "static/thresh/output_images/thresh_" + filename 
        th, img_thresh = cv2.threshold(img, 188, 255, cv2.THRESH_BINARY)
        # 二値化画像の保存
        cv2.imwrite(thresh_output_images, img_thresh)
        cv2.destroyAllWindows()

        edges_output_images = "static/edges_output_images/edges_" + filename 
        #Cannyフィルタによる輪郭抽出
        edges = cv2.Canny(img, 150, 200)
        #輪郭抽出画像の保存
        cv2.imwrite(edges_output_images, edges)

# コマンド実行の確認
if __name__ == "__main__":
    # ファイル監視の開始
    event_handler = FileChangeHandler([target_file])
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()