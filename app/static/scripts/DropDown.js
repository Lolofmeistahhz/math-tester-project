document.addEventListener("DOMContentLoaded", function() {
  const toggleButton9 = document.getElementById("toggleButton9");
  const hiddenBlock9 = document.getElementById("hiddenBlock9");
  let isHidden9 = true;

  toggleButton9.addEventListener("click", function() {
    if (isHidden9) {
      hiddenBlock9.style.display = "block";
      toggleButton9.textContent = "Скрыть";
    } else {
      hiddenBlock9.style.display = "none";
      toggleButton9.textContent = "Показать";
    }
    isHidden9 = !isHidden9;
  });

  const toggleButton10 = document.getElementById("toggleButton10");
  const hiddenBlock10 = document.getElementById("hiddenBlock10");
  let isHidden10 = true;

  toggleButton10.addEventListener("click", function() {
    if (isHidden10) {
      hiddenBlock10.style.display = "block";
      toggleButton10.textContent = "Скрыть";
    } else {
      hiddenBlock10.style.display = "none";
      toggleButton10.textContent = "Показать";
    }
    isHidden10 = !isHidden10;
  });

  const toggleButton11 = document.getElementById("toggleButton11");
  const hiddenBlock11 = document.getElementById("hiddenBlock11");
  let isHidden11 = true;

  toggleButton11.addEventListener("click", function() {
    if (isHidden11) {
      hiddenBlock11.style.display = "block";
      toggleButton11.textContent = "Скрыть";
    } else {
      hiddenBlock11.style.display = "none";
      toggleButton11.textContent = "Показать";
    }
    isHidden11 = !isHidden11;
  });
});
