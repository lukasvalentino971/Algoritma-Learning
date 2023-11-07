function change_matrix_shape() {
    var row = $('#row').val()
    var column = $('#column').val()

    $('#initial-matrix').empty();
    $('#weight-matrix').empty();

    for (let i = 0; i < row; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < column; j++) {
            temp_html += `
            <td>
                <input type="number" id="x${ i }${ j }" value=0 min=0>
            </td>
            `
        }
        temp_html += `</tr>`
        $('#initial-matrix').append(temp_html);
    }

    for (let j = 0; j < column; j++) {
        let temp_html = `
        <td>
            <input type="number" id="w${ j }" value=0 min=0>
        </td>
        `

        $('#weight-matrix').append(temp_html)
    }
}

function calculate_matrix() {
    var row = $('#row').val()
    var column = $('#column').val()

    var matrix = []
    var weight = []

    for (var i = 0; i < row; i++) {
        matrix[i] = []
        for (var j = 0; j < column; j++) {
            matrix[i][j] = parseFloat($(`#x${i}${j}`).val())
        }
    }

    for (var j = 0; j < column; j++) {
        weight[j] = parseFloat($(`#w${j}`).val())
    }

    let form_data = new FormData()
    form_data.append('matrix', JSON.stringify(matrix))
    form_data.append('weight', JSON.stringify(weight))

    $.ajax({
        type: 'POST',
        url: '/post_electre_four',
        data: form_data,
        contentType: false,
        processData: false,
        success: function (response) {
            console.log(response)
        }
    })
}