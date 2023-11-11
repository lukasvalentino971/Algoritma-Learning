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
                <input type="number" id="x${ i }${ j }" min=0.01>
            </td>
            `
        }
        temp_html += `</tr>`
        $('#initial-matrix').append(temp_html);
    }

    for (let j = 0; j < column; j++) {
        let temp_html = `
        <td>
            <input type="number" id="w${ j }" min=0.01>
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
            value = $(`#x${i}${j}`).val()

            if (!value){
                alert("Matrix Can't Be Empty")
                return
            }

            matrix[i][j] = parseFloat(value)
        }
    }

    for (var j = 0; j < column; j++) {
        value = $(`#w${j}`).val()

        if (!value){
            alert("Weight Can't Be Empty")
            return
        }

        weight[j] = parseFloat(value)
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
            result = response.result
            change_result(result)
        },
        error: function (xhr, status, error) {
            // console.log(error)
            alert('Enter a New Matrix or Weight!!!\nInvalid Matrix or Weight!!!')
        }
    })
}

function change_result(result) {
    $('#r-matrix').empty();

    for (let i = 0; i < result.normalized_matrix.length; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < result.normalized_matrix[0].length; j++) {
            temp_html += `
            <td>
                ${result.normalized_matrix[i][j]}
            </td>
            `
        }
        temp_html += `</tr>`
        $('#r-matrix').append(temp_html);
    }

    $('#v-matrix').empty();

    for (let i = 0; i < result.weighted_matrix.length; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < result.weighted_matrix[0].length; j++) {
            temp_html += `
            <td>
                ${result.weighted_matrix[i][j]}
            </td>
            `
        }
        temp_html += `</tr>`
        $('#v-matrix').append(temp_html);
    }

    $('#c-set').empty();

    for (let i = 0; i < result.weighted_matrix.length; i++) {
        for (let j = 0; j < result.weighted_matrix.length; j++) {
            if (i != j) {
                let c_indeks = `C${i+1}${j+1}`
                console.log(result.concordance_set.c_indeks)
                let value_c_set = result.concordance_set[c_indeks]
                let temp_html = `
                <table>
                    <tr>
                        <td class="title-electre-form">${c_indeks}</td>
                        <td>${value_c_set}</td>
                    </tr>
                </table>
                `
                $('#c-set').append(temp_html);
            }
        }
    }
}

// function calculate_csv() {
//     var csv_file = $('#csv-file').val()

//     let form_data = new FormData()
//     form_data.append('csv_file', csv_file)

//     $.ajax({
//         type: 'POST',
//         url: '/post_electre_four',
//         data: form_data,
//         contentType: false,
//         processData: false,
//         success: function (response) {
//             console.log(response)
//         },
//         error: function (xhr, status, error) {
//             // console.log(error)
//             alert('Enter a New Matrix or Weight!!!\nInvalid Matrix or Weight!!!')
//         }
//     })
// }