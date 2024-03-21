type Return = {
    [key: string]: any
};

function getKeyValues(searchParams: URLSearchParams): Promise<Return> {
    return new Promise((res) => {
        const object: Return = {};

        searchParams.forEach((value, key) => {
            object[key] = value;
        });

        res(object);
    });
}

export default getKeyValues;