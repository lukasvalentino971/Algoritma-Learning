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
    // Membuat matriks bobot (hanya 1 kolom)
let weight_html = '<tr>'; // Mulai baris matriks bobot

for (let j = 0; j < row; j++) {
    // Menambahkan label di samping kiri indeks ke-0 pada matriks awal
    weight_html += `
        <td>
            A${j + 1}&nbsp; = 
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





