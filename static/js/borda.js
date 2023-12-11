function change_matrix_shape() {
    var row = parseInt($('#row').val());
    
    $('#initial-matrix').empty();
    $('#weight-matrix').empty();

    // Membuat baris dengan label "Ke-1" sampai "Ke-n" di atas kolom pertama pada matriks awal
    let labelRow = '<tr>';
    for (let i = -1; i < row; i++) {
        if (i == -1) {
            labelRow += `
                <td></td>
            `;
        } else {
            labelRow += `
                <td>Ke-${i + 1}</td>
            `;
        }
    }
    labelRow += '</tr>';
    $('#initial-matrix').append(labelRow);

    // Membuat baris dengan label "Ke-1" sampai "Ke-n" di atas kolom pertama pada matriks awal
    let placeholderRow = '<tr>';
    for (let i = 0; i < row; i++) {
        placeholderRow += `
            <td class="placeholder"></td>
        `;
    }
    placeholderRow += '</tr>';
    $('#initial-matrix').append(placeholderRow);

    // Membuat matriks awal berdasarkan nilai baris yang dimasukkan
    for (let i = 0; i < row; i++) {
        let temp_html = '<tr>';

        // Menambahkan label di samping kiri indeks ke-0 pada matriks awal
        temp_html += `<td>A${i + 1}&nbsp;&nbsp; = &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>`;

        for (let j = 0; j < row; j++) {
            temp_html += `
                <td>
                    <input type="number" id="x${i}${j}" min=0.01>
                </td>
            `;
        }
        temp_html += '</tr>';
        $('#initial-matrix').append(temp_html);
    }

    // Membuat matriks bobot (hanya 1 kolom)
let weight_html = '<tr>'; // Mulai baris matriks bobot

for (let j = 0; j < row; j++) {
    // Menambahkan label di samping kiri indeks ke-0 pada matriks awal
    weight_html += `
        <td>
            Ke-${j + 1}&nbsp; = 
        </td>
    `;

    weight_html += `
        <td>
            <input type="number" id="w${j}" min=0.1>
        </td>
    `;
}

weight_html += '</tr>'; // Selesai baris matriks bobot

$('#weight-matrix').append(weight_html); // Menambahkan HTML ke weight-matrix

}
function calculate() {
        let row = parseInt($('#row').val());
        let data = {
            initialMatrix: [],
            weightMatrix: []
        };
    
        // Mengumpulkan data dari matriks awal
        for (let i = 0; i < row; i++) {
            let rowValues = [];
            for (let j = 0; j < row; j++) {
                let value = parseFloat($(`#x${i}${j}`).val());
                rowValues.push(value);
            }
            data.initialMatrix.push(rowValues);
        }
    
        // Mengumpulkan data dari matriks bobot
        for (let j = 0; j < row; j++) {
            let value = parseFloat($(`#w${j}`).val());
            data.weightMatrix.push(value);
        }
    
        // Kirim data ke server menggunakan Ajax
        $.ajax({
            type: "POST",
            url: "/post_borda",
            contentType: "application/json",
            data: JSON.stringify(data),
            success: function(response) {
                console.log("Data telah dikirim ke server:", response);
                // Handle response jika diperlukan
        
                let resultMatrix = response.result;
        
                let bordaTable = $('.borda-matrix');
                bordaTable.find('tr:gt(0)').remove();
        
                // Menentukan nilai Skor untuk perbandingan
                let skorArray = resultMatrix.map(row => row.reduce((acc, val) => acc + val, 0));
                
                // Mengurutkan indeks dengan nilai Skor tertinggi menjadi urutan pertama
                let sortedIndexes = skorArray.map((_, index) => index)
                    .sort((a, b) => skorArray[b] - skorArray[a]);
        
                for (let i = 0; i < resultMatrix.length; i++) {
                    let kriteria = "A" + (sortedIndexes[i] + 1); // Menghasilkan nama kriteria sesuai dengan indeks yang telah diurutkan
                    let skor = skorArray[sortedIndexes[i]]; // Mendapatkan nilai Skor dari indeks yang telah diurutkan
        
                    // Menentukan nilai Rank berdasarkan perbandingan nilai Skor tertinggi
                    let rank = i + 1;
        
                    bordaTable.append(
                        '<tr>' +
                        '<td>' + kriteria + '</td>' +
                        '<td>' + skor + '</td>' +
                        '<td>' + rank + '</td>' +
                        '</tr>'
                    );
                }
        
                // Menampilkan bagian hasil perhitungan
                $('.electre-result-title').show();
                $('.electre-result').show();
            },
            error: function(err) {
                console.error("Error:", err);
                // Handle error jika diperlukan
            }
        });
        
}




