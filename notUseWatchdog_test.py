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

def Hiraiwa_branch(filename):
    imagePath = target_dir + filename # アップロードされた画像のパスを取得
    outputPath = output_dir + 'face_' + filename # アウトプット先のパスを指定
    cascade_path = 'cascades/haarcascade_frontalface_default.xml' # 顔を検出してくれるxmlファイルの場所を指定
    
    get_img = cv2.imread(imagePath) # アップロードされた画像を取得

    cascade = cv2.CascadeClassifier(cascade_path) # 以下の二行で顔の場所を判別
    facerect = cascade.detectMultiScale(get_img, scaleFactor=1.1, minNeighbors=1, minSize=(100, 100))

    if len(facerect) > 0: # 写真の中に顔があった場合
        for rect in facerect:
            #矩形描画
            cv2.rectangle(get_img, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]),(255,255,255),8)

    cv2.imwrite(outputPath, get_img) # 出力

def ito_souma_Branch(filename):
    # 画像の読み込み
    imagePath = target_dir + filename
    img = cv2.imread(imagePath)
    gray_outputPath = output_dir + "gray_" + filename 
    #グレースケール化
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB2〜 でなく BGR2〜 を指定
    #グレースケール画像の保存
    cv2.imwrite(gray_outputPath, img_gray)

    thresh_outputPath = output_dir + "thresh_" + filename 
    th, img_thresh = cv2.threshold(img, 188, 255, cv2.THRESH_BINARY)
    # 二値化画像の保存
    cv2.imwrite(thresh_outputPath, img_thresh)
    cv2.destroyAllWindows()

    edges_outputPath = output_dir + "edges_" + filename 
    #Cannyフィルタによる輪郭抽出
    edges = cv2.Canny(img, 150, 200)
    #輪郭抽出画像の保存
    cv2.imwrite(edges_outputPath, edges)

def on_created(filename):
    print(filename)
    Hiraiwa_branch(filename)
    ito_souma_Branch(filename)

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