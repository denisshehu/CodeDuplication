function isPrime(number) {
    var result = true;

    for (var i = 2; i <= number / 2; i++) {
        if (number % i === 0) {
            result = false;
            break;
        }
    }

    return result;
}