function getFileDirectory(filename) {
  const array = filename.split('/')
  return array[array.length - 2]
}
export function getFilename(filename) {
  const array = filename.split('/')
  return array[array.length - 1]
}
export function getFileRoot(filename) {
  let array = filename.split('/')
  const directory = getFileDirectory(filename)
  if (directory === undefined) {
    return
  }
  array = array.slice(0, array.length - 2)
  array = array.map((x) => x[0])
  array.push(directory)
  array = array.join('/')
  array = `${array}/`
  return array
}
export function getChangeTypeColor(changeType) {
  if (changeType === 'D') {
    return 'text-pink-600'
  } else {
    return 'text-blue-400'
  }
}
