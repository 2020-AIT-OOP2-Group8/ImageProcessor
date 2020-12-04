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
        
        # START : Hiraiwa-branch
        imagePath = 'static/upload_images/'+filename # アップロードされた画像のパスを取得
        outputPath = 'static/output_images/face_' + filename # アウトプット先のパスを指定
        cascade_path = 'cascades/haarcascade_frontalface_default.xml' # 顔を検出してくれるxmlファイルの場所を指定
        
        get_img = cv2.imread(imagePath) # アップロードされた画像を取得

        cascade = cv2.CascadeClassifier(cascade_path) # 以下の二行で顔の場所を判別
        facerect = cascade.detectMultiScale(get_img, scaleFactor=1.1, minNeighbors=1, minSize=(100, 100))

        if len(facerect) > 0: # 写真の中に顔があった場合
            for rect in facerect:
                #矩形描画
                cv2.rectangle(get_img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(255,255,255),8)

        cv2.imwrite(outputPath, get_img) # 出力
        # END : Hiraiwa-branch

        # START : ito-souma-Branch
        print(filename)
        img_path = "upload_images/" + filename
        # 画像の読み込み
        img = cv2.imread(img_path)
        gray_outputPath = "output_images/gray_" + filename 
        #グレースケール化
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB2〜 でなく BGR2〜 を指定
        #グレースケール画像の保存
        cv2.imwrite(gray_outputPath, img_gray)

        thresh_outputPath = "output_images/thresh_" + filename 
        th, img_thresh = cv2.threshold(img, 188, 255, cv2.THRESH_BINARY)
        # 二値化画像の保存
        cv2.imwrite(thresh_outputPath, img_thresh)
        cv2.destroyAllWindows()

        edges_outputPath = "output_images/edges_" + filename 
        #Cannyフィルタによる輪郭抽出
        edges = cv2.Canny(img, 150, 200)
        #輪郭抽出画像の保存
        cv2.imwrite(edges_outputPath, edges)
        # END : ito-souma-Branch

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