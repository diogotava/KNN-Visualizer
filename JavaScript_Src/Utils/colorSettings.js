let previousColors = {}

function settingsColorsBehaviour() {
    const settingsColorsCloseButton = document.getElementById('settingsColorsCloseButton');
    const settingsColorsSaveButton = document.getElementById('settingsColorsSaveButton');
    const settingsColorsPopup = document.getElementById('settingsColorsPopup');

    settingsColorsCloseButton.addEventListener('click', () => {
        settingsColorsPopup.style.display = 'none';
    });

    settingsColorsSaveButton.addEventListener('click', (event) => {
        event.preventDefault();
        updateColors();
    });
}

function updateColorsShownValues() {
    const colorList = document.getElementById("color-list");
    colorList.innerHTML = '';

    Object.keys(dynamicValues.colors).forEach(key => {
        // Create list item for each color option
        const listItem = document.createElement("li");

        // Create a label with the color name
        const nameLabel = document.createElement("label");
        nameLabel.textContent = key;

        // Create an input field for changing the color
        const colorInput = document.createElement("input");
        colorInput.id = key;
        colorInput.type = "color";
        colorInput.value = rgbToHex(dynamicValues.colors[key][0], dynamicValues.colors[key][1], dynamicValues.colors[key][2]);

        nameLabel.className = 'colorLabel';

        const colorReset = document.createElement("button");
        colorReset.className = "button-12";
        colorReset.innerHTML = "Reset";

        // Add event listener to reset the color
        colorReset.addEventListener("click", event => {
            event.preventDefault();
            let color;
            let resetPrevious = document.getElementById('resetPrevious').checked;
            if (resetPrevious) {
                color = previousColors[key];
                colorInput.value = rgbToHex(color[0], color[1], color[2]);
            } else {
                color = rgbToHex(defaultColors[key][0], defaultColors[key][1], defaultColors[key][2]);
                previousColors[key] = [parseInt(color.substring(1, 3), 16), parseInt(color.substring(3, 5), 16), parseInt(color.substring(5, 7), 16)];
                colorInput.value = color;
            }
        });

        // Append the label and input field to the list item
        listItem.appendChild(nameLabel);
        listItem.appendChild(colorInput);
        listItem.appendChild(colorReset);

        // Append the list item to the color list
        colorList.appendChild(listItem);
    });
    const listItem = document.createElement("li");
    const input = document.createElement("input");
    input.className = 'colorLabel';
    input.type = "text";
    input.style.width = "220px";
    input.style.marginRight = "20px";
    input.style.color = 'black'
    const colorInput = document.createElement("input");
    colorInput.type = "color";
    colorInput.value = rgbToHex(dynamicValues.colors['Default'][0], dynamicValues.colors['Default'][1], dynamicValues.colors['Default'][2]);

    const addColor = document.createElement("button");
    addColor.className = "button-12";
    addColor.innerHTML = "Add";
    addColor.style.width = "66px";

    // Add event listener to reset the color
    addColor.addEventListener("click", event => {
        event.preventDefault();
        let color = colorInput.value;
        color = [parseInt(color.substring(1, 3), 16), parseInt(color.substring(3, 5), 16), parseInt(color.substring(5, 7), 16)];
        dynamicValues.colors[input.value] = color;
        updateColorsShownValues();
        input.value = "";
        colorInput.value = rgbToHex(dynamicValues.colors['Default'][0], dynamicValues.colors['Default'][1], dynamicValues.colors['Default'][2]);
    });

    // Append the label and input field to the list item
    listItem.appendChild(input);
    listItem.appendChild(colorInput);
    listItem.appendChild(addColor);

    // Append the list item to the color list
    colorList.appendChild(listItem);
}

//-------------------------------------------------------- UPDATE --------------------------------------------------------//
function updateColors() {
    Object.keys(dynamicValues.colors).forEach(key => {

        let color = document.getElementById(key).value;
        if (!equalsCheck([parseInt(color.substring(1, 3), 16), parseInt(color.substring(3, 5), 16), parseInt(color.substring(5, 7), 16)], dynamicValues.colors[key]))
            previousColors[key] = dynamicValues.colors[key];
        dynamicValues.colors[key] = [parseInt(color.substring(1, 3), 16), parseInt(color.substring(3, 5), 16), parseInt(color.substring(5, 7), 16)];

    });
}
