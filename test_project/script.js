let count = 0;

const countDisplay = document.getElementById("count");

function updateDisplay() {
    countDisplay.textContent = count;

    if (count > 0) {
        countDisplay.style.color = "lightgreen";
    } else if (count < 0) {
        countDisplay.style.color = "red";
    } else {
        countDisplay.style.color = "white";
    }
}

function increase() {
    count++;
    updateDisplay();
}

function decrease() {
    count--;
    updateDisplay();
}

function reset() {
    count = 0;
    updateDisplay();
}