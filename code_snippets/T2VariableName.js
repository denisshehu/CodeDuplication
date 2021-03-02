function isPrime(number) {
    let isPrime = true;

    for (let j = 2; j <= number / 2; j++) {
        if (number % j === 0) {
            isPrime = false;
            break;
        }
    }

    return isPrime;
}