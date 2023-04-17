const string = 'aabc';
const set = [...new Set(string.split(''))].join('')
console.log(set)