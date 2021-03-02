function isPrime(number) {
    let result = true;

    for (let i = 2; i <= number / 2; i++) {
        let remainder = number % i;
        if (remainder === 0) {
            result = false;
            break;
        }
    }

    return result;
}