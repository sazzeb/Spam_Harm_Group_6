document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('data-form');
    const textarea = document.getElementById('main-textarea');
    const resultsSection = document.getElementById('results-section');
    const resultH2 = document.getElementById('result-h2');
    const resultPBold = document.getElementById('result-p-bold');
    const resultPSpan = document.getElementById('result-p-span');
    const resultH3 = document.getElementById('result-h3');
    const resultList = document.getElementById('result-list');

    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent page reload

        const textInput = textarea.value.trim();
        if (textInput) {
            // Split the input into lines to populate the results
            const lines = textInput.split('\n').filter(line => line.trim() !== '');

            if (lines.length > 0) {
                // Update H2 with the first line
                resultH2.textContent = lines[0];

                // Update the p with bold and span with subsequent lines
                if (lines.length > 1) {
                    resultPBold.textContent = lines[1];
                    resultPSpan.textContent = lines.length > 2 ? lines[2] : '';
                } else {
                    resultPBold.textContent = 'No bold text entered.';
                    resultPSpan.textContent = '';
                }

                // Update H3 with another line
                if (lines.length > 3) {
                    resultH3.textContent = lines[3];
                } else {
                    resultH3.textContent = 'No H3 text entered.';
                }

                // Populate the list with remaining items
                resultList.innerHTML = ''; // Clear previous list items
                const listItems = lines.slice(4, 8); // Take up to 4 items for the list
                if (listItems.length > 0) {
                    listItems.forEach(itemText => {
                        const li = document.createElement('li');
                        li.textContent = itemText;
                        resultList.appendChild(li);
                    });
                } else {
                     const li = document.createElement('li');
                     li.textContent = 'No list items entered.';
                     resultList.appendChild(li);
                }

                // Show the results section
                resultsSection.style.display = 'block';
            }
        }
    });
});