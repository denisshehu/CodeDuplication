/**
 * Checks whether {@param number} is prime.
 *
 * @param number  an integer
 * @returns {boolean}  whether {@param number} is prime
 */
function isPrime(number) {
    let result = true;
    // check whether the number is divisible by any number between 2 and its half
    for (let i = 2; i <= number / 2; i++) {
        if (number % i === 0) { // number is not only divisible by 1 and itself
            result = false; break;
        }
    }
    return result;
}