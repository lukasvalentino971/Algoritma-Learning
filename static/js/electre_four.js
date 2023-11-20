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
            // console.log(response)
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

    // Update Matriks R
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

    // Update Matriks V
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

    // Update Himpunan Concordance
    $('#c-set').empty();

    let set_index = 0

    for (let i = 0; i < result.weighted_matrix.length; i++) {
        for (let j = 0; j < result.weighted_matrix.length; j++) {
            if (i != j) {
                let c_indeks = `C${i+1}${j+1}`
                let value_c_set = result.concordance_set[set_index][c_indeks]
                let temp_html = `
                <table>
                    <tr>
                        <td class="title-electre-form">${c_indeks}</td>
                        <td>{${value_c_set}}</td>
                    </tr>
                </table>
                `
                $('#c-set').append(temp_html);
                set_index++
            }
        }
    }

    // Update Matriks Concordance
    $('#c-matrix').empty();

    for (let i = 0; i < result.concordance_matrix.length; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < result.concordance_matrix[0].length; j++) {
            temp_html += `
            <td>
                ${result.concordance_matrix[i][j]}
            </td>
            `
        }
        temp_html += `</tr>`
        $('#c-matrix').append(temp_html);
    }

    // Update Himpunan Discordance
    $('#d-set').empty();

    set_index = 0

    for (let i = 0; i < result.weighted_matrix.length; i++) {
        for (let j = 0; j < result.weighted_matrix.length; j++) {
            if (i != j) {
                let d_indeks = `D${i+1}${j+1}`
                let value_d_set = result.discordance_set[set_index][d_indeks]
                let temp_html = `
                <table>
                    <tr>
                        <td class="title-electre-form">${d_indeks}</td>
                        <td>{${value_d_set}}</td>
                    </tr>
                </table>
                `
                $('#d-set').append(temp_html);
                set_index++
            }
        }
    }

    // Update Matriks Discordance
    $('#d-matrix').empty();

    for (let i = 0; i < result.discordance_matrix.length; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < result.discordance_matrix[0].length; j++) {
            temp_html += `
            <td>
                ${result.discordance_matrix[i][j]}
            </td>
            `
        }
        temp_html += `</tr>`
        $('#d-matrix').append(temp_html);
    }

    // Update Matriks Dominan Concordance
    $('#d-c-matrix').empty();

    for (let i = 0; i < result.dominance_concordance_matrix.length; i++) {
        let temp_html = `<tr>`
        for (let j = 0; j < result.dominance_concordance_matrix.length; j++) {
            temp_html += `
            <td>
                ${result.dominance_concordance_matrix[i][j]}
            </td>
            `
        }
        temp_html += `</tr>`
        $('#d-c-matrix').append(temp_html);
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