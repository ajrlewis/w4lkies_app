// Toggles the checked class in the checkbox
function toggleCheckbox(checkbox) {
  console.log("toggleCheckbox");
  checkbox.classList.toggle("checked");
  var input = checkbox.querySelector("input[type='checkbox']");
  input.checked = !input.checked;
}

// Get current date and time
function getCurrentTime() {
  var now = new Date();
  return now.toLocaleString();
}