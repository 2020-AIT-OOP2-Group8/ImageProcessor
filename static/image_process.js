console.log('Fire. File.')
fetch(`/view_images`)
    .then(response => {
        console.log(response.status)
        return response.json().then(data => {
            // htmlから対象のtableを取得
            let table = document.getElementById("view_images");
            console.log(data)

            // Jsonで受け取ったlengthの回数を回す
            for (let index = 0; index < data['length']; index++) {
                // 画像のファイル名を取得
                imgFilename = data[index];
                // テーブルに当該行を追加
                let newRow = table.insertRow();

                // 以下画像表示
                // 元画像
                let newCell = newRow.insertCell();
                let newImage = document.createElement('img');
                newImage.src = './static/upload_images/' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
                // モザイク
                newCell = newRow.insertCell();
                newImage = document.createElement('img');
                newImage.src = './static/output_images/face_' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
                // 枠で囲う
                newCell = newRow.insertCell();
                newImage = document.createElement('img');
                newImage.src = './static/output_images/face2_' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
                // 輪郭抽出
                newCell = newRow.insertCell();
                newImage = document.createElement('img');
                newImage.src = './static/output_images/edges_' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
                // グレースケール
                newCell = newRow.insertCell();
                newImage = document.createElement('img');
                newImage.src = './static/output_images/gray_' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
                // 2値化
                newCell = newRow.insertCell();
                newImage = document.createElement('img');
                newImage.src = './static/output_images/thresh_' + imgFilename;
                newImage.style.width = '90%';
                newCell.appendChild(newImage);
            }
        });
    });