$(document).ready(function () {
  $('#btnExport').click(function (e) {
    e.preventDefault()

    var DivTabela = document.querySelector('#divTabela')
    var dados = new Blob(['\ufeff' + DivTabela.outerHTML], {
      type: 'application/vnd.ms-excel'
    })
    var url = window.URL.createObjectURL(dados)

    var a = document.createElement('a')

    a.href = url
    a.download = 'export-table'

    a.click()
  })
})
