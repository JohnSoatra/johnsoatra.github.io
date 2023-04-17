const fs = require('fs');
const chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
// 0-61

const amount = 1;
const range = 3;
const limit = 1;

function looper(
    baseString,
    charLength,
    arr = []
) {
    const newArr = [];

    if (arr.length) {
        for (let each of arr) {
            for (let i = 0; i < baseString.length; i ++) {
                newArr.push(baseString[i] + each);
            }
        }
    } else {
        for (let i = 0; i < baseString.length; i ++) {
            newArr.push(baseString[i]);
        }
    }

    if (newArr[0].length === charLength) {
        return newArr;
    } else {
        return looper(baseString, charLength, newArr);
    }

}

const res = looper(chars, 4);
console.log(res.join(','))
