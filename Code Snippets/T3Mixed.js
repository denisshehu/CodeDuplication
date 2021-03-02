function isPrime(number) {

    for (let i = 2; i <= number / 2; i++) {
        let remainder = number % i
        if (remainder === 0) {
            return false
        }
    }

    return true
}