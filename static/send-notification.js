let tel = ''
let message = ''
let wppUrl = ''

function createUrl() {
  selectTel = document.querySelector('.dest')
  selectVenda = document.querySelector('.vendas')
  selectPrazo = document.querySelector('.prazo')

  var valueTel = selectTel.value
  var valueVenda = selectVenda.value
  var valuePrazo = selectPrazo.value
  var dataFinal = document.querySelector('.data-final').value
  var pn = document.querySelector('.part-number').value
  var qtd = document.querySelector('.qtd').value
  var obs = document.querySelector('.obs').value

  var vd = valueVenda.split(' - ')

  var dataFinalBr = dataFinal.split('-').reverse().join('/')

  message = `Cliente: ${vd[2]},
             Nº Pedido/NF: ${vd[0]},
             Empresa: ${1},
             Data da venda: ${vd[3]},
             Prazo informado: ${valuePrazo},
             Data final: ${dataFinalBr},
             P/N: ${pn},
             Qtd: ${qtd},
             Obs: ${obs}`

  var messageUri = encodeURI(message)
  wppUrl =
    'https://api.whatsapp.com/send?phone=' + valueTel + '&text=' + messageUri

  var a = document.createElement('a')

  a.href = wppUrl
  a.target = '_blank'

  a.click()
}
