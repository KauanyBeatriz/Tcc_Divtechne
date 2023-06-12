var activeButtonId = null;

    function changeColor(buttonId) {
      var button = document.getElementById(buttonId);

      if (activeButtonId !== null) {
        var activeButton = document.getElementById(activeButtonId);
        activeButton.classList.remove('active');
      }

      button.classList.add('active');
      activeButtonId = buttonId;
    }