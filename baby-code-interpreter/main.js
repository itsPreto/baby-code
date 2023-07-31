import { requestCompletion } from './request_completion.js';

window.onload = function () {
  const codeTextarea = document.getElementById('code');
  const btn1 = document.getElementById("btn1");
  let currentLogo = 1;

  // make sure the container is empty for the placeholder to show
  document.querySelector('.container').innerHTML = '';

  setInterval(animateLogo, 3500);

  const instructionsPlaceholder = `<\uD83D\uDC0D\uD83E\uDD99>\\A~~~~~~~~~\\A 100% Open Source. Llama-based, & Super Fun & Easy to Use.\\A~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \\A      1. Enter your prompt. \uD83D\uDCAC    \\A 2. Hit it up \uD83C\uDF4C.\\A                  3. Verify the code. \uD83D\uDD0D               \\A       4. Run it up. \uD83D\uDE80.     \\A           5. Inspect the output. \uD83D\uDD75        \\A         6. Debug it up. \uD83D\uDC1B.     \\A \\A           \uD83C\uDF0D Go Democracy \uD83C\uDF0D          \\A \\A \u2728 Happy Coding \u2728 \\A     ~~~~~~~~~~~~~~~~~    `;


  const instructions_style = document.createElement('style');
  instructions_style.innerHTML = `
      .container::before {
        content: "${instructionsPlaceholder}";
        white-space: pre-wrap;
      }
    `;

  document.head.appendChild(instructions_style);



  // ========= listeners =========

  document.querySelector('.container').addEventListener('animationend', function (event) {
    if (event.animationName === 'flyInFromLeft') {
      this.classList.add('fadeInPlaceholder');
      this.classList.remove('fadeOutPlaceholder');
    }
  });

  btn1.addEventListener('click', function () {
    const pythonCode = document.getElementById('output').value;
    fetch('/run_python_code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code: pythonCode })
    })
      .then(response => response.json())
      .then(data => {
        console.log(data.result);
      });
  });


  document.getElementById('code').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (this.value.trim() !== '') {
        console.log(this.value);
        requestCompletion(document);
      }
    }
  });

  document.getElementById('sendButton').addEventListener('click', async function () {
    await requestCompletion(document);
  });

  codeTextarea.oninput = function () {
    this.style.textAlign = this.value ? 'left' : 'center';
  };


  function animateLogo() {
    // Fade out and lower z-index of current logo
    const currentLogoElement = document.getElementById(`logo${currentLogo}`);
    currentLogoElement.style.opacity = '0';
    currentLogoElement.style.zIndex = '0';

    // Increment currentLogo, looping back to 1 if necessary
    currentLogo = currentLogo % 3 + 1;

    // Fade in and raise z-index of next logo
    const nextLogoElement = document.getElementById(`logo${currentLogo}`);
    nextLogoElement.style.opacity = '1';
    nextLogoElement.style.zIndex = '1';
  }
}