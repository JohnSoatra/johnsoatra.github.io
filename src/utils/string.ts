function capitalize(string: string) {
    return string && string[0].toUpperCase() + string.slice(1);
}

function isLink(string: string) {
    return string.startsWith('http://') || string.startsWith('https://');
}

export {
    isLink,
    capitalize
}