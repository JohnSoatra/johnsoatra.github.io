import { isLink } from "./string";

function isNullUndefined(value: any) {
    return (
        value === null ||
        value === undefined
    );
}

function stringEmpty(value: string) {
    return value === '';
}

function isPositive(num: number) {
    return num > 0;
}

function isZero(num: number) {
    return num === 0;
}

function isNegative(num: number) {
    return num < 0;
}

function isUndefined(value: any) {
    return value === undefined;
}

function isImageUrl(url: string) {
    return isLink(url) && hasImageExtension(url);
}

function hasImageExtension(url: string) {
    return /\.(png|svg)+$/.test(url);
}

export {
    isNullUndefined,
    stringEmpty,
    isPositive,
    isNegative,
    isZero,
    isUndefined,
    isImageUrl
};