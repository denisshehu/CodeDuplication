function isNumberPrime(value) {
    var isPrime = true;

    for (let j = 2; j <= value / 2; j++) {
        if (value % j === 0) {
            isPrime = false;
            break;
        }
    }

    return isPrime;
}