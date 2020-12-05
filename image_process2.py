# ファイル変更イベント検出のため、watchdogをインポート
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

# ファイルアクセスとスリープのため、osとtimeをインポート
import os
import time

# 画像処理
import cv2

# 監視対象ディレクトリを指定する
target_dir = 'static/upload_images'

def makeImage(filename):

    imagePath = 'static/upload_images/'+filename # アップロードされた画像のパスを取得
    outputPath_face = 'static/face_output_images/face_' + filename # 顔を四角で囲む画像のアウトプット先のパスを指定
    outputPath_mosaic = 'static/mosaic_output_images/mosaic_' + filename # 顔をモザイクで隠す画像のアウトプット先のパスを指定
    cascade_path = 'cascades/haarcascade_frontalface_alt2.xml' # 画像処理に必要なxmlファイルの場所を指定
    print(imagePath)
    get_img = cv2.imread(imagePath) # アップロードされた画像を取得
    gray_img = cv2.imread(imagePath, 0) # get_imgをグレースケール化で保存

    rect_img = get_img.copy() # rect_imgにオリジナル画像をコピー
    mosaic_img = get_img.copy() # mosaic_imgにオリジナル画像をコピー

    cascade = cv2.CascadeClassifier(cascade_path)
    faces = cascade.detectMultiScale(gray_img)

    if len(faces) > 0: # 写真の中に顔があった場合
        for face in faces:
            x, y, w, h = face

            # 検出した顔の範囲を四角で囲む
            rect_img = cv2.rectangle(rect_img, (x, y), (x+w, y+h), color=(255, 255, 255), thickness=5)
            cv2.imwrite(outputPath_face, rect_img)

            # 検出した顔の範囲をモザイクする
            roi = mosaic_img[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w//10, h//10))
            roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
            mosaic_img[y:y+h, x:x+w] = roi 
    else:
        cv2.imwrite(outputPath_face, get_img)

    print(f'Correct: face_{filename}')
    
    cv2.imwrite(outputPath_mosaic, mosaic_img) # 出力
    print(f'Correct: mosaic_{filename}')

# PatternMatchingEventHandler の継承クラスを作成
class FileChangeHandler(FileSystemEventHandler):

    def on_created(self, event):
        print(f'on_created:')
        filepath = event.src_path
        filename = os.path.basename(filepath)
        makeImage(filename)

    # ファイル変更時のイベント
    def on_modified(self, event):
        print(f'on_modified:')
        filepath = event.src_path
        filename = os.path.basename(filepath)
        makeImage(filename)

# コマンド実行の確認
if __name__ == "__main__":
    # ファイル監視の開始
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, target_dir, recursive=True)
    observer.start()
    # 処理が終了しないようスリープを挟んで無限ループ
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() 