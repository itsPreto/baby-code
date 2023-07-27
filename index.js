 const sendButton = document.getElementById("sendButton");
 const output = document.getElementById("output");

 const codeTextarea = document.getElementById('code');

 codeTextarea.oninput = function() {
     this.style.textAlign = this.value ? 'left' : 'center';
 };
 // Get placeholder text
 const text = output.placeholder;

 // Match delimiters
 const formatted = text.replace(/\[INST\] <<SYS>> <\/SYS>> \[\/INST\]/g,
   '<span style="color: blue">$&</span>'
 );

 // Set formatted text as new placeholder
 output.placeholder = formatted;

 function makeEditable() {
   // Toggle editability
   output.readOnly = !output.readOnly;

   // Change caret color based on editability
   if (output.readOnly) {
     output.style.caretColor = 'transparent';
   } else {
     output.style.caretColor = 'auto';

     // Focus textarea when made editable
     output.focus();
     output.value = output.placeholder;
   }
 }

 let currentLogo = 1;

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


 // Call animateLogo every second
 setInterval(animateLogo, 8000);

 const btn1 = document.getElementById("btn1");
 const btn2 = document.getElementById("btn2");
 const btn3 = document.getElementById("btn3");
 const footerButtons = document.getElementById('footer-buttons');

 function toggleVerticalScrollOnBody() {
 console.log("output width:" + output.style.width);
 console.log("footerButtons width:" + footerButtons.style.width);
 footerButtons.style.width = getComputedStyle(output).width;
 // Get the height of the output window
 const outputHeight = document.getElementById('output').offsetHeight;

 // If the output window height is greater than 520px, enable scrolling on the body
 if (outputHeight > 523) {
     document.body.style.overflowY = 'scroll';
 }
 // If the output window height is less than or equal to 520px, disable scrolling on the body
 else {
     document.body.style.overflowY = 'hidden';
 }
 }
 toggleVerticalScrollOnBody()

 new ResizeObserver(toggleVerticalScrollOnBody).observe(output)

 btn1.addEventListener('click', function() {
     console.log("Button 1 clicked");
     // Add your code here
 });

 btn2.addEventListener('click', function() {
     console.log("Button 2 clicked");
     // Add your code here
 });

 btn3.addEventListener('click', function() {
     console.log("Button 3 clicked");
     // Add your code here
 });
 output.addEventListener('keydown', e => {

   // Check if Shift+Enter was pressed
   if(e.shiftKey && e.key === 'Enter') {
     // Prevent browser from inserting newline
     e.preventDefault();

     // If already in edit mode, update placeholder and clear text
     if(!output.readOnly) {
       // Get current text
       const text = e.target.value;

       // Update placeholder with current text
       e.target.placeholder = text;

       // Reset value to empty string
       e.target.value = "";
     }

     // Toggle editability
     output.readOnly = !output.readOnly;

     // Change caret color based on editability
     if (output.readOnly) {
       output.style.caretColor = 'transparent';
     } else {
       output.style.caretColor = 'auto';

       // Focus textarea when made editable
       output.focus();
       output.value = output.placeholder;
     }
   }
 });


 async function sendCode() {
 document.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/WwxRR.gif')";
   document.getElementById('output').value = "";
   try {

     // Get raw prompt text
     const question = document.getElementById('code').value;

     // Wrap it in the INST format
     const formattedPrompt = `
     [INST]
     {
       "prompt": "${question}"
     }
     [/INST]`;

     // Send formattedPrompt to API
     const response = await fetch('http://localhost:8000/generate', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({
         question: formattedPrompt
       })
     });

     if (!response.ok) {
       const message = `An error has occurred: ${response.status}`;
       throw new Error(message);
     }

     const code = await response.text();

     const runResponse = await fetch('http://localhost:8000/run', {
       method: 'POST',
       headers: {
         'Content-Type': 'application/json',
       },
       body: JSON.stringify({code}),
     });

     if (!runResponse.ok) {
       const message = `An error has occurred: ${runResponse.status}`;
       throw new Error(message);
     }

     const output = await runResponse.text();
     document.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/mJHTA.png')";
     document.getElementById('output').value = output;
   } catch (error) {
     console.log(error);
     document.getElementById('output').value = "Error: " + error.message;
     document.querySelector(".hoverable").style.backgroundImage = "url('https://i.stack.imgur.com/mJHTA.png')";
   }
 }
