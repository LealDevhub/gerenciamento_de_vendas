var btnExport = document.querySelector('#btnExport')

btnExport.onclick = () => exportData('xlsx')

function exportData(type) {
  const fileName = 'exported-table.' + type
  const table = document.querySelector('#table')
  const wb = XLSX.utils.table_to_book(table)
  XLSX.writeFile(wb, fileName)
}
