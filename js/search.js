function search() {
    // for (let i = 1; i < 100; i ++) {
        fetch('http://google.com').then(res => {
            console.log(res);
        });
    // }
}

search()