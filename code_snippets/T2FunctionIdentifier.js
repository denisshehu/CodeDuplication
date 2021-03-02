function isNumberPrime(value) {
    let result = true;

    for (let i = 2; i <= value / 2; i++) {
        if (value % i === 0) {
            result = false;
            break;
        }
    }

    return result;
}