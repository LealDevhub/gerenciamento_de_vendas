/* globals Chart:false */
const dates = document.querySelectorAll('.dates')
const values = document.querySelectorAll('.values')
const array_dates = Array.from(dates)
const array_values = Array.from(values)

var lista = []
var valores = []

array_dates.forEach(item => {
  lista.push(item.value)
})
array_values.forEach(val => {
  var valor = Number(val.value)
  if (valores.length == 0) {
    valores.push(valor)
  } else {
    valores.push(valor + valores[valores.length - 1])
  }
})
;(() => {
  'use strict'

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars

  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: lista,
      datasets: [
        {
          data: valores,
          lineTension: 0,
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          borderWidth: 4,
          pointBackgroundColor: '#007bff'
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  })
})()
