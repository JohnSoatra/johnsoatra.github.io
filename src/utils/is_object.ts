function isObject(string: any) {
    if (typeof string === 'object' && string.length === undefined) {
        return true;
    }

    return false;
}

export default isObject;